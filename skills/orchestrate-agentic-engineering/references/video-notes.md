# Video Notes

## Source

- Title: _L8 Principal Building a Full Stack App with Agentic Engineering_
- Creator: Kun Chen
- URL: <https://www.youtube.com/watch?v=kPN564Kol14>
- Duration: 1:40:02
- Published: 2026-07-27
- Reviewed from English YouTube captions.

No full transcript is stored. Notes below paraphrase observed workflow and separate product-specific choices from reusable orchestration.

## Observed Workflow

- Human gives one coordinator a long narrative instead of pre-routing every task.
- Coordinator normalizes narrative and sends independent market and technical research in parallel.
- Research becomes interactive, reviewable artifacts rather than only long prose.
- Human corrects hidden assumptions, removes premature scope, and challenges inaccurate infrastructure cost estimates.
- Settled product and architecture decisions move into repository artifacts.
- Coordinator delegates frontend, backend, infrastructure, UX, and review work while remaining available for steering.
- Context compaction becomes manageable because durable state lives outside chat.
- Integration exposes mismatches that isolated tracks miss, including mock clients and wrong backend addresses.
- Completion requires real authentication, real backend, persisted state, and end-to-end evidence.
- Production and credential actions require human authorization even when agents have broad capability.

## Transferable Principles

1. Use one steering interface to reduce human context switching.
2. Keep coordinator responsive by delegating bounded work.
3. Parallelize independent discovery before freezing plan.
4. Make human judgment explicit at cost, scope, security, and production boundaries.
5. Persist decisions and task state in repository before context pressure rises.
6. Treat work graph and handoff contracts as coordination infrastructure.
7. Integrate early enough to expose cross-stream contract drift.
8. Define done as executable user journey, not local tests or mocks.

## Adaptation Choices

- Replace Herder, First Mate, Pi, Lavish, and model names with role and capability requirements.
- Support hosts without subagents by executing same dependency graph sequentially.
- Add explicit file-isolation, raw-artifact review, secret handling, and external-action boundaries.
- Require stop-and-replan behavior when new evidence invalidates dependency graph.
- Keep full-stack example as evidence, not universal architecture recommendation.
