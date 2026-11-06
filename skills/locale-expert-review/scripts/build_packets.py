#!/usr/bin/env python3
"""Builds one review packet per locale: every shipped string beside its source text and context, plus the extra texts
and the rendered screens a reviewer should look at.

Usage: build_packets.py config.json out_dir

config.json:
{
  "source": "en",                                    # source language code in the String Catalogs
  "xcstrings": ["path/Localizable.xcstrings"],       # Apple String Catalogs (optional)
  "android_res": ["path/app/src/main/res"],          # Android res directories, one per module (optional)
  "messages": {"Flutter": "path/l10n/app_{lang}.arb"},  # flat or nested JSON message files, {lang} per locale (optional)
  "locales": [
    {
      "id": "ar-SA",                                 # packet name
      "name": "Arabic (Saudi Arabia)",               # shown to the reviewer
      "xcstrings": "ar",                             # language code inside the catalogs, or null
      "android": "values-ar",                        # values folder, or null
      "messages": "ar",                              # code that fills {lang} in "messages", or null
      "texts": [["Store description", "path/en.txt", "path/ar.txt"]],   # label, source file, translated file
      "screens": ["path/screens/ar/home.png"]        # rendered screens in this locale
    }
  ]
}

Only the standard library is used. Nothing is sent anywhere.
"""
import json
import os
import sys
import xml.etree.ElementTree as ET


def flat(s):
    return " ".join(str(s).split()) if s is not None else ""


def xc_values(loc):
    """Yields (variant label, text) for one localization of a String Catalog entry."""
    if not loc:
        return
    if "stringUnit" in loc:
        yield "", loc["stringUnit"].get("value", "")
    for kind, cases in loc.get("variations", {}).items():
        for case, inner in cases.items():
            for label, text in xc_values(inner):
                yield f"{kind}={case}" + (f" {label}" if label else ""), text
    for name, sub in loc.get("substitutions", {}).items():
        for label, text in xc_values(sub):
            yield f"%#@{name}@ {label}".strip(), text


def source_for(src, variant, key):
    """The source text for a case the target has and the source may not, such as Arabic's "two".
    A prefixed case ("%#@items@ plural=two", "device=mac plural=two") falls back to the source's "other" case under the
    same prefix, then to any source case under that prefix, then to the plain source text."""
    if variant in src:
        return src[variant]
    prefix = variant.rsplit("plural=", 1)[0] if "plural=" in variant else ""
    if prefix + "plural=other" in src:
        return src[prefix + "plural=other"]
    same = [v for k, v in sorted(src.items()) if prefix and k.startswith(prefix)]
    return same[0] if same else src.get("plural=other", src.get("", key))


def xc_rows(paths, source, lang):
    rows = []
    for path in paths:
        data = json.load(open(path, encoding="utf-8"))
        src_lang = data.get("sourceLanguage", source)
        for key, entry in sorted(data.get("strings", {}).items()):
            if entry.get("shouldTranslate") is False:
                continue
            locs = entry.get("localizations", {})
            src = dict(xc_values(locs.get(src_lang))) or {"": key}
            tgt = dict(xc_values(locs.get(lang)))
            comment = flat(entry.get("comment"))
            if not key.strip():
                continue
            # A language may split a string into plural cases that the source does not use, or the reverse.
            # Each case is a row, and a translation is MISSING only when the language has no text at all.
            for variant in sorted(set(tgt) or set(src)):
                rows.append((os.path.basename(path), key, variant, source_for(src, variant, key),
                             tgt.get(variant, "MISSING"), comment))
    return rows


def android_values(folder):
    out = {}
    if not folder or not os.path.isdir(folder):
        return out
    for name in sorted(os.listdir(folder)):
        if not name.endswith(".xml"):
            continue
        try:
            root = ET.parse(os.path.join(folder, name)).getroot()
        except ET.ParseError:
            continue
        for el in root:
            key = el.get("name")
            if not key or el.get("translatable") == "false":
                continue
            if el.tag == "string":
                out[(key, "")] = "".join(el.itertext())
            elif el.tag == "plurals":
                for item in el.findall("item"):
                    out[(key, "quantity=" + item.get("quantity", ""))] = "".join(item.itertext())
            elif el.tag == "string-array":
                for i, item in enumerate(el.findall("item")):
                    out[(key, f"[{i}]")] = "".join(item.itertext())
    return out


