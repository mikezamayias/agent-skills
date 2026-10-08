# Worst-case catalog

Realistic values that break UI, grouped by the kind of value a screen renders.
Pick only the rows that match fields in the step 1 surface table.
Every value is something a real user, import, or API client can produce.
Use `example.com`, `example.org`, or `.test` domains so a fixture never points at a real inbox or site.
The names are illustrative patterns, not real people.

Sections: names, identifiers, labels and copy, free text, numbers and money, collections, time, media, states, environment, grapheme handling.

## Names

| Value                                               | What it tends to break                                                                 |
| --------------------------------------------------- | -------------------------------------------------------------------------------------- |
| `Aleksandra Wiśniewska-Kowalczyk`                   | Long, hyphenated, diacritics, wraps to two lines at the hyphen                         |
| `Παναγιώτα Χατζηγεωργίου-Κωνσταντοπούλου`           | Long Greek compound surname, overflows single-line rows                                |
| `Christopher Alexander Montgomery III`              | Suffix, naive first-plus-last initials give `CI`                                       |
| `Jo` and `J`                                        | Name column mostly empty, one-letter initials, tiny tap target if the name is the link |
| `Ólafur Darri Ólafsson`                             | Accented capital, sorting and initials                                                 |
| `Đặng Thị Ngọc Hân`                                 | Stacked Vietnamese diacritics, clipped by tight line height plus clipping              |
| `王秀英`                                            | CJK with no spaces, "first and last word" initials find one word                       |
| `نور الهدى عبد الرحمن`                              | RTL, icons and punctuation land on the wrong side                                      |
| `Seán O'Brien-Ó Súilleabháin`                       | Apostrophe, escaping, search                                                           |
| `María José de la Cruz y Fernández`                 | Lowercase particles, initials and last-name sorting                                    |
| `dana`                                              | All lowercase, initials must still be uppercase                                        |
| `🦊 Fox` and `👩🏽‍💻 Priya`                             | Emoji first, index 0 returns half a character, ZWJ sequence counts as 7+ code units    |
| `Sam   Lee` padded with leading and trailing spaces | Leading, trailing and repeated spaces, empty words in initials                         |
| Missing name, email only                            | The fallback chain itself                                                              |
| `Άννα` shown in an all-caps label                   | Greek all-caps drops the accent (`ΑΝΝΑ`), generic `toUpperCase()` keeps it (`ΆΝΝΑ`)    |

## Identifiers, emails, URLs

These strings have no spaces, so text layout has nowhere to wrap them.

| Value                                                              | What it tends to break                                                |
| ------------------------------------------------------------------ | --------------------------------------------------------------------- |
| `bartholomew.fitzgerald@northwind-industries-holdings.example.com` | Pushes every sibling off the row                                      |
| `a@b.co`                                                           | Layout that assumed a long email looks empty                          |
| `first.last+billing-notifications@example.com`                     | Validation that rejects `+`, end-truncation hides the meaningful part |
| `ops@sub.department.region.example.co.uk`                          | Domain extraction, two-part TLD                                       |
| A 120-character URL with a query string                            | Overflow, end-truncation hides what differs                           |
| `9f8e7d6c-5b4a-4c3d-8e2f-1a0b9c8d7e6f`                             | UUID, middle-truncation candidate                                     |
| `Q3 Board Deck - FINAL (revised) v12 [approved].pdf`               | End-truncation hides version and extension                            |
| `IMG_20250914_183022_HDR_portrait_edited_edited.HEIC`              | Unbreakable camera file name                                          |
| `@a` and a 30-character handle                                     | Handle extremes                                                       |

## Labels and copy from data or translation

| Value                                                     | What it tends to break                        |
| --------------------------------------------------------- | --------------------------------------------- |
| `Senior Product Design Engineer, Platform Infrastructure` | Secondary slot wraps to three lines           |
| `Invitation expired 12 days ago`                          | Status badge wraps or squeezes the name       |
| `Benachrichtigungseinstellungen`                          | German compound with no break point           |
| `Ρυθμίσεις απορρήτου και ασφάλειας`                       | Greek runs much longer than the English label |
| `Paramètres de confidentialité et de sécurité`            | French expansion of a short English label     |
| Twelve tags on one item                                   | Tag row becomes a wall, needs a `+8` overflow |
| One 45-character tag                                      | A single chip wider than its container        |
| Empty string or whitespace-only title                     | Collapsed heading, zero-height row            |
| `<script>alert(1)</script>`, `&amp;`, `**bold**`          | Must render as literal text                   |
| A newline inside a single-line field                      | Doubles row height or silently disappears     |

## Free text

| Value                                 | What it tends to break                                     |
| ------------------------------------- | ---------------------------------------------------------- |
| A 5,000-word post or description      | Clamping, "show more", editor growth, scroll performance   |
| A single emoji as the whole entry     | Previews and titles derived from the first line            |
| Only newlines or spaces               | "Empty" checks that test length instead of trimmed content |
| A pasted block with tabs and Markdown | Escaping and preview rendering                             |

