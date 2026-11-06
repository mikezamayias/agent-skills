---
name: locale-expert-review
description: >-
  Reviews a shipped app in every language the way a native user sees it, with one expert agent per language. Use before a release, after adding languages, or when a native speaker reports a translation or layout problem. Covers strings on every platform, store listings and rendered screens, including script, digits and direction.
metadata:
  provenance: local
---

# Locale expert review

A translation can pass every script check and still read badly to a native user.
The worst defects are often not in the text at all: a font with no glyphs for the script, a number printed without the locale's digits, demo data that bypasses localization, or a renderer that ignores right-to-left.
This skill puts one native-speaker expert per language in front of everything a user of that language sees, side by side with the source, and with the rendered screens.

Run the cheap plain checks first (completeness, placeholders, length, glossary), so the experts spend their attention on meaning, grammar and rendering.

## Step 1: Inventory what a user reads

List every surface, per platform:

- app strings: Apple String Catalogs (`.xcstrings`), Android `res/values-*/strings.xml` (strings, plurals, arrays), Flutter ARB, web message files
- store texts: App Store name, subtitle, description, keywords, promotional text, and the Google Play title, short and full description
- rendered screens in each language: the main screen, a detail screen, a list or filtered view, a share image, a watch or widget screen, and one store screenshot slide

Rendered screens are not optional.
A reviewer who sees only strings cannot catch letters drawn apart, clipped labels, two digit systems on one screen, or a mirrored layout that stayed left to right.

## Step 2: Render the screens in each language

Render through the app's own code with the language and region set, never by pasting translations into a mock.
Include every script family you ship: right-to-left (Arabic, Hebrew, Urdu), joined scripts (Arabic, Urdu Nastaliq), Indic scripts, CJK, and languages with their own digits (Arabic, Bengali, Marathi, Persian, Nepali, Burmese).
An offscreen renderer (a snapshot test, an image renderer, a headless browser) often defaults to left to right and to the host's locale, so set both explicitly and check one right-to-left render by eye before trusting the rest.

## Step 3: Build one packet per language

`scripts/build_packets.py config.json out_dir` writes one Markdown packet per language: every string as a row with its key, plural case, source text, translation and the developer's comment, then the store texts beside their source, then the paths of the rendered screens.
It reads Apple String Catalogs, Android resources from one or more modules, and flat or nested JSON message files such as Flutter ARB or web locale files, with the standard library only.
For another format, convert it to one of these or add a reader to the script.
The config format is in the script's docstring.
Keep the config in the project repository so the next review reuses it.
`scripts/test_build_packets.py` is the script's self-test.

A plural case the source lacks (Arabic's dual, Polish's few) is its own row beside the source's "other" text, and a language with only "other" (Japanese, Chinese) gets one row, so a reviewer never sees a false "missing".
A translated list shorter than the source shows its missing items as MISSING.

## Step 4: One expert per language

Give each language to its own agent on the strongest model at high reasoning effort.
Use the prompt in `references/expert-prompt.md`.
It casts the agent as a native-speaker localization reviewer, tells it to read the whole packet and open every screen, lists what is already fixed so it is not reported again, and weights the checks: meaning, grammar with real numbers, short labels and abbreviations, script and typography, consistency, store texts, screens.
It returns a structured list of findings with severity, key, current text, back-translation and fix.

Run the agents in parallel batches.
State the expected token cost before starting: a packet of about 1,300 strings is about 60,000 input tokens per language, plus the screens, and a full review with re-reads and reasoning came to about 165,000 tokens per language.
At about ten agents at a time, 46 languages took about 25 minutes.

## Step 5: Group findings across languages

Before fixing anything language by language, group the findings by key and by kind across all languages.
A problem reported in many languages is usually not a translation problem:

- the same key mistranslated the same way in several languages means the source text is ambiguous, so fix the source first, then every translation
- the same source-language word left on screen in most languages means the code builds that text itself instead of using a localized string
- the same markup or placeholder showing literally means a format the platform does not process in that position

Fix those once, at the root, and only then hand the rest out per language.
When you drop findings that a root fix already covers, select them by their problem statement, never by text that appears in a key: one key can name several strings, and a filter on key text silently drops unrelated findings.
Count what each filter dropped and read the list.

## Step 6: Verify before fixing

Treat every finding as a claim.
For blocker and major findings that change meaning, have a second, independent agent on the same language judge the finding without seeing the first agent's reasoning, and keep it only if both agree.
Ask that agent for exact edits, not prose: the target file kind, the exact key and plural case, a text to find inside the current translation and its replacement.
Apply them with a script that refuses an edit whose text is not found exactly once or that changes the placeholders, and that escapes text for the target format.
Then run the plain checks again, and update the glossary where a verified edit changed a glossary term on every platform.
Check screen findings against the screenshot yourself.
Fix mechanical findings (punctuation, digits, a dropped word, an inconsistent term with an agreed glossary entry) directly.
Put meaning and register changes to a human native speaker or the decision-maker, never silently.

## Traps the experts keep finding

- **Monospaced fonts and joined scripts:** a monospaced system font usually has no Arabic letters, so its fallback draws each letter in a fixed cell and words fall apart, and letter spacing pulls joined letters apart in any font.
  Switch monospaced and tracked styles to the proportional system font, without tracking, when the shown language is written in Arabic script.
- **Numbers built by string interpolation:** `"\(value)"` or `"$count"` prints Western digits next to locale-formatted numbers.
  Format every user-visible number with the locale, including axis labels and counts.
- **Digits typed into translations:** "7 days" translated with a literal 7 keeps Western digits where the locale uses its own.
  Prefer a placeholder that the code formats.
- **Demo and sample data:** text stored preformatted in English ("$250.04 of $250.00") shows English in every language's screenshots.
  Store values as numbers and format at display time.
- **Unit abbreviations:** "d" and "h" style abbreviations are not standard in many languages.
  Prefer the platform's duration formatter, and have the expert check each abbreviation.
- **Numbers and grammar:** duals, counters, case after numerals and gender agreement break when a sentence is assembled around a number.
  Use the platform's plural and inflection support, not concatenation.
- **Inflection markup left in plural variants:** Apple's automatic grammar agreement markup (the `inflect: true` attribute on a bracketed phrase) is not processed everywhere a translation can carry it.
  A plural variant that already spells out each form can print it literally, so remove it from such variants and check a render.
- **Names built in code:** a combined or default name assembled in code ("All " + provider) skips localization on every platform that builds it.
  Build it from a localized format string.
- **Ambiguous source sentences:** a pronoun or a phrase like "show the accounts on that Mac" can attach two ways, and machine translation picks one.
  When several languages make the same mistake, rewrite the source.
- **Latin names in right-to-left text:** a product or account name at the start of a right-to-left sentence can flip the line's direction.
  Isolate embedded names with bidi isolates or the platform's equivalent.

## Output

- one line per language: the expert's overall judgment and the register it uses (formal or informal address)
- the findings, grouped by language and severity, each with key, current text, back-translation and fix, and whether it was verified
- the mechanical fixes applied, and the meaning changes waiting for a human
- the languages no human has reviewed, so the gap stays visible
