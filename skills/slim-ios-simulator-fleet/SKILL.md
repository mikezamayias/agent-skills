---
name: slim-ios-simulator-fleet
description: >-
  Use simslim to disable unused daemons inside iOS 18+ simulators so more of them fit on one Mac. Use when booting more than a couple of iOS simulators or when GitHub Actions macOS jobs run out of memory. Also use when an agent needs one simulator per task.
metadata:
  docs-verified: "2026-09-28"
---

# Slim iOS simulator fleet

`simslim` disables ~170 unused daemons **inside that simulator only**. Host Mac is untouched.

Requires Mac + Xcode + iOS **18.5+** runtime for persistent slimming.
`simslim on` rejects older runtimes before touching the simulator.
On iOS 17.x and 18.3, `simslim on <udid> --no-reboot` slims only the current boot session, so re-run it after every boot.

## Install and slim

```sh
brew install mobai-app/tap/simslim
simslim list
simslim on <udid>
```

`on` writes the disable overrides and boots the simulator slim, shutting it down first if it is booted.
Later boots come up slim (~4 GB → ~0.9 GB).

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

## CI preflight

```sh
simslim verify "$UDID" --profile ci.json || simslim on "$UDID" --profile ci.json
simslim doctor "$UDID" --requires push,storekit,universal-links
```

GitHub-hosted macOS runners: `export SIMSLIM_BOOT_TIMEOUT=15m` and `SIMSLIM_SPAWN_TIMEOUT=5m`.

`simslim clone` before destructive experiments. `disk-clean` is permanent and **requires** `--confirm`. It will not delete app documents or shrink the signed iOS runtime.

After `erase` / new runtime / "Erase All Content and Settings", the sim is stock again — re-run `on`.

## Sources

- <https://github.com/MobAI-App/simslim>
