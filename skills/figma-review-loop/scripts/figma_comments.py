#!/usr/bin/env python3
"""List a Figma file's comment threads with the frame each one is pinned to, and render frames.

  python3 figma_comments.py <file-key> [--all] [--json]
      open threads (or all with --all), oldest first, with replies
  python3 figma_comments.py <file-key> --render <out-dir> <node-id> [<node-id> ...]
      render frames as JPEG at 2x into <out-dir>, for review

The token comes from $FIGMA_TOKEN, or else from the macOS Keychain item named by
$FIGMA_KEYCHAIN_SERVICE (default "figma-pat"). It is sent only in the request header
and never printed. A personal access token is read-only for comments: resolving
happens in Figma itself. Stdlib only.
"""
import json
import os
import subprocess
import sys
import urllib.parse
import urllib.request

API = "https://api.figma.com/v1"


def token():
    if os.environ.get("FIGMA_TOKEN"):
        return os.environ["FIGMA_TOKEN"]
    service = os.environ.get("FIGMA_KEYCHAIN_SERVICE", "figma-pat")
    r = subprocess.run(["security", "find-generic-password", "-s", service, "-w"], capture_output=True, text=True)
    if r.returncode:
        sys.exit(f"No token: set FIGMA_TOKEN or add a Keychain item named {service!r}.")
    return r.stdout.strip()


def get(path, tok):
    req = urllib.request.Request(API + path, headers={"X-Figma-Token": tok})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.load(r)


def node_names(key, ids, tok):
    names = {}
    ids = sorted(ids)
    for i in range(0, len(ids), 50):
        q = urllib.parse.quote(",".join(ids[i:i + 50]))
        for nid, n in (get(f"/files/{key}/nodes?ids={q}&depth=1", tok).get("nodes") or {}).items():
            names[nid] = (n or {}).get("document", {}).get("name", "(deleted)")
    return names


def threads(key, include_resolved, tok):
    comments = get(f"/files/{key}/comments", tok)["comments"]
    roots = [c for c in comments if not c.get("parent_id")]
    if not include_resolved:
        roots = [c for c in roots if not c.get("resolved_at")]
    replies = {}
    for c in comments:
        if c.get("parent_id"):
            replies.setdefault(c["parent_id"], []).append(c)
    ids = {(c.get("client_meta") or {}).get("node_id") for c in roots} - {None}
    names = node_names(key, ids, tok) if ids else {}
    out = []
    for c in sorted(roots, key=lambda c: c["created_at"]):
        nid = (c.get("client_meta") or {}).get("node_id")
        out.append({
            "id": c["id"], "created_at": c["created_at"], "author": c["user"]["handle"],
            "resolved": bool(c.get("resolved_at")), "node_id": nid,
            "node_name": names.get(nid, "(canvas)" if nid is None else "(unknown)"),
            "message": c["message"],
            "replies": [{"author": r["user"]["handle"], "message": r["message"]}
                        for r in sorted(replies.get(c["id"], []), key=lambda r: r["created_at"])],
        })
    return out


def render(key, out_dir, ids, tok):
    os.makedirs(out_dir, exist_ok=True)
    q = urllib.parse.quote(",".join(ids))
    urls = get(f"/images/{key}?ids={q}&format=jpg&scale=2", tok)["images"]
    for nid, url in urls.items():
        if not url:
            print(f"{nid}: nothing rendered (empty or invisible node)")
            continue
        path = os.path.join(out_dir, nid.replace(":", "-") + ".jpg")
        urllib.request.urlretrieve(url, path)
        print(path)


def main(argv):
    if len(argv) < 2:
        sys.exit(__doc__)
    key, rest, tok = argv[1], argv[2:], token()
    if rest[:1] == ["--render"] and len(rest) >= 3:
        return render(key, rest[1], rest[2:], tok)
    result = threads(key, "--all" in rest, tok)
    if "--json" in rest:
        return print(json.dumps(result, ensure_ascii=False, indent=1))
    for t in result:
        state = "resolved" if t["resolved"] else "open"
        print(f"[{t['created_at'][:10]}] {state} · {t['node_name']} ({t['node_id']}) · {t['author']}: {t['message']}")
        for r in t["replies"]:
            print(f"    ↳ {r['author']}: {r['message']}")
    print(f"{len(result)} thread(s)")


if __name__ == "__main__":
    main(sys.argv)
