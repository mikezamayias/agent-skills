---
name: figma-review-loop
description: >-
  Run a Figma design review round: read comments via the REST API, record rulings, redesign frames and sweep instances. Use when asked about Figma comments ("are all Figma comments resolved?") or at session start on a project with Figma. Also use after a ruling that changes a screen, or before calling a design pass done.
metadata:
  provenance: local
---

# Figma review loop

The Figma MCP server can read and edit the canvas but cannot read comments, so comments go unread unless something fetches them over the REST API.
A comment is the reviewer's feedback, and its thread is the record of what was asked.
Resolve it, never delete it.

Load the Figma plugin's `figma-use` skill before any `use_figma` call.
This skill covers the review loop around it.

## Files

- `scripts/figma_comments.py <file-key> [--all] [--json]` lists comment threads, open by default and oldest first, with the frame name and node ID each is pinned to, plus replies.
- `scripts/figma_comments.py <file-key> --render <out-dir> <node-id>...` renders frames as 2x JPEGs for review.

The file key is the part of the file URL after `/design/`.

## Token

A personal access token with `file_comments:read` and `file_content:read` scopes.
The script reads it from `$FIGMA_TOKEN` or the macOS Keychain item `figma-pat`, overridable with `$FIGMA_KEYCHAIN_SERVICE`.
If there is none, tell the user where to create it (Figma, Settings, Security, Personal access tokens) and to store it with `security add-generic-password -s figma-pat -a "$USER" -w`, which prompts for the value.
Never echo it, put it in a command argument, or log it.
For ad hoc `curl`, pass the header through stdin:

```bash
printf 'X-Figma-Token: %s\n' "$(security find-generic-password -s figma-pat -w)" | curl -sS -H @- https://api.figma.com/v1/files/<key>/comments
```

A personal access token cannot resolve comments.
The decision-maker resolves them in Figma, and the report lists which ones are ready.

## The loop

1. **Fetch.** List the open threads.
   At session start, compare their dates with the decision log, because unread comments are unrecorded rulings.
2. **Classify each thread:**
   - **Directive** ("remove X", "add Y"): record it as a ruling (see `decision-sweep`), then redesign.
   - **Question** ("what happens when this list is empty?"): answer it where it was asked.
     If a chat answer does not land, draw the answer in the file next to the frame, as a small annotated flow on the prototype page, and point to it.
   - **Needs a decision:** put it on an answer sheet (see `answer-sheet`) with the rendered frame as the image.
3. **Redesign.** Edit the frames, keeping disjoint pages per helper agent if you delegate.
   Recording a ruling in documents is not the same as changing the design, so do both in the same round.
4. **Sweep every instance.** When anything is wrong with a component, such as a misaligned element, a clipped label, or a wrong token, find every instance across the file and check each one programmatically.
   Fix it at the main component when the source is wrong.
   Spot-checking screenshots misses systematic defects.
   Make sure a sweep only touches the nodes it is meant to, because similar-looking layers in other components get caught.
5. **Design for real data.** Check lists at 0, 1, and many items, long names, and overflow.
   Remove anything that only matters to the system and not to the user.
6. **Render and review.** Render the changed frames to JPEG and look at them before reporting.
   Some model APIs reject large PNG exports, so use JPEG.
7. **Wire the prototype** if the file has one: new screens get their connections, and existing flows still start.
8. **Report** per thread:
   - what was asked
   - what changed, split into documents and design
   - whether it is ready for the decision-maker to resolve
     Put the ones ready to resolve in one list, and never say "resolved" for a thread the decision-maker has not resolved.

## Figma quirks

- Prototype interactions: there is no long-press trigger, and drag triggers on a swap are rejected, so use a press or tap trigger instead.
- Figma auto-creates flows ("Flow N") when you add connections, so rename or remove them.
- Gradient stops bound to variables can lose their alpha.
- Large image renders can time out, so render in batches or in the background.
- A render can come back blank below a large image fill.
  Re-render before assuming the design is broken.
- A resumed helper must check what already exists before drawing, or it duplicates frames.
