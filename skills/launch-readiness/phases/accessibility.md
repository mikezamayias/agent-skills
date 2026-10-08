# Phase: Accessibility

## Tier

T2 — Quality Gate

## Inputs

- Stack profile (UI framework)
- Overlay checks (project-specific a11y requirements)
- Scope: file list or "all"

## Checks

### 1. Interactive Elements Without Semantics

- Scan for interactive widgets (`GestureDetector`, `InkWell`, custom press-feedback wrappers, custom tap handlers) that lack a `Semantics` wrapper
- Also check: `IconButton`, custom button widgets, anything with `onTap`/`onPressed`
- **Critical if**: Interactive navigation element (tab bar, back button, primary CTA) has no Semantics
- **High if**: Any other interactive element has no Semantics
- **auto_fixable**: yes
- **fix_action**: Wrap with `Semantics(label: '{inferred label}', button: true, onTap: {handler})`
- **Method**: Grep for onTap/onPressed, check parent tree for Semantics

### 2. Tap Targets Below Minimum

- Scan for interactive elements with explicit size constraints below 44x44 logical pixels
- Check: `SizedBox`, `Container` with width/height, `ConstrainedBox` wrapping interactive elements
- **High if**: Tap target explicitly constrained below 44pt in either dimension
- Platform minimums: 44x44 pt on iOS (`iOSTapTargetGuideline`) and 48x48 dp on Android (`androidTapTargetGuideline`).
- **High if**: Tap target explicitly constrained below 48dp on Android builds
- **Method**: Read widget files, check size constraints on interactive elements, and run `meetsGuideline(androidTapTargetGuideline)` / `meetsGuideline(iOSTapTargetGuideline)` in widget tests

### 3. Missing Semantic Labels on Icons

- Scan for `Icon()` widgets used as standalone informational elements (not decorative)
- Check for `semanticLabel` parameter
- **Medium if**: Informational icon without semanticLabel
- **Low if**: Decorative icon without semanticLabel (acceptable)
- **auto_fixable**: yes (for obvious cases)
- **fix_action**: Add `semanticLabel: '{icon description}'`
- **Method**: Grep for Icon() usage, check for semanticLabel parameter

### 4. Heading Hierarchy

- Scan screens for text elements that serve as headings
- Verify logical hierarchy (no jumping from h1 to h3)
- **Medium if**: Heading hierarchy gaps within a screen
- **Method**: Read page files, identify heading-style text widgets

### 5. Focus Traversal

- Check that custom interactive elements participate in focus traversal
- Verify no `ExcludeSemantics` or `excludeSemantics: true` on interactive elements
- **High if**: `excludeSemantics: true` on an interactive element
- **auto_fixable**: yes
- **fix_action**: Remove `excludeSemantics: true`
- **Method**: Grep for excludeSemantics

### 6. Stack-Aware Checks

- If `shadcn_ui`: Check `ShadTooltip` on icon-only buttons
- If Material: Check `Tooltip` on `IconButton`
- **Medium if**: Icon-only button without tooltip
- **Method**: Grep for icon button patterns per framework

### 7. Overlay Checks

- Read the matched overlay's Accessibility section
- Execute each additional check

## Severity Rules Summary

| Check                           | Critical | High | Medium | Low |
| ------------------------------- | -------- | ---- | ------ | --- |
| Navigation element no Semantics | X        |      |        |     |
| Other interactive no Semantics  |          | X    |        |     |
| Tap target < 44pt               |          | X    |        |     |
| excludeSemantics on interactive |          | X    |        |     |
| Icon without semanticLabel      |          |      | X      |     |
| Heading hierarchy gap           |          |      | X      |     |
| Decorative icon no label        |          |      |        | X   |

## Output Format

```text
file:line | severity | check_name | description | auto_fixable: yes/no | fix_action: {description}
```
