#!/usr/bin/env python3
"""Answer sheets: open questions for a decision-maker as one self-contained HTML page.

  python3 answer_sheet.py build <questions-dir>/<date>.json
writes <date>.html next to the JSON.
  python3 answer_sheet.py serve <questions-dir> <answers-dir> [port]
serves the questions directory on 127.0.0.1 (default port 8765). The page's
"Save" button posts the answers, and the server writes them into
<answers-dir>/<date>.md: appended on the first save, replaced in place on a
later save of the same sheet, so other content in that file is kept.
Answers also autosave in the browser, so a reload loses nothing.

Question file format (JSON):
  {"date": "2026-01-15", "title": "...", "intro": "...",
   "questions": [{"id": "slug", "title": "...", "context": ["paragraph", ...],
                  "images": [{"src": "path relative to the questions directory", "caption": "..."}],
                  "options": [{"label": "...", "detail": "...", "recommended": true}]}]}
Paragraphs take **bold** and lines starting with "- " as bullets. Every question
gets a free-text note field, and an "Other" answer is always possible through it.
Stdlib only.
"""
import html
import json
import os
import re
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def inline(text):
    return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", html.escape(text))


def paragraphs(items):
    out, bullets = [], []
    for item in items + [""]:
        if item.startswith("- "):
            bullets.append(f"<li>{inline(item[2:])}</li>")
            continue
        if bullets:
            out.append("<ul>" + "".join(bullets) + "</ul>")
            bullets = []
        if item:
            out.append(f"<p>{inline(item)}</p>")
    return "".join(out)


def build(path):
    spec = json.load(open(path, encoding="utf-8"))
    if not DATE.match(spec["date"]):
        sys.exit("date must be YYYY-MM-DD")
    cards = []
    for n, q in enumerate(spec["questions"], 1):
        opts = []
        for i, o in enumerate(q["options"]):
            badge = '<span class="rec">Recommended</span>' if o.get("recommended") else ""
            opts.append(
                f'<label class="opt"><input type="radio" name="{q["id"]}" value="{i}">'
                f'<span><b>{inline(o["label"])}</b>{badge}'
                f'<small>{inline(o.get("detail", ""))}</small></span></label>')
        cards.append(
            f'<section class="q" id="{q["id"]}"><h2><span class="n">{n}</span>{inline(q["title"])}</h2>'
            f'<div class="ctx">{paragraphs(q["context"])}</div>'
            + (f'<div class="imgs">' + "".join(
                f'<figure><img src="{html.escape(i["src"])}" alt="{html.escape(i["caption"])}">'
                f'<figcaption>{inline(i["caption"])}</figcaption></figure>' for i in q["images"]) + '</div>'
               if q.get("images") else "") +
            f'<div class="opts">{"".join(opts)}</div>'
            f'<textarea name="{q["id"]}__note" placeholder="Notes, changes or a different answer (optional)"></textarea>'
            f'</section>')
    page = TEMPLATE.format(
        title=inline(spec["title"]), intro=paragraphs(spec.get("intro", [])),
        cards="".join(cards), spec=json.dumps(spec, ensure_ascii=False).replace("</", "<\\/"))
    out = os.path.splitext(path)[0] + ".html"
    open(out, "w", encoding="utf-8").write(page)
    print(out)


class Handler(SimpleHTTPRequestHandler):
    questions = answers = ""

    def __init__(self, *a, **kw):
        super().__init__(*a, directory=self.questions, **kw)

    def do_POST(self):
        if self.path != "/save":
            return self.send_error(404)
        body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        if not DATE.match(body.get("date", "")) or not isinstance(body.get("markdown"), str):
            return self.send_error(400)
        os.makedirs(self.answers, exist_ok=True)
        target = os.path.join(self.answers, body["date"] + ".md")
        # The file may already hold other notes, so only this sheet's block
        # is written: appended the first time, replaced in place on a later save.
        block = body["markdown"].strip() + "\n"
        heading = block.splitlines()[0]
        text = open(target, encoding="utf-8").read() if os.path.exists(target) else ""
        start = text.find(heading + "\n")
        if start < 0:
            text = text.rstrip("\n") + ("\n\n" if text.strip() else "") + block
        else:
            end = text.find("\n## ", start + len(heading))
            text = text[:start] + block + (text[end:] if end >= 0 else "")
        open(target, "w", encoding="utf-8").write(text)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(target.encode())


def serve(questions, answers, port):
    Handler.questions, Handler.answers = os.path.abspath(questions), os.path.abspath(answers)
    print(f"http://127.0.0.1:{port}/")
    ThreadingHTTPServer(("127.0.0.1", port), Handler).serve_forever()


