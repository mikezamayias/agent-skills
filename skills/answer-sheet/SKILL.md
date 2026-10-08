---
name: answer-sheet
description: >-
  Put open questions for the user on one self-contained HTML page, with answers saved to a dated Markdown file. Use when more than a handful of questions, decisions or sign-offs are waiting instead of a coded list in chat. Also use when the decision-maker cannot keep up with codes, or a review round needs screenshots per question.
metadata:
  provenance: local
---

# Answer sheet

A question in chat competes with everything else in the chat.
Long lists of coded questions become unreadable once the reader forgets what each code meant.
An answer sheet replaces the chat list with one page per round: every question carries its own background, the options and what each leads to, a recommendation, and a free-text box.
The page saves answers in the browser as the user goes and writes them to the repository on "Save answers".

## When to use it

- More than about five open questions, or any sentence-level sign-off.
- The questions span sessions, so the reader will not remember the earlier messages.
- A question needs a picture, such as a design frame, a chart, or a screenshot.

For one or two quick questions, ask in chat, with each code followed by its meaning.

## Files

- `scripts/answer_sheet.py` builds and serves the page. It uses only the Python standard library.
- `scripts/example.json` is a template question file.
- `scripts/test_answer_sheet.py` is the check. Run it after changing the script.

Pick two directories in the project, for example `questions/` and `answers/`, and record them in the project's `AGENTS.md` so every agent uses the same place.
The answers directory is the decision-maker's.
Agents read it and never edit it.

## Steps

1. Write `<questions-dir>/<YYYY-MM-DD>.json` in the format of `scripts/example.json`.
   Add a suffix (`-b`, `-c`) for a second sheet on the same day.
2. Build the page with `python3 <skill>/scripts/answer_sheet.py build <questions-dir>/<date>.json`.
3. Start the server once per session in the background with `python3 <skill>/scripts/answer_sheet.py serve <questions-dir> <answers-dir> [port]`.
   It binds to 127.0.0.1 only, on port 8765 by default.
4. Open `http://127.0.0.1:8765/<date>.html` in the in-app preview or the browser.
   In chat, say in one or two sentences what the sheet covers.
   Do not repeat the questions in chat.
5. When the user says they saved, read `<answers-dir>/<date>.md`, record each ruling where the project keeps decisions (see the `decision-sweep` skill), act on it, and commit the answer file with the changes.
6. If the answers raise new questions, they go on the next sheet.

## Writing a question

Each question must stand on its own for a reader who has forgotten everything said before.

- **Title:** the decision in plain words, as a question or a short instruction.
  Never a code.
- **Context:** paragraphs and bullets that start with a hyphen, with `**bold**` allowed.
  - Start from scratch: what exists today, what the problem is, and who it affects.
  - Explain every product name, acronym, and legal term the first time it appears.
  - State the harm the recommendation prevents, not only what it does.
  - When asking for a sign-off, quote the exact sentence or show exactly what changed.
- **Images:** optional, with `src` relative to the questions directory and a caption.
  Use JPEG. Some model APIs reject large PNG exports, and JPEG keeps the repository small.
- **Options:** 2 to 4, each with a label and a detail saying what happens next if it is chosen.
  Mark exactly one `"recommended": true`, unless you genuinely have no view.
  Every question also gets a free-text box, so there is no need for an "Other" option.
- Never ask the decision-maker to check a fact you can check yourself.
  Check it, then ask only the decision.
- Never ask about a concern the decision-maker has already dismissed.

## Behaviour to rely on

- Answers autosave in the browser, keyed by date and title, so a reload loses nothing.
- Save writes a block that starts `## <title> (answered in the answer sheet)`.
  A second Save of the same sheet replaces that block instead of appending a duplicate.
- The file may hold the user's own notes too.
  The server only touches its own block.
- If the server is down, "Copy answers" puts the same Markdown on the clipboard for pasting into chat.
- `window.answerSheet()` returns the current state, which is useful when driving the page from browser automation.

## Pitfalls

- Starting a second server on the same port fails.
  Check with `curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:8765/` before starting one.
- The rendered page escapes HTML.
  Only `**bold**` and bullets that start with a hyphen are formatted.
- Keep emoji out of sheets.
