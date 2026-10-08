# Phase: Responsive

## Tier

T2 — Quality Gate

## Inputs

- Stack profile (UI framework)
- Overlay checks (project-specific responsive requirements)
- Scope: file list or "all"

## Checks

### 1. Hardcoded Widths

- Scan for `width:` constraints with literal values > 200 logical pixels
- Exclude: icon sizes, tap targets, design system constants
- **Critical if**: Hardcoded width > 300 that would overflow on 375pt screen (iPhone SE)
- **High if**: Hardcoded width 200-300 in a layout that doesn't scroll horizontally
- **Method**: Grep for `width:` with numeric literals, check context

### 2. Horizontal Overflow Patterns

- Scan for `Row` widgets without `Expanded`, `Flexible`, or `SingleChildScrollView` wrapping
- Check for multiple `Text` widgets in a `Row` where content could exceed screen width
- **Critical if**: Visible content clipped/invisible on 375pt width
- **Medium if**: Row without flex children where overflow is theoretically possible
- **Method**: Read widget files, check Row children for flex wrappers

### 3. Text Scaling Tolerance

- Check if the app handles text scaling from `MediaQuery.textScalerOf(context)` up to 2.0x (`textScaleFactorOf` is deprecated)
- Scan for fixed-height containers wrapping `Text` widgets
- **Medium if**: Fixed-height container around text that would clip at 2.0x scale
- **Method**: Check for fixed height + Text combinations

### 4. Missing Breakpoint Usage

- Scan layout pages for responsive patterns
- **Medium if**: Full-screen layout with no breakpoint/MediaQuery adaptation
- Stack-aware: check for `ShadBreakpoints` (shadcn_ui), `LayoutBuilder` (Material), `MediaQuery` (generic)
- **Method**: Read page files, check for responsive pattern usage

### 5. Touch Target Sizing

- Scan interactive elements for explicit size constraints
- **High if**: Touch target < 44x44 on any viewport size (48x48 dp on Android)
- Note: overlaps with Accessibility phase but here we check across breakpoints
- **Method**: Check interactive element sizes

### 6. Scrollability

- Check screens with multiple sections for scroll wrapper
- **High if**: Screen content likely exceeds viewport height on small devices without scroll
- **Method**: Read page files, check for ScrollView or equivalent wrapper

### 7. Overlay Checks

- Read the matched overlay's Responsive section
- Execute each additional check

## Severity Rules Summary

| Check                        | Critical | High | Medium | Low |
| ---------------------------- | -------- | ---- | ------ | --- |
| Overflow on 375pt            | X        |      |        |     |
| Hardcoded width > 300        | X        |      |        |     |
| Hardcoded width 200-300      |          | X    |        |     |
| No scroll on long content    |          | X    |        |     |
| Touch target < 44pt          |          | X    |        |     |
| Text scaling clip            |          |      | X      |     |
| No breakpoint usage          |          |      | X      |     |
| Suboptimal layout adaptation |          |      |        | X   |

## Output Format

```text
file:line | severity | check_name | description | auto_fixable: yes/no | fix_action: {description}
```
