# Phase: Testing

## Tier

T1 — Ship Blocker

## Inputs

- Stack profile (state management, test runner)
- Overlay checks (project-specific test requirements)
- Scope: file list or "all"

## Checks

### 1. Test Suite Passes

Run the project's test suite:

- If `very_good_cli` detected: `very_good test --coverage --min-coverage {threshold}`
- Otherwise: `flutter test`
- **Critical if**: Any test fails
- **Method**: Run the test command via Bash, parse exit code and output

### 2. Coverage Threshold

- Read threshold from CLAUDE.md (look for "min-coverage" or "coverage" mentions), default to 50%
- **Critical if**: Coverage below threshold
- **Method**: Parse coverage output from test runner

### 3. Skipped Tests

- Scan test files for `skip:` parameter without a `// reason:` comment on the same or preceding line
- **High if**: Skipped test without documented reason
- **Low if**: Skipped test with documented reason (just note it)
- **Method**: Grep test files for `skip: true` or `skip:` patterns

### 4. Permanently Excluded Tags

- Check test runner config and CI workflow for `--exclude-tags` flags
- **Medium if**: Tests excluded by tag with no tracking issue referenced
- **Method**: Grep workflow YAML files and test config for exclude-tags

### 5. State Management Test Patterns (stack-aware)

- If `flutter_bloc`: Verify cubits have corresponding test files using `blocTest`
- If `riverpod`: Verify providers have test files using `ProviderContainer`
- If `provider`: Verify ChangeNotifiers have test files
- **Medium if**: State class exists without corresponding test file
- **Method**: Glob for state files, check for matching test files

### 6. Overlay Checks

- Read the matched overlay's Testing section
- Execute each additional check listed there
- Severity: as specified in overlay, default to High

## Severity Rules Summary

| Check                      | Critical | High | Medium | Low |
| -------------------------- | -------- | ---- | ------ | --- |
| Test failure               | X        |      |        |     |
| Below coverage             | X        |      |        |     |
| Skipped no reason          |          | X    |        |     |
| Excluded tags              |          |      | X      |     |
| Missing state tests        |          |      | X      |     |
| Skipped with reason        |          |      |        | X   |
| Non-descriptive test names |          |      |        | X   |

## Output Format

```text
file:line | severity | check_name | description | auto_fixable: no | fix_action: none
```

Note: Testing phase findings are generally not auto-fixable — they require writing tests or fixing code.
