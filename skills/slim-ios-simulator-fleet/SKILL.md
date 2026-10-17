---
name: slim-ios-simulator-fleet
description: >-
  Use simslim to disable unused daemons inside iOS, tvOS, watchOS and visionOS simulators so more of them fit on one Mac. Use when booting more than a couple of simulators or when GitHub Actions macOS jobs run out of memory. Also use when an agent needs one simulator per task.
metadata:
  docs-verified: "2026-10-17"
---

# Slim iOS simulator fleet

`simslim` disables ~170 of the ~180 daemons a fresh simulator starts **inside that simulator only**. Host Mac is untouched.

Requires Mac + Xcode + a simulator runtime at or above the persistence gate: iOS or tvOS **18.5**, watchOS 11.5, visionOS 2.5.
`simslim on` rejects older runtimes before touching the simulator.
On iOS 17.x and 18.3, `simslim on <udid> --no-reboot` slims only the current boot session, so re-run it after every boot.
The README says the tvOS, watchOS and visionOS cutoffs follow the iOS release generation and are not independent measurements.

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
Later boots come up slim (~4 GB → ~0.9 GB).
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

## CI preflight

```sh
simslim verify "$UDID" --profile ci.json || simslim on "$UDID" --profile ci.json
simslim doctor "$UDID" --requires push,storekit,universal-links
```

GitHub-hosted macOS runners: `export SIMSLIM_BOOT_TIMEOUT=15m` and `SIMSLIM_SPAWN_TIMEOUT=5m`.

`simslim clone` before destructive experiments. `disk-clean` is permanent and **requires** `--confirm`. It will not delete app documents or shrink the signed iOS runtime.

After `erase` / new runtime / "Erase All Content and Settings", the sim is stock again — re-run `on`.

## Disk and lifecycle

Run `simslim size <udid>` for a simulator's disk footprint and `simslim disk-categories` for what can be removed and what is protected.
Run `simslim disk-plan <udid>` before any clean, because it shows the reclaimable breakdown and deletes nothing.
Clean with `simslim disk-clean <udid> --categories caches,logs,temporary --confirm`.
Lifecycle commands are `simslim boot`, `shutdown`, `clone <udid> <name>`, `rename`, `erase` and `delete`, and `boot` waits for services before it returns.
Pass `--json` when a script parses simslim output.
These commands come from MobAI's simslim skill (October 2026), so run `simslim --help` to confirm them on the installed version.

## Sources

- <https://github.com/MobAI-App/simslim> (README and commit titles read 2026-10-17)
