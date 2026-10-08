# Phase: Hardening

## Tier

T2 — Quality Gate

## Inputs

- Stack profile (state management, UI framework)
- Overlay checks (project-specific edge cases)
- Scope: file list or "all"

## Checks

### 1. Missing Error States

- Scan pages/widgets that display data from async sources (cubits, providers, futures)
- Verify they handle the error/failure case with user-visible feedback
- **Critical if**: Screen that makes network calls has no error handling UI
- **High if**: Screen shows data from state but doesn't check for error state type
- **Method**: Read page files, check for error state branches in BlocBuilder/Consumer/etc.

### 2. Missing Empty States

- Scan list/collection views for empty data handling
- Verify `ListView`, `GridView`, `Column` with `for` loops have an empty check
- **Medium if**: List view renders nothing when data is empty (blank screen)
- **Method**: Read widget files with list rendering, check for `isEmpty` guards

### 3. Missing Loading States

- Scan pages that trigger async loads in `initState` or on user action
- Verify they show a loading indicator during the async operation
- **High if**: Screen with async data shows nothing while loading
- **Method**: Check state management pattern for loading state emission and corresponding UI

### 4. Lifecycle Guards (stack-aware)

- If `flutter_bloc`: Every async cubit method must check `if (isClosed) return;` before each `emit()` after an `await`
- If `riverpod`: Async notifier methods must check `ref.mounted` (Riverpod 3.0+) before state updates
- If `provider`: ChangeNotifier async methods must check `disposed` state
- **High if**: Async state method missing lifecycle guard after await
- **auto_fixable**: yes
- **fix_action**: Add `if (isClosed) return;` before emit (bloc) or equivalent guard
- **Method**: Read state files, check for await followed by emit without guard

### 5. Network Error Handling

- Scan repository methods that make HTTP/API calls
- Verify they catch network exceptions and return appropriate failure types
- **High if**: Repository method has uncaught network exceptions
- **Method**: Read repository files, check for try-catch around HTTP calls

### 6. Text Overflow

- Scan for `Text()` widgets in constrained layouts (`Row`, fixed-width containers) without overflow handling
- **Medium if**: Text in constrained layout without `overflow`, `maxLines`, or `Expanded` wrapper
- **auto_fixable**: yes
- **fix_action**: Add `overflow: TextOverflow.ellipsis, maxLines: N`
- **Method**: Read widget files, find Text in Row/constrained contexts

### 7. Overlay Checks

- Read the matched overlay's Hardening section
- Execute each additional check
- Severity: as specified in overlay

## Severity Rules Summary

| Check                                | Critical | High | Medium | Low |
| ------------------------------------ | -------- | ---- | ------ | --- |
| Missing error state (network screen) | X        |      |        |     |
| Missing loading state                |          | X    |        |     |
| Missing lifecycle guard              |          | X    |        |     |
| Missing network error handling       |          | X    |        |     |
| Missing empty state                  |          |      | X      |     |
| Text overflow risk                   |          |      | X      |     |

## Output Format

```text
file:line | severity | check_name | description | auto_fixable: yes/no | fix_action: {description}
```