TEMPLATE = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>{title}</title>
<style>
:root{{--bg:#f6f6f4;--card:#fff;--fg:#1b1b1b;--mut:#5d5d5d;--line:#dcdcd8;--acc:#1f6f5c;--sel:#e7f3ef}}
@media (prefers-color-scheme:dark){{:root{{--bg:#131416;--card:#1c1d20;--fg:#ececec;--mut:#a3a3a3;--line:#33353a;--acc:#5cc3a6;--sel:#1d2d29}}}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--fg);font:16px/1.55 -apple-system,system-ui,sans-serif}}
main{{max-width:780px;margin:0 auto;padding:28px 18px 120px}}h1{{font-size:26px;margin:0 0 6px}}
.intro{{color:var(--mut)}}.q{{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:20px 22px;margin:18px 0}}
.q.done{{border-color:var(--acc)}}h2{{font-size:19px;margin:0 0 10px;display:flex;gap:10px;align-items:baseline}}
.n{{flex:none;font-size:13px;color:var(--mut);border:1px solid var(--line);border-radius:99px;padding:0 8px}}
.ctx p{{margin:8px 0}}.ctx ul{{margin:6px 0;padding-left:22px}}.opts{{display:grid;gap:8px;margin:14px 0 10px}}
.opt{{display:flex;gap:10px;border:1px solid var(--line);border-radius:10px;padding:10px 12px;cursor:pointer}}
.opt:has(input:checked){{border-color:var(--acc);background:var(--sel)}}.opt input{{margin-top:5px;accent-color:var(--acc)}}
.imgs{{display:flex;gap:12px;overflow-x:auto;margin:10px 0}}figure{{margin:0;flex:none;width:240px}}
figure img{{width:240px;border-radius:12px;border:1px solid var(--line);cursor:zoom-in}}figcaption{{font-size:13px;color:var(--mut)}}
figure img.big{{width:402px}}figure:has(img.big){{width:402px}}
.opt small{{display:block;color:var(--mut);font-size:14px;margin-top:2px}}
.rec{{font-size:12px;color:var(--acc);border:1px solid var(--acc);border-radius:99px;padding:0 7px;margin-left:8px;white-space:nowrap}}
textarea{{width:100%;min-height:60px;border:1px solid var(--line);border-radius:10px;padding:10px;background:transparent;color:var(--fg);font:inherit}}
footer{{position:fixed;inset:auto 0 0 0;background:var(--card);border-top:1px solid var(--line);padding:12px 18px}}
footer div{{max-width:780px;margin:0 auto;display:flex;gap:10px;align-items:center}}#count{{flex:1;color:var(--mut)}}
button{{font:inherit;border:1px solid var(--acc);background:var(--acc);color:#fff;border-radius:10px;padding:8px 14px;cursor:pointer}}
button.alt{{background:transparent;color:var(--acc)}}
</style></head><body><main><h1>{title}</h1><div class="intro">{intro}</div>{cards}</main>
<footer><div><span id="count"></span><button class="alt" id="copy">Copy answers</button><button id="save">Save answers</button></div></footer>
<script>
const SPEC={spec};const KEY="answer-sheet:"+SPEC.date+":"+SPEC.title;
const form=()=>document.querySelectorAll("input,textarea");
function state(){{const s={{}};form().forEach(e=>{{if(e.type==="radio"){{if(e.checked)s[e.name]=e.value}}else if(e.value.trim())s[e.name]=e.value}});return s}}
function refresh(){{const s=state();let done=0;SPEC.questions.forEach(q=>{{const ok=q.id in s||(q.id+"__note") in s;document.getElementById(q.id).classList.toggle("done",ok);done+=ok}});
document.getElementById("count").textContent=done+" of "+SPEC.questions.length+" answered";localStorage.setItem(KEY,JSON.stringify(s))}}
function markdown(){{const s=state();const out=["## "+SPEC.title+" (answered in the answer sheet)"];
SPEC.questions.forEach(q=>{{const o=q.id in s?q.options[+s[q.id]]:null;const note=s[q.id+"__note"];if(!o&&!note)return;
out.push("","### "+q.title);if(o)out.push("Answer: "+o.label+(o.recommended?" (the recommended option)":""));if(note)out.push("Note: "+note.trim())}});return out.join("\\n")}}
window.answerSheet=()=>({{date:SPEC.date,state:state(),markdown:markdown()}});
const saved=JSON.parse(localStorage.getItem(KEY)||"{{}}");form().forEach(e=>{{if(e.type==="radio")e.checked=saved[e.name]===e.value;else if(saved[e.name])e.value=saved[e.name]}});
document.addEventListener("input",refresh);refresh();
document.querySelectorAll("figure img").forEach(i=>i.onclick=()=>i.classList.toggle("big"));
document.getElementById("copy").onclick=async()=>{{await navigator.clipboard.writeText(markdown());document.getElementById("count").textContent="Copied. Paste it into the chat."}};
document.getElementById("save").onclick=async()=>{{try{{const r=await fetch("/save",{{method:"POST",headers:{{"Content-Type":"application/json"}},body:JSON.stringify({{date:SPEC.date,markdown:markdown()}})}});
document.getElementById("count").textContent=r.ok?"Saved to "+await r.text()+". Tell the agent you're done.":"Save failed ("+r.status+"). Use Copy answers instead."}}
catch(e){{document.getElementById("count").textContent="The save server isn't running. Use Copy answers instead."}}}};
</script></body></html>"""

if __name__ == "__main__":
    if len(sys.argv) >= 3 and sys.argv[1] == "build":
        build(sys.argv[2])
    elif len(sys.argv) >= 4 and sys.argv[1] == "serve":
        serve(sys.argv[2], sys.argv[3], int(sys.argv[4]) if len(sys.argv) > 4 else 8765)
    else:
        sys.exit(__doc__)
