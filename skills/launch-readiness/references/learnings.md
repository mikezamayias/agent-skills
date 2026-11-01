# Launch Readiness — Learned Patterns

Patterns discovered during runs that are not yet in phase check lists.
Entries older than 90 days without promotion to a phase file are auto-pruned.

---

## 2026-10-29 - SwiftUI app run

- NEW CHECK (store-compliance): re-read the store description, review notes and App Privacy argument against features added after they were written (here: iPhone direct sign-in added after the "iPhone never signs in" text). A claim the binary contradicts is a 2.3.1 rejection.
- NEW CHECK (hardening): for every purchase path, check where the purchase identity (RevenueCat App User ID, account token) is stored and whether it survives reinstall and account linking. A random ID in app storage plus "Keep with original App User ID" locks a paying user out.
- REFINEMENT (accessibility): a SwiftUI `.frame(minHeight: 44)` placed after `Button(...)` does not grow the hit area. Check that the frame is inside the label with a contentShape.
