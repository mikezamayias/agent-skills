# Customization Matrix

Prefer the project's existing choices. Use this matrix when creating a new app or when the user asks for architecture recommendations.

## Required User Decisions

Ask or confirm these choices before scaffolding greenfield work or making architecture-level changes:

- State management: BLoC/Cubit, Bloc with events, Riverpod, Provider/ChangeNotifier, or existing project convention.
- Backend: REST, GraphQL, Firebase, Supabase, custom backend, local-only/mock data, or existing backend.
- Frontend design system: Material 3, adaptive Material/Cupertino, Shadcn-style Flutter components, custom design system, or existing project convention.

When the repo already has clear conventions, present the inferred answer and ask whether to follow it.

| Concern              | Default                                     | Use Default When                                                       | Consider Alternative When                                                                       |
| -------------------- | ------------------------------------------- | ---------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| State management     | BLoC/Cubit                                  | Feature workflows are event-light and testability matters              | Riverpod is already standard in the repo, or many derived providers are required                |
| Backend              | Custom REST via Dio                         | API shape is controlled and feature endpoints are conventional         | Firebase/Supabase for managed backend, GraphQL for graph-shaped data, local-only for prototypes |
| Dependency injection | GetIt                                       | Constructor injection with a simple service locator is enough          | Injectable is already used, or registration boilerplate is large                                |
| UI system            | Adaptive Material/Cupertino with app tokens | Mobile app needs native platform feel                                  | Material-only for simpler products, Shadcn-style components for a unified custom design         |
| Routing              | GoRouter                                    | Declarative routes and deep links are needed                           | AutoRoute is already used or strongly typed generated routes are required                       |
| Serialization        | FlatBuffers                                 | Large/frequent payloads, random access, low allocation, controlled API | Protobuf for simpler binary contracts, JSON for third-party APIs                                |
| Local storage        | drift (SQLite)                              | Caches, relational queries, and migrations need one typed store        | ObjectBox for object database needs, and never new Hive code                                    |
| Localization         | Flutter l10n with ARB                       | Built-in Flutter tooling is enough                                     | Slang for stronger generated APIs, Easy Localization for simpler JSON/YAML files                |
| Testing              | flutter_test, bloc_test, mocktail           | Null-safe mocks and Cubit/BLoC state tests are needed                  | Mockito only when the project already depends on generated mocks                                |
| Logging              | logger                                      | Lightweight console logging is enough                                  | Talker when in-app log viewing or Dio/BLoC integrations are desired                             |

## State Management

Default to one Cubit per screen or feature workflow. Inject use cases through constructors. Keep Cubit states serializable or mappable only when the project benefits from generated equality and `copyWith`.

Use Bloc instead of Cubit when there are several distinct user events, event transformers, or complex concurrency rules.

Use Riverpod only when it is already a project convention or the feature is mostly composed from many derived pieces of shared state.

## Backend Choice

Use REST with Dio when endpoints are resource-oriented, the API is already available, or the project needs explicit control over interceptors, retries, auth, and binary response handling.

Use Firebase when the product benefits from managed auth, Firestore, storage, functions, push, and realtime sync with minimal custom backend code.

Use Supabase when the product benefits from Postgres, row-level security, generated APIs, auth, storage, and SQL-backed reporting.

Use GraphQL when screens compose data from many related entities and the backend schema is already maintained.

Use local-only or mock data only for prototypes, offline-first experiments, or when the user explicitly asks to defer backend integration.

## Dependency Injection

Use a single registration module, commonly `dependencies_injection.dart`.

Register:

- External services and clients as singletons.
- Repositories and data sources as lazy singletons.
- Cubits as factories unless the project intentionally shares Cubit instances.

Always provide a reset path for tests.

## Serialization Choice

Use FlatBuffers only when its complexity is justified:

- The app reads large lists or binary payloads.
- The app only needs selective field access.
- Memory allocation and parse time matter.
- The API can serve `application/x-flatbuffers`.
- The team accepts schema generation and inside-out builders.

Use Protobuf when the team wants binary payloads with simpler APIs and broader tooling.

Use JSON when the backend is third-party, payloads are small, or inspectability matters more than binary performance.

## Storage Choice

Default to drift.
Store raw FlatBuffer bytes in a `blob()` column keyed by ID when the cache is mostly by key and values mirror server responses.
Use drift tables and queries when the product needs joins, sorting, filtering, and migrations.
On Flutter web, drift needs `sqlite3.wasm` and the drift worker in `web/`, as its web setup page describes.

Choose ObjectBox when object graph queries and high local database throughput are more important than SQL.

If the project uses Hive, follow the Hive Projects section in `SKILL.md` and propose migrating to drift.

## UI and Routing

Keep UI components separated:

- Shared design primitives in `lib/core/widgets/` or a design-system package.
- Feature-specific components in `lib/features/<feature>/presentation/widgets/`.
- Full screens in `pages/`.

Use route path enums or constants rather than scattered string literals.

## Testing Choices

Use binary fixtures in `test/fixtures/` for FlatBuffer data-layer tests. Generate fixtures with the same builders used by production code when possible.

Mock only across layer boundaries:

- Use case tests mock repositories.
- Repository tests mock data sources.
- Cubit tests mock use cases.
- Widget tests mock Cubits or inject fake use cases through the established DI pattern.
