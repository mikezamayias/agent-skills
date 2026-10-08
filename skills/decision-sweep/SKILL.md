---
name: decision-sweep
description: >-
  Keep project documents true to decisions: log each ruling once, update every dependent file, run checks and commit. Use when the user answers questions, rules on a design or policy, or says "keep the latest notes as truth". Also use at session start to catch new answers, and when documents contradict each other.
metadata:
  provenance: local
---

# Decision sweep

A decision that lives only in chat disappears at the next context compaction.
A decision recorded in one file but restated in five others goes stale in four of them the next time it changes.
This skill keeps one owner per fact and a log of rulings that wins every conflict, and runs the same loop after every ruling.

## Structure the project needs

Set these up once, in a new project or when adopting the skill in an existing one, and record them in the project's `AGENTS.md`.

1. **Precedence order.** Write down which source wins a conflict, for example:
   - the decision-maker's answer files
   - the design file's comments
   - the decision log
   - owner documents
   - everything else
     Newer beats older within the same level.
2. **Decision log** (`DECISIONS.md` or similar).
   It holds one section per round, headed with the date and the topic, and one heading per ruling in plain words.
   Each ruling says what was decided, why, and who decided when.
   A later ruling that reverses an earlier one says so and links back.
3. **Owner table.** Each subject (schema, screens, notifications, privacy, costs) has exactly one owner file that defines its facts.
   Every other file links to the owner instead of restating it.
4. **Answer files.** The decision-maker's raw answers, one file per day (see the `answer-sheet` skill).
   Agents never edit them.
5. **Checks.** A linter for broken links and naming rules, plus any schema, string, or data checks.
   A red check means the edit is wrong.

In an existing project, do not restructure everything at once.
Start with the log and the precedence order, and move facts to owners as the sweeps touch them.

## Session start

1. Compare the modification time of every answer file and notes file with the decision log's last change.
   Anything newer holds unrecorded answers, so read it first.
2. Check for uncommitted work.
   Report changes you did not make, and never reset or stash them.
3. Read open design-review comments if the project has a design file (see `figma-review-loop`).
4. Read the decision log's latest sections before acting on any older document.

## The loop, for every ruling

1. **Record.** The main agent alone writes the ruling into the decision log.
   Quote the decision-maker's words when they are short.
2. **Find the dependents.** Search for the subject's terms, identifiers, strings, numbers, and screen names across the repository.
   List every file that restates, implements, tests, or displays the old behaviour, including specs, schemas, copy and translation files, policies, task lists, and designs.
3. **Sweep.** Update each dependent, or delegate the update to a helper agent with this brief:
   - the rulings, verbatim
   - the file list, split so no two helpers share a file
   - no commits
   - the decision log and answer files are off limits
   - report every choice the ruling did not settle
     Run large sweeps in the background and keep the main thread free for the decision-maker.
4. **Fix stale facts without asking.** A fact that contradicts a newer ruling is wrong, so correct it and note it in the report.
   Ask only when two rulings genuinely conflict.
5. **Check.** Run every project check against the final state of the files.
6. **Surface the open choices.** Every product choice a helper made that no ruling settled goes to the decision-maker on the next answer sheet, with a recommendation.
   None stands by default.
7. **Re-open signed text.** If the ruling makes a signed-off sentence untrue, such as a policy line or a store description, mark it for re-sign-off and show exactly what changed (see `promise-audit`).
8. **Design parity.** If the ruling changes a screen, update the design in the same round.
   Report separately what changed in the documents and what changed in the design.
9. **Commit.** Read the staged diff, then commit with `&&` after the checks, so a failed step never yields a commit that claims the change.
   Push only under the project's recorded push rule.

## Report shape

End each round with:

- the rulings recorded, in plain words
- the files changed, grouped by subject
- stale facts corrected
- open choices, which also go on the next answer sheet
- what the checks ran and their result
- what is recorded in documents but not yet in design or code

Never refer to a ruling by a code alone.

## Pitfalls

- Two helpers editing the same file at once break the checks.
  Assign disjoint files.
- Renaming a heading breaks `[[FILE#Heading]]`-style links.
  Search for links to it before renaming.
- Helpers tend to "helpfully" settle open product questions.
  The brief must forbid it, and the report must list any that slipped through.
- Sweeps surface older contradictions nobody asked about.
  Fix the ones that contradict a ruling, and list the rest instead of widening the round.
- Timestamps inside transcript or export files can come from metadata written later.
  Trust file contents and the log's dates over them.
