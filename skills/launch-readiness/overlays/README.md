# Overlays

Project-specific check additions for the launch-readiness skill.

## How to Write an Overlay

1. Create a file named `{project-name}.md` in this directory
2. The name must match one of:
   - The `name` field in `pubspec.yaml`
   - The git repository root directory name
   - Or be specified explicitly via `--overlay {name}`

## Structure

```markdown
# {Project Name} Overlay

## Project Info

- name: {project name}
- type: {Flutter mobile/web/desktop}
- monetization: {model or "none"}

## Phase Additions

### Testing

{additional test requirements}

### Security

{additional security checks}

### Hardening

{additional edge case checks}

### Accessibility

{additional a11y checks}

### Responsive

{additional responsive checks}

### Localization

{l10n scope and known string locations}

### Analytics

{required funnel steps, event naming rules}

### Performance

{project-specific performance rules}

### Polish

{design system rules, banned patterns}
```

## Rules

- Each section header must match a phase name exactly
- Checks inherit severity from the phase unless explicitly overridden
- Overlay checks run AFTER generic phase checks
- Keep overlays focused — generic patterns belong in phase files
