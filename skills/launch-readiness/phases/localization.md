# Phase: Localization

## Tier

T2 — Quality Gate

## Inputs

- Stack profile (l10n system)
- Overlay checks (project-specific l10n scope)
- Scope: file list or "all"

## Checks

### Mode A: Localization Configured

Applies when stack profile detects `intl`, `easy_localization`, `slang`, or `l10n.yaml`.

#### A1. Strings Bypassing L10n

- Scan presentation layer for user-facing string literals not going through the l10n system
- User-facing = inside `Text()`, `label:`, `hintText:`, `semanticLabel:`, `title:`, button labels
- Exclude: debug strings, log messages, enum values, const keys
- **Critical if**: Regression — l10n is configured but strings bypass it in recently changed files
- **High if**: > 10% of user-facing strings are hardcoded
- **Medium if**: < 10% hardcoded (gradual migration acceptable)
- **Method**: Grep presentation files for string literals in UI contexts, cross-check with l10n keys

#### A2. Missing Translations

- Check for ARB/JSON files with missing keys compared to the primary locale
- **High if**: Keys present in primary locale but missing in supported locales
- **Method**: Compare key sets across locale files

#### A3. Key Naming Consistency

- Check l10n keys follow a consistent naming pattern
- **Low if**: Inconsistent naming (camelCase vs snake_case, no prefix convention)
- **Method**: Read locale files, check key patterns

### Mode B: No Localization Configured

Applies when no l10n system is detected.

#### B1. Hardcoded String Inventory

- Count all user-facing string literals in the presentation layer
- Emit a single advisory finding with the count
- **Medium**: "No localization configured — N user-facing strings found across M files"
- Do NOT generate a string catalog (that's a feature dev task, not a readiness check)
- **Method**: Grep presentation files for string literals in UI widget parameters

### Stack-Aware Detection

- `intl`: Look for `l10n.yaml`, `*.arb` files in `lib/l10n/`
- `easy_localization`: Look for `translations/` directory, `EasyLocalization` in widget tree
- `slang`: Look for `slang.yaml` or `i18n/` directory
- Manual: Look for custom `AppLocalizations` or string constant files

### Overlay Checks

- Read the matched overlay's Localization section
- May narrow scope (e.g., "presentation layer only, domain uses enums")

## Severity Rules Summary

### Mode A (l10n configured)

| Check                            | Critical | High | Medium | Low |
| -------------------------------- | -------- | ---- | ------ | --- |
| Strings bypass l10n (regression) | X        |      |        |     |
| > 10% hardcoded                  |          | X    |        |     |
| Missing translations             |          | X    |        |     |
| < 10% hardcoded                  |          |      | X      |     |
| Key naming inconsistency         |          |      |        | X   |

### Mode B (no l10n)

| Check                          | Critical | High | Medium | Low |
| ------------------------------ | -------- | ---- | ------ | --- |
| No l10n configured (inventory) |          |      | X      |     |

## Output Format

```text
file:line | severity | check_name | description | auto_fixable: no | fix_action: none
```

Note: Localization findings are not auto-fixable — they require design decisions about key naming, translation scope, and l10n system choice.
