#!/usr/bin/env python3
"""Self-test for build_packets.py: python3 test_build_packets.py (exits 1 on a failure)."""
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w", encoding="utf-8").write(text)


def main():
    d = tempfile.mkdtemp()
    catalog = {"sourceLanguage": "en", "strings": {
        "items": {"localizations": {
            "en": {"stringUnit": {"value": "You have %#@n@"},
                   "substitutions": {"n": {"variations": {"plural": {
                       "one": {"stringUnit": {"value": "%arg item"}},
                       "other": {"stringUnit": {"value": "%arg items"}}}}}}},
            "ar": {"stringUnit": {"value": "لديك %#@n@"},
                   "substitutions": {"n": {"variations": {"plural": {
                       "two": {"stringUnit": {"value": "عنصران"}},
                       "other": {"stringUnit": {"value": "%arg عنصر"}}}}}}}}},
        "": {"localizations": {}},
    }}
    write(f"{d}/L.xcstrings", json.dumps(catalog, ensure_ascii=False))
    write(f"{d}/res/values/strings.xml", '<resources><string-array name="tabs"><item>Home</item><item>About</item>'
          '</string-array><plurals name="d"><item quantity="one">%d day</item><item quantity="other">%d days</item>'
          '</plurals></resources>')
    write(f"{d}/res/values-ar/strings.xml", '<resources><string-array name="tabs"><item>الرئيسية</item>'
          '</string-array></resources>')
    write(f"{d}/res/values-ja/strings.xml", '<resources><plurals name="d"><item quantity="other">%d日</item>'
          '</plurals></resources>')
    write(f"{d}/l10n/app_en.arb", json.dumps({"hello": "Hello", "@hello": {"description": "Greeting"}}))
    write(f"{d}/l10n/app_ar.arb", json.dumps({"hello": "مرحبا"}, ensure_ascii=False))
    config = {"source": "en", "xcstrings": ["L.xcstrings"], "android_res": ["res"],
              "messages": {"Flutter": "l10n/app_{lang}.arb"},
              "locales": [{"id": "ar", "name": "Arabic", "xcstrings": "ar", "android": "values-ar", "messages": "ar"},
                          {"id": "ja", "name": "Japanese", "xcstrings": None, "android": "values-ja"}]}
    write(f"{d}/config.json", json.dumps(config))
    subprocess.run([sys.executable, f"{HERE}/build_packets.py", f"{d}/config.json", f"{d}/out"], check=True,
                   capture_output=True)
    ar = open(f"{d}/out/ar.md", encoding="utf-8").read()
    ja = open(f"{d}/out/ja.md", encoding="utf-8").read()
    checks = {
        "a target-only plural case shows the source's other case": "| %#@n@ plural=two | %arg items | عنصران |" in ar,
        "a short translated array reads MISSING": "| tabs | [1] | About | MISSING |" in ar,
        "ARB rows carry their description": "| hello |  | Hello | مرحبا | Greeting |" in ar,
        "a language with only other has one plural row": ja.count("| d | quantity=") == 1,
        "an empty key is skipped": "| L.xcstrings |  |" not in ar,
    }
    failed = [name for name, ok in checks.items() if not ok]
    for name in checks:
        print(("FAIL " if name in failed else "ok   ") + name)
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