## Numbers and money

| Value                                                  | What it tends to break                                                             |
| ------------------------------------------------------ | ---------------------------------------------------------------------------------- |
| `0`                                                    | "0 members", empty bars, division by zero in percentages                           |
| `1`                                                    | "1 members", "1 days ago"                                                          |
| `1284`                                                 | Needs a locale grouping separator                                                  |
| `1000000`                                              | Badge width, consider a compact form where precision does not matter               |
| `12345678.9` as currency                               | Overflows totals columns, `1.284,50 €` in `el` and `de` versus `€1,284.50` in `en` |
| `-42.5`                                                | Sign, colour logic, accounting parentheses                                         |
| `0.1 + 0.2`                                            | `0.30000000000000004` rendered raw                                                 |
| `142%` and `-3%`                                       | Progress bars and gauges past their bounds                                         |
| `null`, `NaN`, `Infinity`                              | Rendered literally, or `"null"` from string interpolation                          |
| A live value crossing a digit boundary (`99` to `100`) | Width jump without tabular figures                                                 |

## Collections

| Value                                   | What it tends to break                                |
| --------------------------------------- | ----------------------------------------------------- |
| 0 items                                 | Whether an empty state exists at all                  |
| 1 item                                  | Grids that look broken with one card, "1 of 1"        |
| Exactly page size, and page size plus 1 | Off-by-one copy, an empty second page                 |
| 1,000+ items unpaginated                | Scroll performance, memory, "Showing 40 of 1,284"     |
| One item ten times taller than the rest | Grid rows stretching to the tallest                   |
| Items with identical names              | Lists where the name is the only distinguishing field |

## Time

| Value                                                  | What it tends to break                                                  |
| ------------------------------------------------------ | ----------------------------------------------------------------------- |
| Now                                                    | "0 seconds ago" instead of "just now"                                   |
| 12 days, 11 months, 3 years ago                        | Relative-time thresholds, switch to an absolute date after about a week |
| A future date                                          | "-3 days ago"                                                           |
| `1970-01-01`                                           | A zero timestamp shown as a real date                                   |
| `2026-10-25T03:30:00+03:00` (Europe/Athens DST change) | Off-by-one-day and duplicated or missing hours                          |
| A Greek date in a sentence                             | Month genitive (`3 Μαρτίου`), hand-built strings get it wrong           |
| A duration of 1,284 hours                              | Never rolls up to days                                                  |

## Media

| Value                              | What it tends to break                                  |
| ---------------------------------- | ------------------------------------------------------- |
| Avatar URL that 404s or times out  | Broken-image icon instead of the initials fallback      |
| No avatar at all                   | The fallback's size and colour parity with real avatars |
| 4000x200 and 200x4000 images       | Distortion without cover-fit, card height blowout       |
| Transparent dark logo in dark mode | Invisible on the background                             |
| Slow image                         | Layout shift without a fixed size or aspect ratio       |

## States

| Value                        | What it tends to break                                  |
| ---------------------------- | ------------------------------------------------------- |
| Loading longer than 2 s      | Skeleton that does not match the final layout           |
| API or sync error            | No error state, or a raw exception message on screen    |
| Offline, then partial sync   | Mixed fresh and stale rows, misaligned optional fields  |
| Every enum value in one list | Badge widths vary across rows                           |
| No permission                | Disabled actions change row layout                      |
| The current user in the list | "You" labels, actions that should not apply to yourself |

## Environment

Not data, but checked the same way after loading the worst-case fixture.

| Condition                                                                               | What it tends to break                              |
| --------------------------------------------------------------------------------------- | --------------------------------------------------- |
| Narrowest width (320 logical px, pt, or CSS px)                                         | Every overflow at once                              |
| Component reused in a narrow column, sheet or menu bar popover                          | Designs made for full width                         |
| Widest layout (tablet, desktop, 2560 px)                                                | Line lengths too long, content stranded on one side |
| Text scale 2.0 on Android, about 3.1 at the largest iOS accessibility size, 200% on web | Fixed heights clip growing text                     |
| Landscape phone with the keyboard open                                                  | Bottom overflow, hidden submit button               |
| Dark mode                                                                               | Hard-coded colours, invisible borders and logos     |
| RTL                                                                                     | Icons, chevrons, padding and trailing action order  |
| Touch only                                                                              | Hover-only actions unreachable                      |

## Grapheme handling

Initials, truncation and "first character" logic must work on user-perceived characters, not code units.

- Dart: `string.characters.first` from `package:characters`, which Flutter already depends on.
- JavaScript: `Intl.Segmenter` with `granularity: 'grapheme'`.
- Swift: `String` is grapheme-based already, so `name.first` is safe, but `utf16.count` limits are not.
