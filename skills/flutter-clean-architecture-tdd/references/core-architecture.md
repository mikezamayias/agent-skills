# Core Architecture

Use feature-first Clean Architecture. Each feature owns its data, domain, presentation, and tests.

```text
lib/
  core/
    api/             # clients, interceptors, request wrappers
    config/          # app configuration and DI setup
    constants/       # colors, typography, icons, tokens
    enums/           # shared enums
    error/           # failures and exceptions
    extensions/      # Dart and Flutter extensions
    fbs/             # shared FlatBuffers schemas and generated code
    keys/            # storage keys
    localization/    # ARB files and generated l10n
    routes/          # navigation
    services/        # local services and adapters
    usecases/        # base use case types
    utils/           # helpers, isolate parsing
    widgets/         # shared UI components
  features/
    <feature>/
      data/
        implements/  # repository implementations
        models/      # generated DTO accessors or data-only models
        sources/     # remote and local data sources
      domain/
        entities/    # immutable business models
        repositories/ # repository contracts
        usecases/    # single-responsibility business logic
      presentation/
        cubit/       # state management
        pages/       # screens
        widgets/     # feature components
  main.dart
  root_app.dart
  dependencies_injection.dart

test/
  core/
  features/
  fixtures/
  helpers/
  integration/
```

## Layer Contracts

- Domain depends on no Flutter, network, storage, generated DTO, or package-specific infrastructure types.
- Repository interfaces live in domain. Repository implementations live in data.
- Data sources return raw transport/storage results or data-layer models; repositories convert them to entities and failures.
- Presentation depends on use cases and entities, not repositories directly unless the existing codebase already uses that shortcut.
- Shared app concerns belong in `core/`; feature-specific code stays inside the feature.

## Data Flow

```text
API or cache bytes -> generated FlatBuffer accessor -> repository -> entity -> use case -> Cubit -> UI
```

Never expose generated FlatBuffer classes from repository public APIs, Cubit states, widgets, or domain entities.

## TDD Method

Use red-green-refactor:

1. Red: write a failing test that describes behavior.
2. Green: add the smallest implementation that passes.
3. Refactor: improve names, boundaries, and duplication while tests stay green.

Use the testing pyramid:

- Unit tests: entities, use cases, repositories, data sources, Cubits.
- Widget tests: rendering, interactions, navigation surface.
- Integration tests: complete feature flows and critical wiring.

Use the AAA pattern in tests: Arrange, Act, Assert.

## Entity Pattern

Use `dart_mappable` for domain entities when adding new models:

```dart
@MappableClass()
class UserEntity with UserEntityMappable {
  const UserEntity({
    required this.id,
    required this.name,
    required this.email,
    required this.createdAt,
  });

  final int id;
  final String name;
  final String email;
  final DateTime createdAt;
}
```

Prefer normal Dart classes with generated equality and `copyWith` over DTO-shaped domain objects.

## FlatBuffers Pattern

Use FlatBuffers when the app controls both sides of the API, handles large or frequent payloads, needs low allocation, or benefits from random access. Avoid FlatBuffers for small JSON-only APIs unless the project explicitly requires it.

Schema files live under `lib/core/fbs/` unless they are truly feature-private.

```fbs
namespace App.User;

table User {
  id: int64;
  name: string;
  email: string;
  created_at: int64;
}

table UsersResponse {
  users: [User];
  total_count: int32;
}

root_type UsersResponse;
```

Generate Dart accessors with:

```bash
flatc --dart -o lib/core/fbs/generated/ lib/core/fbs/*.fbs
```

Convert at the boundary:

```dart
extension UserFbReader on User {
  UserEntity toEntity() => UserEntity(
        id: id,
        name: name ?? '',
        email: email ?? '',
        createdAt: DateTime.fromMillisecondsSinceEpoch(createdAt),
      );
}
```

FlatBuffers are built inside-out: create strings and child objects before parent tables. Keep builder logic in data-layer mappers or extensions.

## Repository Pattern

Repositories orchestrate cache/network selection, convert transport/storage data to entities, and return `Either<Failure, T>`.

```dart
class UserRepositoryImpl implements UserRepository {
  UserRepositoryImpl(this._remote, this._local);

  final UserRemoteDataSource _remote;
  final UserLocalDataSource _local;

  @override
  Future<Either<Failure, UserEntity>> getUser(int id) async {
    final cachedBytes = await _local.getCachedUserBytes(id);
    if (cachedBytes != null) {
      return Right(User(cachedBytes).toEntity());
    }

    final result = await _remote.getUser(id);
    return result.fold(
      Left.new,
      (bytes) async {
        await _local.cacheUserBytes(id, bytes);
        return Right(User(bytes).toEntity());
      },
    );
  }
}
```

Adapt examples to the generated FlatBuffer API in the actual project.

## Failure and State

Use a small failure hierarchy:

```dart
abstract class Failure {
  const Failure(this.message);
  final String? message;
}

class ServerFailure extends Failure {
  const ServerFailure(super.message);
}

class CacheFailure extends Failure {
  const CacheFailure(super.message);
}

class ParseFailure extends Failure {
  const ParseFailure(super.message);
}
```

Use sealed `dart_mappable` states for Cubits when the codebase already uses generated states. Emit loading, success, empty, and failure states through `Either.fold`.

## Code Generation

Regenerate when schemas or generated classes change:

```bash
flatc --dart -o lib/core/fbs/generated/ lib/core/fbs/*.fbs
dart run build_runner build
```