def android_rows(res_dirs, folder):
    src, tgt = {}, {}
    for res in res_dirs:
        src.update(android_values(os.path.join(res, "values")))
        tgt.update(android_values(os.path.join(res, folder)))
    rows = []
    keys = sorted({k for k, _ in src} | {k for k, _ in tgt})
    for key in keys:
        src_v = {v for k, v in src if k == key}
        tgt_v = {v for k, v in tgt if k == key}
        if any(v.startswith("quantity=") for v in src_v | tgt_v):
            # Plural cases follow the language: Japanese has only "other", Arabic has six.
            variants = sorted(tgt_v) or sorted(src_v)
        else:
            # Strings and array items: every source row shows, so a shorter translated array reads MISSING.
            variants = sorted(src_v | tgt_v, key=lambda v: (len(v), v))
        for variant in variants:
            english = src.get((key, variant), src.get((key, "quantity=other"), ""))
            rows.append(("strings.xml", key, variant, english, tgt.get((key, variant), "MISSING"), ""))
    return rows


def flatten(obj, prefix=""):
    """Flat key-to-text pairs from a message file: Flutter ARB or nested web JSON. ARB "@" metadata is skipped."""
    out = {}
    for k, v in obj.items():
        if k.startswith("@"):
            continue
        key = f"{prefix}.{k}" if prefix else k
        if isinstance(v, dict):
            out.update(flatten(v, key))
        elif isinstance(v, str):
            out[key] = v
    return out


def message_rows(source_path, target_path):
    src_raw = json.load(open(source_path, encoding="utf-8"))
    tgt_raw = json.load(open(target_path, encoding="utf-8")) if os.path.exists(target_path) else {}
    src, tgt = flatten(src_raw), flatten(tgt_raw)
    rows = []
    for key in sorted(set(src) | set(tgt)):
        meta = src_raw.get("@" + key) if isinstance(src_raw.get("@" + key), dict) else {}
        rows.append((os.path.basename(target_path), key, "", src.get(key, ""), tgt.get(key, "MISSING"),
                     flat(meta.get("description"))))
    return rows


def table(rows):
    lines = ["| file | key | variant | source | translation | context |", "|---|---|---|---|---|---|"]
    for f, key, variant, src, tgt, comment in rows:
        cells = [f, key, variant, src, tgt, comment]
        lines.append("| " + " | ".join(flat(c).replace("|", "\\|") for c in cells) + " |")
    return "\n".join(lines)


def main():
    config_path, out_dir = sys.argv[1], sys.argv[2]
    base = os.path.dirname(os.path.abspath(config_path))
    cfg = json.load(open(config_path, encoding="utf-8"))
    here = lambda p: p if os.path.isabs(p) else os.path.join(base, p)
    os.makedirs(out_dir, exist_ok=True)
    for loc in cfg["locales"]:
        parts = [f"# Review packet: {loc['name']} ({loc['id']})", ""]
        counts = []
        if cfg.get("xcstrings") and loc.get("xcstrings"):
            rows = xc_rows([here(p) for p in cfg["xcstrings"]], cfg.get("source", "en"), loc["xcstrings"])
            counts.append(f"{len(rows)} Apple rows")
            parts += ["## Apple strings", "", table(rows), ""]
        if cfg.get("android_res") and loc.get("android"):
            res = cfg["android_res"] if isinstance(cfg["android_res"], list) else [cfg["android_res"]]
            rows = android_rows([here(p) for p in res], loc["android"])
            counts.append(f"{len(rows)} Android rows")
            parts += ["## Android strings", "", table(rows), ""]
        for label, pattern in cfg.get("messages", {}).items():
            if loc.get("messages"):
                rows = message_rows(here(pattern.replace("{lang}", cfg.get("source", "en"))),
                                    here(pattern.replace("{lang}", loc["messages"])))
                counts.append(f"{len(rows)} {label} rows")
                parts += [f"## {label} strings", "", table(rows), ""]
        for label, src_path, tgt_path in loc.get("texts", []):
            src = open(here(src_path), encoding="utf-8").read() if src_path and os.path.exists(here(src_path)) else ""
            tgt = open(here(tgt_path), encoding="utf-8").read() if os.path.exists(here(tgt_path)) else "MISSING"
            parts += [f"## {label}", "", "Source:", "", "```text", src.strip(), "```", "", "Translation:", "",
                      "```text", tgt.strip(), "```", ""]
        screens = [here(p) for p in loc.get("screens", []) if os.path.exists(here(p))]
        if screens:
            parts += ["## Rendered screens", "", *[f"- {p}" for p in screens], ""]
        missing = [here(p) for p in loc.get("screens", []) if not os.path.exists(here(p))]
        if missing:
            parts += ["Screens listed in the config but not found:", "", *[f"- {p}" for p in missing], ""]
        path = os.path.join(out_dir, f"{loc['id']}.md")
        open(path, "w", encoding="utf-8").write("\n".join(parts))
        print(f"{loc['id']}: {', '.join(counts) or 'no strings'}, {len(loc.get('texts', []))} texts, {len(screens)} screens")


if __name__ == "__main__":
    main()
