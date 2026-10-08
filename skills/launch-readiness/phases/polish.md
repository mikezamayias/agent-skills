# Phase: Polish

## Tier

T3 — Polish & Verify

## Inputs

- Stack profile (UI framework)
- CLAUDE.md rules (theme constants, naming conventions)
- Overlay checks (project-specific design system rules)
- Scope: file list or "all"

## Checks

### 1. Raw Color Values

- Scan presentation layer for hardcoded color values:
  - `Color(0x...)`, `Color.fromRGBO(...)`, `Color.fromARGB(...)`
  - Hex color patterns in string form
- Exclude: test files, domain layer
- **High if**: Hardcoded color in presentation layer (design system bypass)
- **auto_fixable**: yes (if design system color mapping is clear from CLAUDE.md)
- **fix_action**: Replace with the design system's color accessor
- **Method**: Grep for Color() constructor patterns in presentation files

### 2. Raw Spacing Values

- Scan for literal spacing values (`SizedBox(height: 16)`, `EdgeInsets.all(8)`, `Padding(padding: EdgeInsets.only(...))`)
- Check CLAUDE.md for the project's spacing constants (e.g., `Spacing.*`)
- **Medium if**: Raw numeric spacing where design system constants exist
- **auto_fixable**: yes (if spacing constants map clearly)
- **fix_action**: Replace with design system constant (e.g., `Spacing.md`)
- **Method**: Grep for SizedBox/EdgeInsets/Padding with numeric literals

### 3. Raw Typography

- Scan for inline `TextStyle()` construction instead of typography system usage
- Check CLAUDE.md for the design system's typography accessor
- **Medium if**: Inline TextStyle where typography system exists
- **auto_fixable**: partially (style mapping may not be 1:1)
- **Method**: Grep for TextStyle() in presentation files

### 4. TODO/FIXME/HACK Comments

- Scan for TODO, FIXME, HACK, XXX comments
- **Medium if**: TODO/FIXME present (tech debt shipping to production)
- **Low if**: HACK/XXX present (known workaround)
- **Method**: Grep for comment patterns

### 5. Animation Convention Violations

- Check CLAUDE.md for animation rules (e.g., "use the shared motion durations and curves")
- Verify animations follow the documented conventions
- **Medium if**: Animation pattern violates documented convention
- **Method**: Read animation chains, compare with CLAUDE.md rules

### 6. Design System Compliance (stack-aware)

- If CLAUDE.md specifies a card component: verify all cards use it
- If CLAUDE.md specifies icon set: verify no other icon packages used
- If CLAUDE.md bans imports: verify no banned imports in presentation layer
- **High if**: Banned import present
- **Medium if**: Non-standard card/component used
- **auto_fixable**: partially (import replacement is straightforward)
- **Method**: Grep for patterns specified in CLAUDE.md

### 7. Overlay Checks

- Read the matched overlay's Polish section
- Execute each additional check (e.g., "one shared card component, no ad-hoc bordered containers")

## Severity Rules Summary

| Check                  | Critical | High | Medium | Low |
| ---------------------- | -------- | ---- | ------ | --- |
| Hardcoded colors       |          | X    |        |     |
| Banned imports         |          | X    |        |     |
| Raw spacing values     |          |      | X      |     |
| Raw typography         |          |      | X      |     |
| TODO/FIXME             |          |      | X      |     |
| Animation convention   |          |      | X      |     |
| Non-standard component |          |      | X      |     |
| HACK/XXX comments      |          |      |        | X   |
| Minor alignment nits   |          |      |        | X   |

## Output Format

```text
file:line | severity | check_name | description | auto_fixable: yes/no | fix_action: {description}
```
