# agent-skills

Agent skills for mobile app work, with a focus on Flutter.

Each skill is a directory under `skills/` with a `SKILL.md` in the [Agent Skills](https://agentskills.io) format.
Many skills adapt someone else's video, article, or post, and credit the original in a Sources section.
Skills that depend on libraries, SDKs, or store policies record in `metadata.docs-verified` the date they were last checked against official documentation, and list those docs under Sources.

## Install

### Claude Code

Claude Code loads skills from `~/.claude/skills/` for all projects and from `.claude/skills/` for a single project.

```bash
git clone https://github.com/mikezamayias/agent-skills.git
mkdir -p ~/.claude/skills

# One skill
cp -R agent-skills/skills/launch-readiness ~/.claude/skills/

# Every skill, as symlinks that pick up `git pull`
for d in "$PWD"/agent-skills/skills/*/; do ln -s "${d%/}" ~/.claude/skills/; done
```

### Other agents

Other agents that read Agent Skills folders take the same directories.
Copy or symlink each skill folder into the agent's skills directory.

| Agent  | Skills directory      |
| ------ | --------------------- |
| Codex  | `~/.codex/skills/`    |
| Cursor | `~/.cursor/skills/`   |
| Pi     | `~/.pi/agent/skills/` |

These paths change between agent versions, so check your agent's documentation.

Some skills call external tools, such as the Codex CLI, the `asc` App Store Connect CLI, Sentry, or mobile-mcp.
Each `SKILL.md` states what it needs.

## Validate

```bash
uv run --with pyyaml python3 toolbox/validate-skills.py
```

The validator checks names, descriptions (at most 1024 characters and 3 sentences), frontmatter keys, the `docs-verified` date format, and local links.

Markdown is formatted with Prettier and linted with markdownlint, the same tools the VS Code extensions `esbenp.prettier-vscode` and `davidanson.vscode-markdownlint` run.
Both CLIs are pinned to the versions those extensions bundle, and `.markdownlint-cli2.jsonc` holds the lint config for both the CLI and the extension.

```bash
npx prettier@3.7.4 --check "**/*.md"
npx markdownlint-cli2@0.23.2 "**/*.md"
```

## Skills

These are skills I wrote or adapted.
Skills that adapt someone else's work credit it in the skill.

<!-- skills:start -->

### Mobile app skills

| Skill                                                                                          | What it does                                                                                              |
| ---------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| [app-graphics](skills/app-graphics/SKILL.md)                                                   | Generates store icons, feature graphics, social banners, and a press hero from a project's local files.   |
| [app-landing-page](skills/app-landing-page/SKILL.md)                                           | Generates five single-file landing pages, each with a different design philosophy.                        |
| [app-screenshots](skills/app-screenshots/SKILL.md)                                             | Orchestrates App Store and Play Store screenshot capture, framing, and locale fan-out for a Flutter app.  |
| [break-ui](skills/break-ui/SKILL.md)                                                           | Stress-tests a Flutter screen with worst-case data, text scale, and RTL, and leaves a widget test behind. |
| [consumer-app-from-behavior](skills/consumer-app-from-behavior/SKILL.md)                       | Turns observed consumer behavior into a core loop, a reference teardown, and an MVP spec.                 |
| [cross-language-safety](skills/cross-language-safety/SKILL.md)                                 | Prevents type mismatches between PostgreSQL, PostgREST, Deno, JSON, and Dart.                             |
| [dart-tool-scripts](skills/dart-tool-scripts/SKILL.md)                                         | Moves non-trivial CI and bootstrap logic from Bash into `tool/*.dart` scripts.                            |
| [flutter-app-size-audit](skills/flutter-app-size-audit/SKILL.md)                               | Cuts Flutter install size through build flags, asset formats, and shrinking.                              |
| [flutter-async-at-the-edge](skills/flutter-async-at-the-edge/SKILL.md)                         | Keeps async work in services and repositories so views render synchronous sealed state.                   |
| [flutter-async-cubit-safety](skills/flutter-async-cubit-safety/SKILL.md)                       | Guards every `emit` after an `await` to prevent emit-after-close crashes.                                 |
| [flutter-bloc-clean-architecture](skills/flutter-bloc-clean-architecture/SKILL.md)             | Applies BLoC/Cubit with Clean Architecture, Very Good Ventures conventions, and a feature-first layout.   |
| [flutter-clean-architecture-tdd](skills/flutter-clean-architecture-tdd/SKILL.md)               | Scaffolds and reviews Flutter features with Clean Architecture and test-first development.                |
| [flutter-cubit-smart-caching](skills/flutter-cubit-smart-caching/SKILL.md)                     | Adds time-based freshness checks so cubits skip redundant reloads on navigation.                          |
| [flutter-error-logging-conventions](skills/flutter-error-logging-conventions/SKILL.md)         | Replaces silent `catch (_)` blocks with consistently prefixed logging.                                    |
| [flutter-observability-instrumentation](skills/flutter-observability-instrumentation/SKILL.md) | Adds type-safe analytics, tracing, metrics, and breadcrumbs with Sentry and PostHog.                      |
| [flutter-paywall-and-review-timing](skills/flutter-paywall-and-review-timing/SKILL.md)         | Covers IAP wiring, App Store review prompt limits, and a decaying paywall schedule.                       |
| [flutter-precommit-cleanup](skills/flutter-precommit-cleanup/SKILL.md)                         | Formats, analyzes, regenerates code, and squashes WIP commits before a PR.                                |
| [flutter-router-decision](skills/flutter-router-decision/SKILL.md)                             | Picks a Flutter router and keeps go_router unless there is a concrete need to switch.                     |
| [flutter-runtime-safety](skills/flutter-runtime-safety/SKILL.md)                               | Catches errors that escape try-catch and stops restored backups from bringing back bad state.             |
| [flutter-shorebird-ota](skills/flutter-shorebird-ota/SKILL.md)                                 | Ships Dart-only over-the-air patches with Shorebird, including in CI.                                     |
| [flutter-stream-architecture](skills/flutter-stream-architecture/SKILL.md)                     | Multicasts repository streams and limits Bloc rebuilds.                                                   |
| [flutter-strict-analysis](skills/flutter-strict-analysis/SKILL.md)                             | Adopts a strict lint policy and enforces it in CI with `--fatal-infos`.                                   |
| [flutter-web-first-paint](skills/flutter-web-first-paint/SKILL.md)                             | Fixes blank first loads on Flutter web with an HTML splash, deferred imports, and preloading.             |
| [forced-pivot-15-day](skills/forced-pivot-15-day/SKILL.md)                                     | Sequences a one to three week pivot forced by a store guideline, policy, or deadline.                     |
| [gplay-console](skills/gplay-console/SKILL.md)                                                 | Preflights and automates Google Play releases, tracks, store listings, Data safety, and vitals.           |
| [ios-distribution-feature-flags](skills/ios-distribution-feature-flags/SKILL.md)               | Sets compile-time feature flags for Debug, TestFlight, and App Store builds.                              |
| [launch-readiness](skills/launch-readiness/SKILL.md)                                           | Runs a tiered Flutter launch audit and produces a scored SHIP, HOLD, or BLOCK report.                     |
| [launch-watch](skills/launch-watch/SKILL.md)                                                   | Proves launch telemetry arrives, then watches analytics, crashes, email, and feedback for three weeks.    |
| [market-pulse](skills/market-pulse/SKILL.md)                                                   | Produces an app market analysis covering competitors, sizing, pricing, and projections.                   |
| [mobile-ui-reference](skills/mobile-ui-reference/SKILL.md)                                     | Designs Flutter screens from shipped references instead of generated UI.                                  |
| [paywall-conversion-flow](skills/paywall-conversion-flow/SKILL.md)                             | Orders onboarding, the rating prompt, and the paywall so value comes first.                               |
| [paywall-transparency](skills/paywall-transparency/SKILL.md)                                   | Shows users what they get and when they will be charged before the paywall.                               |
| [pr-preview-shipping](skills/pr-preview-shipping/SKILL.md)                                     | Makes every pull request produce an installable preview.                                                  |
| [proactive-crash-repair-loop](skills/proactive-crash-repair-loop/SKILL.md)                     | Turns Sentry crash telemetry into deduplicated, human-reviewed draft fix PRs.                             |
| [promise-audit](skills/promise-audit/SKILL.md)                                                 | Traces every promise in a privacy policy, terms, or marketing claim to the mechanism behind it.           |
| [ship-first-dollar-app](skills/ship-first-dollar-app/SKILL.md)                                 | Validates paid pain, scopes a one-feature MVP, and measures the path to first revenue.                    |
| [slim-ios-simulator-fleet](skills/slim-ios-simulator-fleet/SKILL.md)                           | Fits more iOS simulators on one Mac with simslim.                                                         |
| [store-launch-mastermind](skills/store-launch-mastermind/SKILL.md)                             | Orchestrates App Store and Google Play go-live into one go/no-go report.                                  |

### Agentic workflow skills

| Skill                                                                              | What it does                                                                                               |
| ---------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| [academic-research-assistant](skills/academic-research-assistant/SKILL.md)         | Synthesizes several research papers into one literature review of claims, debates, and consensus.          |
| [answer-sheet](skills/answer-sheet/SKILL.md)                                       | Puts open questions on one self-contained HTML page and saves the answers to a dated Markdown file.        |
| [decision-sweep](skills/decision-sweep/SKILL.md)                                   | Logs each ruling once and updates every dependent document, then runs checks.                              |
| [engineering-diary](skills/engineering-diary/SKILL.md)                             | Keeps a daily engineering diary so a solo developer does not lose context between sessions.                |
| [figma-review-loop](skills/figma-review-loop/SKILL.md)                             | Runs a Figma review round: reads comments, records rulings, redesigns frames, and sweeps instances.        |
| [moscow-prioritization](skills/moscow-prioritization/SKILL.md)                     | Cuts a noisy backlog with Must, Should, Could, and Won't.                                                  |
| [orchestrate-agentic-engineering](skills/orchestrate-agentic-engineering/SKILL.md) | Coordinates one human, one orchestrator, and bounded specialist agents from brief to end-to-end proof.     |
| [parallel-agent-inbox](skills/parallel-agent-inbox/SKILL.md)                       | Runs many coding-agent threads as an inbox and only pulls the human in when work is done or blocked.       |
| [spec-sql-harness](skills/spec-sql-harness/SKILL.md)                               | Proves SQL from design documents by loading it into the production Postgres image with smoke tests.        |
| [sync-context](skills/sync-context/SKILL.md)                                       | Builds a morning briefing from the last 7 days of GitHub, Slack, and PostHog activity.                     |
| [task-blitz](skills/task-blitz/SKILL.md)                                           | Pulls open tasks from Notion and runs independent ones with parallel sub-agents that plan before coding.   |
| [techdebt](skills/techdebt/SKILL.md)                                               | Scans a project for duplicate code, dead code, TODOs, and unused imports, and writes a prioritized report. |
| [vendor-decision](skills/vendor-decision/SKILL.md)                                 | Chooses or re-checks a backend, API, or service from live evidence, competitors, and gatekeepers.          |
| [web-interface-review](skills/web-interface-review/SKILL.md)                       | Reviews web UI code for accessibility, focus, forms, dark mode, i18n, and phone behavior.                  |

<!-- skills:end -->

## Third-party skills I use

I also use these skills as published by their authors.
They are not copied here, so install them from their source.

<!-- third-party:start -->

| Source                                                                                                       | Skills                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| ------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [clawhub.ai/0xterrybit/skills/todo](https://clawhub.ai/0xterrybit/skills/todo)                               | `todo`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| [clawhub.ai/bjesuiter/skills/prd](https://clawhub.ai/bjesuiter/skills/prd)                                   | `prd`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| [clawhub.ai/chandrasekar-r/skills/security-audit](https://clawhub.ai/chandrasekar-r/skills/security-audit)   | `security-audit`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| [clawhub.ai/julianengel/skills/remind-me](https://clawhub.ai/julianengel/skills/remind-me)                   | `remind-me`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| [clawhub.ai/michaelgathara/skills/youtube-watcher](https://clawhub.ai/michaelgathara/skills/youtube-watcher) | `youtube-watcher`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| [clawhub.ai/pors/skills/research](https://clawhub.ai/pors/skills/research)                                   | `research`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| [clawhub.ai/zats/skills/perplexity](https://clawhub.ai/zats/skills/perplexity)                               | `perplexity`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| [Appllama/appllama-skills](https://github.com/Appllama/appllama-skills)                                      | `appllama-app-design-skill`, `appllama-usage`                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| [besoeasy/open-skills](https://github.com/besoeasy/open-skills)                                              | `humanizer`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| [clawdbot/linkedin-cli](https://github.com/clawdbot/linkedin-cli)                                            | `linkedin-cli`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| [cloudflare/skills](https://github.com/cloudflare/skills)                                                    | `agents-sdk`, `durable-objects`, `turnstile-spin`, `web-perf`                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| [codeswithroh/tastemaker](https://github.com/codeswithroh/tastemaker)                                        | `tastemaker`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| [dietrichgebert/ponytail](https://github.com/dietrichgebert/ponytail)                                        | `ponytail`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| [herdrdev/herdr](https://github.com/herdrdev/herdr)                                                          | `herdr`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| [heygen-com/hyperframes](https://github.com/heygen-com/hyperframes)                                          | `faceless-explainer`, `hyperframes`, `hyperframes-animation`, `hyperframes-audio`, `hyperframes-cli`, `hyperframes-core`, `hyperframes-creative`, `hyperframes-keyframes`, `hyperframes-registry`, `hyperframes-studio`, `media-use`                                                                                                                                                                                                                                                                    |
| [multica-ai/andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills)                    | `karpathy-guidelines`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| [openclaw/openclaw](https://github.com/openclaw/openclaw)                                                    | `apple-notes`, `apple-reminders`, `coding-agent`, `gemini`, `peekaboo`, `skill-creator`                                                                                                                                                                                                                                                                                                                                                                                                                 |
| [pskoett/self-improving-agent](https://github.com/pskoett/self-improving-agent)                              | `self-improving-agent`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| [rorkai/app-store-connect-cli-skills](https://github.com/rorkai/app-store-connect-cli-skills)                | `asc-app-create-ui`, `asc-aso-audit`, `asc-build-lifecycle`, `asc-cli-usage`, `asc-crash-triage`, `asc-id-resolver`, `asc-localize-metadata`, `asc-metadata-sync`, `asc-notarization`, `asc-ppp-pricing`, `asc-release-flow`, `asc-revenuecat-catalog-sync`, `asc-screenshot-resize`, `asc-shots-pipeline`, `asc-signing-setup`, `asc-submission-health`, `asc-subscription-localization`, `asc-testflight-orchestration`, `asc-wall-submit`, `asc-whats-new-writer`, `asc-workflow`, `asc-xcode-build` |
| [twostraws/Swift-Concurrency-Agent-Skill](https://github.com/twostraws/Swift-Concurrency-Agent-Skill)        | `swift-concurrency-pro`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| [twostraws/Swift-Testing-Agent-Skill](https://github.com/twostraws/Swift-Testing-Agent-Skill)                | `swift-testing-pro`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| [twostraws/SwiftUI-Agent-Skill](https://github.com/twostraws/SwiftUI-Agent-Skill)                            | `swiftui-pro`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| [vercel-labs/agent-browser](https://github.com/vercel-labs/agent-browser)                                    | `agent-browser`, `agent-browser-legacy`                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| [VeryGoodOpenSource/vgv-ai-flutter-plugin](https://github.com/VeryGoodOpenSource/vgv-ai-flutter-plugin)      | `vgv-accessibility`, `vgv-dart-flutter-sdk-upgrade`, `vgv-green-gate`, `vgv-license-compliance`, `vgv-static-security`, `vgv-testing`, `vgv-ui-package`, `vgv-very-good-analysis-upgrade`                                                                                                                                                                                                                                                                                                               |

<!-- third-party:end -->

## Contributing

Open an issue for changes.
This repository is generated, so pull requests would be overwritten.

## License

BSD 3-Clause.
See [LICENSE](LICENSE).
