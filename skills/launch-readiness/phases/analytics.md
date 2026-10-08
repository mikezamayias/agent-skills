# Phase: Analytics

## Tier

T3 — Polish & Verify

## Inputs

- Stack profile (analytics, navigation, state management)
- Overlay checks (required funnel steps, event naming rules)
- Scope: file list or "all"

## Checks

### 1. Screen Detection & View Events

Detect screens using stack-aware heuristics:

- **go_router**: Each `GoRoute` path definition = one screen
- **auto_route**: Each `@RoutePage()` annotation = one screen
- **navigator**: Each `MaterialPageRoute`/`CupertinoPageRoute` push = one screen

For each detected screen, verify a corresponding screen view event exists:

- **Medium if**: Screen without a view tracking event
- **Method**: Map route definitions, then grep for tracking calls that reference each screen

### 2. Action Detection & Tracking

Detect trackable user actions:

- Any `onTap`/`onPressed` callback that calls a cubit/notifier/controller method = trackable
- Form submissions (`onSubmit`, `onSave`) = trackable
- Toggle switches, settings changes = trackable
- NOT trackable: scroll events, animation completions, hover states

For each detected action, verify a tracking event exists:

- **Medium if**: User action without tracking event
- **Method**: Grep for onTap/onPressed that call state methods, check for tracking call nearby

### 3. Orphan Events

- Find all defined event names/enums in the analytics system
- Verify each is actually triggered somewhere in the codebase
- **Medium if**: Event defined but never triggered (dead event)
- **Method**: List all event definitions, grep for each in the codebase

### 4. Funnel Completeness

- If overlay defines a required funnel (e.g., install → sign-up → first key action → purchase), verify:
  - Each step has a tracking event
  - Events are triggered in the correct code paths
- **High if**: Core funnel step (from overlay) is missing tracking
- **Method**: Read overlay funnel definition, verify each step exists

### 5. Failure Event Counterparts

- For each success event (e.g., a purchase success event), check for a corresponding failure event
- **Low if**: Success event exists without a failure counterpart
- **Method**: List success-type events, check for matching failure events

### 6. Stack-Aware Event Naming

- If PostHog: Verify all events use typed event constants, no raw strings
- If Firebase: Verify `FirebaseAnalytics.instance.logEvent()` uses consistent event names
- If Amplitude: Verify `amplitude.track(BaseEvent(...))` uses consistent naming
- **Medium if**: Raw string event names instead of typed constants
- **Method**: Grep for tracking calls, check if they reference constants vs string literals

### 7. Overlay Checks

- Read the matched overlay's Analytics section
- Execute required funnel verification and naming rules

## Severity Rules Summary

| Check                              | Critical | High | Medium | Low |
| ---------------------------------- | -------- | ---- | ------ | --- |
| Core funnel step missing (overlay) |          | X    |        |     |
| Screen without view event          |          |      | X      |     |
| Action without tracking            |          |      | X      |     |
| Orphan event                       |          |      | X      |     |
| Raw string event names             |          |      | X      |     |
| Missing failure counterpart        |          |      |        | X   |

## Output Format

```text
file:line | severity | check_name | description | auto_fixable: no | fix_action: none
```

Note: Analytics findings are not auto-fixable — they require decisions about what to track and how.
