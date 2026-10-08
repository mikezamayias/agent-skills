---
name: flutter-stream-architecture
description: >-
  Design Flutter/Bloc stream layers that scale. Use when seeing duplicate API calls, redundant rebuilds, or when reviewing repository/cubit boundaries.
metadata:
  docs-verified: "2026-09-28"
---

# Flutter Stream Architecture

Architectures that scale treat streams as **infrastructure**, not factories. The mistake most teams make is creating a fresh stream per consumer — a "factory" — which silently triggers duplicate upstream pipelines (DB queries, websockets, API polls).

## The shift

- **Factory pattern (bad at scale):** every `repo.watchUser()` call returns a new stream → N consumers = N upstream pipelines.
- **Multicast pattern (good):** repository owns one upstream stream and broadcasts to all consumers via `BehaviorSubject` / `StreamController.broadcast()` / `rxdart`.

Wrap the upstream once. Cache the latest value. Replay it to new subscribers.

## Rebuild discipline

In Bloc/Cubit, two flags matter:

- `buildWhen` on `BlocBuilder` — only rebuild when the relevant slice changes. Stops 10x redundant rebuilds during typing/scrolling.
- `listenWhen` on `BlocListener` — only fire side effects on transitions, not every state change.

Pair with the `restartable()` event transformer from `bloc_concurrency` for search/typing flows so the in-flight request is cancelled when a new event arrives.
`droppable()` does the opposite: it ignores new events while one is processing.
Event transformers apply to `Bloc` only, so use a `Bloc` rather than a `Cubit` for these flows.

## Strategy pattern over conditionals

When you have "local search vs remote search" or "free vs paid pipeline," encode the variation as a `SearchStrategy` interface with two implementations. Don't grow `if (isPro)` branches inside the cubit — that's where bugs live.

## Don't abstract too early

When the domain is still forming, repetition is cheaper than false generality. Wait until you have 3 concrete examples before extracting an abstraction. Premature interfaces create the wrong contract and have to be torn out anyway.

## Review checklist

- [ ] No `repository.watchX()` returns a fresh stream per call.
- [ ] All `BlocBuilder`s have `buildWhen`.
- [ ] All `BlocListener`s have `listenWhen`.
- [ ] Search/autocomplete flows use a `Bloc` with `restartable()`.
- [ ] No more than one `if (isPro)` in any single file.

## Sources

- <https://pub.dev/packages/bloc_concurrency>
- <https://bloclibrary.dev/flutter-bloc-concepts/>
- <https://api.dart.dev/stable/dart-async/StreamController/StreamController.broadcast.html>
