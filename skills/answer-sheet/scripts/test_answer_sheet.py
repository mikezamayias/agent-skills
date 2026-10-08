#!/usr/bin/env python3
"""Smallest check for answer_sheet.py: build a page, save twice, expect one block."""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import threading
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import answer_sheet  # noqa: E402

tmp = tempfile.mkdtemp()
try:
    questions, answers = os.path.join(tmp, "questions"), os.path.join(tmp, "answers")
    os.makedirs(questions)
    spec = os.path.join(questions, "2026-01-15.json")
    shutil.copy(os.path.join(HERE, "example.json"), spec)
    subprocess.run([sys.executable, os.path.join(HERE, "answer_sheet.py"), "build", spec], check=True, capture_output=True)
    assert os.path.exists(os.path.join(questions, "2026-01-15.html")), "page not built"

    answer_sheet.Handler.questions, answer_sheet.Handler.answers = questions, answers
    server = answer_sheet.ThreadingHTTPServer(("127.0.0.1", 0), answer_sheet.Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    url = f"http://127.0.0.1:{server.server_port}/save"

    def save(markdown):
        body = json.dumps({"date": "2026-01-15", "markdown": markdown}).encode()
        urllib.request.urlopen(urllib.request.Request(url, body, {"Content-Type": "application/json"}))

    save("## Sheet (answered in the answer sheet)\n\n### Q\nAnswer: first")
    save("## Sheet (answered in the answer sheet)\n\n### Q\nAnswer: second")
    text = open(os.path.join(answers, "2026-01-15.md")).read()
    assert text.count("## Sheet") == 1 and "second" in text and "first" not in text, text
    server.shutdown()
    print("ok")
finally:
    shutil.rmtree(tmp)
