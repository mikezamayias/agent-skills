# Launch Readiness Report — {date}

## Verdict: {SHIP / HOLD / BLOCK}

**Project**: {project name}
**Scope**: {full codebase / changed files (N files)}
**Overlay**: {overlay name or "none"}

## Stack Profile

```text
- state: {detected}
- analytics: {detected}
- crash: {detected}
- subs: {detected}
- ui: {detected}
- nav: {detected}
- di: {detected}
- l10n: {detected}
- test_runner: {detected}
```

## Scorecard

| Phase            | Critical | High  | Medium | Low   | Auto-fixable |
| ---------------- | -------- | ----- | ------ | ----- | ------------ |
| Testing          | -        | -     | -      | -     | -            |
| Security         | -        | -     | -      | -     | -            |
| Store Compliance | -        | -     | -      | -     | -            |
| Hardening        | -        | -     | -      | -     | -            |
| Accessibility    | -        | -     | -      | -     | -            |
| Responsive       | -        | -     | -      | -     | -            |
| Localization     | -        | -     | -      | -     | -            |
| Analytics        | -        | -     | -      | -     | -            |
| Performance      | -        | -     | -      | -     | -            |
| Polish           | -        | -     | -      | -     | -            |
| **TOTAL**        | **-**    | **-** | **-**  | **-** | **-**        |

## Verdict Logic

- BLOCK: 1+ critical findings
- HOLD: 0 criticals, 3+ unacknowledged highs
- SHIP: 0 criticals, all highs acknowledged or 0 highs

---

## Tier 1 — Ship Blockers

### Testing

{findings or "No issues found."}

### Security

{findings or "No issues found."}

### Store Compliance

{findings or "No issues found."}

{If T1 blocked, note: "Tier 2 and 3 not executed — fix T1 criticals first."}

---

## Tier 2 — Quality Gates

### Hardening

{findings or "No issues found."}

### Accessibility

{findings or "No issues found."}

### Responsive

{findings or "No issues found."}

### Localization

{findings or "No issues found."}

{If T2 blocked, note: "Tier 3 not executed — fix T2 criticals first."}

---

## Tier 3 — Polish & Verification

### Analytics

{findings or "No issues found."}

### Performance

{findings or "No issues found."}

### Polish

{findings or "No issues found."}

---

## Auto-Fix Available

{N} issues can be fixed automatically:

| Phase   | Count | Summary             |
| ------- | ----- | ------------------- |
| {phase} | {n}   | {brief description} |

**Fix now? [y/n]**

---

## New Patterns Discovered

{N} checks not in current phase files:

1. **{phase}**: {description}
2. **{phase}**: {description}

**Update phase files? [y/n]**
