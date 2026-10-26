---
name: slim-ios-simulator-fleet
description: >-
  Uses simslim to disable unused daemons inside iOS, tvOS, watchOS and visionOS simulators so more fit on one Mac. Use when booting more than a couple of simulators or when GitHub Actions macOS jobs run out of memory. Also use when an agent needs one simulator per task.
metadata:
  docs-verified: "2026-10-25"
---

# Slim iOS simulator fleet

`simslim` disables ~170 of the ~180 daemons a fresh simulator starts **inside that simulator only**. Host Mac is untouched.

Requires Mac + Xcode + a simulator runtime at or above the persistence gate: iOS or tvOS **18.5**, watchOS 11.5, visionOS 2.5.
`simslim on` rejects older runtimes before touching the simulator.
On iOS 17.x and 18.3, `simslim on <udid> --no-reboot` slims only the current boot session, so re-run it after every boot.
The README says the tvOS, watchOS and visionOS cutoffs follow the iOS release generation and are not independent measurements.

Agents tend to boot one new simulator per task and leave the old ones running, which is how a 16 or 18 GB Mac runs out of memory (single reports).
Add a rule to the project's agent instructions that a new simulator is booted only after the previous one is shut down by UDID, and cap the number of booted simulators.
`simslim list --booted` shows what is running, and `simslim top` shows a live per-simulator RAM monitor.

## Remote code gate

**Remote code gate.** This step runs code fetched at run time. Each time, download the exact version into an empty directory without running it, have a separate reviewer agent (the `code-gate` subagent where it exists) read its source, and run it only if the reviewer returns SAFE, from those reviewed files, never from a fresh download. On UNSAFE or UNSURE, do not run it and tell the user why.

Covers:

- `brew install mobai-app/tap/simslim`, a third-party Homebrew tap, in "Install and slim" and in any CI step that installs it.
- Updating `simslim` before debugging a launch delay or a log flood.

## Other platforms

The same commands and profiles cover tvOS, watchOS and visionOS simulators.
The memory figures in this skill were measured on iOS, so savings elsewhere depend on runtime and workload.
For Watch connectivity tests, keep `connectivity,messaging` with `--except`, and add `health` for HealthKit or fitness tests.
A visionOS simulator stays expensive even when slim.
Update simslim before debugging a launch delay or a log flood.
Commits from 2026-10-08 and 2026-10-09 stopped disabling `gamed`, `assistantd` and `navd`, per their titles: an XCUITest launch delay, a Spotlight memory leak, and a Maps widget log flood handled with `--except widgets`.

## Install and slim

```sh
brew install mobai-app/tap/simslim
simslim list
simslim on <udid>
```

`on` writes the disable overrides and boots the simulator slim, shutting it down first if it is booted.
Later boots come up slim.
The author's own table measured one iOS simulator on an M1 Pro with 16 GB at 4.0 GB stock and 0.9 GB slim, and 258 processes against 70, using `phys_footprint`.
Other figures on file are one user report of 4.1 GB to about 1 GB (single report) and an idle fully slim baseline of 1,113.4 MiB on iOS 26.5 in the repository's method note.
Treat 4x as an upper estimate and measure with `simslim measure <udid>`.
Do not compare it with a sum of `ps` RSS, because RSS counts shared mappings once per process.
`simslim off <udid>` restores a simulator to stock by re-enabling every daemon and rebooting it, and a full reconfigure takes a minute or two.
Check a slimmed simulator with `simslim status <udid>` and its memory with `simslim measure <udid>`, both on a booted simulator.
`simslim profiles` lists the daemon categories a slim boot disables and the tradeoff of each.
Do not disable daemons by hand with `xcrun simctl`, because simslim's allowlist skips the daemons that wedge a simulator, such as `nanoregistryd` and `sleepd`, even with `--keep` or `--except`.

## Commit a profile

```json
{
  "name": "ci",
  "description": "UI tests",
  "except": ["store"],
  "keep": ["com.apple.apsd"]
}
```

```sh
simslim on <udid> --profile ci.json
```

Cannot mix `--profile` with `--except` / `--keep`.

Keep features you actually test: `--except search` or `--keep com.apple.apsd` (push), `storekitd` (StoreKit), `swcd` (universal links). StoreKit / push / Spotlight tests fail if you slim those categories.
The category names are `search` (Spotlight), `store` (push via `apsd` and StoreKit via `storekitd`) and `web` (universal links via `swcd`).
Contacts, Photos and Calendar pickers may misbehave when their categories are slimmed.

On the main branch after v0.12.2 (commit of 2026-10-25, not in a release), `simslim enable <udid> icloud,photos` turns categories or single daemons back on in a running simulator without a reboot, and `simslim disable <udid> icloud` turns them off again.
Add `--save dev.json` to write the change into the profile file, so that `on`, `watch` and `verify` agree with it.
`enable` reports a daemon that launchd only loads at the next boot (`notStarted` in `--json`), and `disable` keeps a daemon running that another enabled category still needs (`stillEnabled`).
The Homebrew formula still builds v0.12.2, so check `simslim --help` for `enable` before relying on it.

## CI preflight

```sh
simslim verify "$UDID" --profile ci.json || simslim on "$UDID" --profile ci.json
simslim doctor "$UDID" --requires push,storekit,universal-links
```

GitHub-hosted macOS runners: `export SIMSLIM_BOOT_TIMEOUT=15m` and `SIMSLIM_SPAWN_TIMEOUT=5m`.

Run `simslim doctor --list` for the feature names that `--requires` accepts, and add `--json` for a script.
`doctor` exits non-zero when a required feature is broken, so it works as a CI preflight.

`simslim clone` before destructive experiments. `disk-clean` is permanent and **requires** `--confirm`. It will not delete app documents or shrink the signed iOS runtime.

After `erase` / new runtime / "Erase All Content and Settings", the sim is stock again — re-run `on`.

Slim state lives in that simulator's launchd database on that Mac.
A deleted and recreated simulator, a simulator on a new runtime, and a simulator moved to another Mac all come up stock, so run `simslim verify` before a run that depends on it.
`on --no-reboot`, `enable` and `disable` act on the running boot session and, on iOS 17.x and 18.3, do not survive a reboot.

## Parallel testing clones

`xcodebuild` parallel testing creates a stock clone per worker, because disable overrides do not survive `simctl clone`.
Run `simslim watch` (with `--profile`, `--except` or `--keep`) in the background before the test run.
It polls the default and `testing` device sets, plus any set passed with `--set`, and slims each simulator without a reboot as it boots.
A failed slim is retried on the next scan, and a simulator that boots again is slimmed again.
Use `simslim clone <udid> <name>` instead of `simctl clone` when a copy must stay slim.
`simslim repair-clone <source-udid> <clone-udid>` repairs clones made by older simslim builds and needs the exact source UDID.

## Disk and lifecycle

Run `simslim size <udid>` for a simulator's disk footprint and `simslim disk-categories` for what can be removed and what is protected.
Run `simslim disk-plan <udid>` before any clean, because it shows the reclaimable breakdown and deletes nothing.
Clean with `simslim disk-clean <udid> --categories caches,logs,temporary --confirm`.
Lifecycle commands are `simslim boot`, `shutdown`, `clone <udid> <name>`, `rename`, `erase` and `delete`, and `boot` waits for services before it returns.
Pass `--json` when a script parses simslim output.
These commands come from MobAI's simslim skill (October 2026), so run `simslim --help` to confirm them on the installed version.

## Sources

- <https://github.com/MobAI-App/simslim> (README and commit titles read 2026-10-17, README at main and commit titles read 2026-10-25)
