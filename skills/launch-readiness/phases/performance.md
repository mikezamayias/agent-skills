# Phase: Performance

## Tier

T3 — Polish & Verify

## Inputs

- Stack profile (state management, UI framework, animations)
- Overlay checks (project-specific performance rules)
- Scope: file list or "all"

## Checks

### 1. Expensive Operations in build()

- Scan `build()` methods for operations that should be in state management or initState:
  - API/HTTP calls
  - Heavy computation (sorting, filtering large lists, complex math)
  - File I/O
  - Database queries
- **High if**: API call or heavy computation inside build()
- **Method**: Read widget files, scan build() method bodies

### 2. Layout Property Animations

- Scan animation code for properties that cause layout reflow:
  - Animating `width`, `height`, `top`, `left`, `right`, `bottom`, `margin`, `padding`
  - These should use `transform` or `opacity` instead
- **Medium if**: Animation targets layout properties
- **Method**: Grep for animation definitions, check animated properties

### 3. Missing const Constructors

- Scan widget classes for constructors that could be `const` but aren't
- Focus on frequently instantiated widgets (list items, repeated UI elements)
- **Medium if**: Widget constructor could be const but isn't, and widget is used in a list/builder
- **Low if**: Widget constructor could be const but isn't, used infrequently
- **Method**: Read widget files, check constructor and field declarations

### 4. Image Asset Sizing

- Scan for image assets without resolution-appropriate variants
- Check for oversized images (> 1MB, or dimensions > 3x what's displayed)
- **Medium if**: Image asset significantly larger than display size
- **Method**: Check assets directory, compare file sizes and dimensions

### 5. Unnecessary Widget Rebuilds (stack-aware)

- If `flutter_bloc`:
  - `BlocBuilder` without `buildWhen` on frequently changing state
  - `BlocBuilder` on entire state when only one field is needed
- If `riverpod`:
  - `watch()` on entire provider when `select()` would suffice
  - Missing `autoDispose` on providers that should clean up
- If `provider`:
  - `Consumer` rebuilding on every state change without selector
- **Medium if**: Broad rebuild where selective rebuild is possible
- **Method**: Read state consumer patterns, check for selectivity

### 6. Overlay Checks

- Read the matched overlay's Performance section
- Execute each additional check (e.g., specific animation curve restrictions)

## Severity Rules Summary

| Check                        | Critical | High | Medium | Low |
| ---------------------------- | -------- | ---- | ------ | --- |
| API call in build()          |          | X    |        |     |
| Heavy computation in build() |          | X    |        |     |
| Layout property animation    |          |      | X      |     |
| Missing const (list item)    |          |      | X      |     |
| Oversized image asset        |          |      | X      |     |
| Broad rebuild                |          |      | X      |     |
| Missing const (infrequent)   |          |      |        | X   |

## Output Format

```text
file:line | severity | check_name | description | auto_fixable: yes/no | fix_action: {description}
```

Auto-fixable: Adding `const` to constructors where all fields are final and initialized with const-compatible defaults.
