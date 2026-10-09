# Package layout

A worked example for a task-tracking app with four features:

- `tasks` has all three layers.
- `projects` has all three layers and depends on `tasks_domain`.
- `auth` is headless, with domain and data only.
- `dashboard` is presentation only and composes `tasks_domain` and `projects_domain`.

## Tree

```text
tasks_repo/
  pubspec.yaml
  apps/
    tasks_app/
      lib/
        main_development.dart
        main_production.dart
        bootstrap.dart
        app/
          app.dart
          app_dependencies.dart     # builds data implementations, exposes domain interfaces
          router.dart               # creates screen modules and passes navigation callbacks
      test/
  features/
    tasks/
      tasks_domain/
        lib/
          tasks_domain.dart         # barrel
          src/
            models/task.dart
            repositories/tasks_repository.dart
        test/src/
      tasks_data/
        lib/
          tasks_data.dart
          src/
            data_sources/tasks_local_data_source.dart
            mappers/task_mapper.dart
            repositories/drift_tasks_repository.dart
        test/src/
      tasks_presentation/
        lib/
          tasks_presentation.dart   # barrel for every screen
          task_list.dart            # entry point for one screen
          src/
            task_list/
              bloc/task_list_cubit.dart
              bloc/task_list_state.dart
              views/task_list_view.dart
              task_list_module.dart
            task_detail/
              ...
        test/src/
    projects/
      projects_domain/  projects_data/  projects_presentation/
    auth/
      auth_domain/  auth_data_firebase/
    dashboard/
      dashboard_presentation/
  shared/
    app_database/                   # database schema and migrations, no feature mapping
    app_ui/                         # theme and reusable widgets
    app_l10n/                       # ARB files and generated localizations
```

- Put implementation under `lib/src/` and export the public API from the barrel at `lib/<package>.dart`.
  The `implementation_imports` lint then flags any import of another package's `src/`.
- Give each package its own `test/` that mirrors `lib/src/`.
- Keep test helpers inside the package that uses them.
  Add a shared testing package only when a second package needs the same helper.
- A shared database package owns the schema and migrations.
  Each feature's data package owns the mapping from rows to its domain models.

## Workspace root

```yaml
name: tasks_workspace
publish_to: none

environment:
  sdk: ^3.6.0

workspace:
  - apps/tasks_app
  - features/auth/auth_domain
  - features/auth/auth_data_firebase
  - features/dashboard/dashboard_presentation
  - features/projects/projects_domain
  - features/projects/projects_data
  - features/projects/projects_presentation
  - features/tasks/tasks_domain
  - features/tasks/tasks_data
  - features/tasks/tasks_presentation
  - shared/app_database
  - shared/app_l10n
  - shared/app_ui
```

Globs such as `- features/*/*` need Dart 3.11 or later.

## Member pubspecs

Every member declares `resolution: workspace` and an SDK constraint of `^3.6.0` or higher.
The `dependencies` list is the architecture: a dependency that is not listed cannot be imported.

```yaml
# features/tasks/tasks_domain/pubspec.yaml
name: tasks_domain
publish_to: none
environment:
  sdk: ^3.6.0
resolution: workspace

dependencies:
  meta: ^1.16.0

dev_dependencies:
  test: ^1.26.3
  very_good_analysis: ^10.3.0
```

```yaml
# features/tasks/tasks_data/pubspec.yaml
name: tasks_data
publish_to: none
environment:
  sdk: ^3.6.0
resolution: workspace

dependencies:
  app_database:
    path: ../../../shared/app_database
  tasks_domain:
    path: ../tasks_domain

dev_dependencies:
  mocktail: ^1.0.5
  test: ^1.26.3
  very_good_analysis: ^10.3.0
```

```yaml
# features/tasks/tasks_presentation/pubspec.yaml
name: tasks_presentation
publish_to: none
environment:
  sdk: ^3.6.0
resolution: workspace

dependencies:
  app_l10n:
    path: ../../../shared/app_l10n
  app_ui:
    path: ../../../shared/app_ui
  flutter:
    sdk: flutter
  flutter_bloc: ^9.1.1
  tasks_domain:
    path: ../tasks_domain

dev_dependencies:
  bloc_test: ^10.0.0
  flutter_test:
    sdk: flutter
  mocktail: ^1.0.5
  very_good_analysis: ^10.3.0
```

`tasks_presentation` has no `tasks_data` entry, so a widget that imports a data source fails analysis.

## Domain interface

```dart
// features/tasks/tasks_domain/lib/src/repositories/tasks_repository.dart
abstract interface class TasksRepository {
  Stream<List<Task>> watchTasks();

  Future<void> complete(TaskId id);
}
```

## Screen module

```dart
// features/tasks/tasks_presentation/lib/src/task_list/task_list_module.dart
class TaskListModule extends StatelessWidget {
  const TaskListModule({
    required this.tasksRepository,
    required this.onOpenTask,
    super.key,
  });

  final TasksRepository tasksRepository;
  final ValueChanged<TaskId> onOpenTask;

  @override
  Widget build(BuildContext context) {
    return BlocProvider(
      create: (_) => TaskListCubit(tasksRepository)..load(),
      child: TaskListView(onOpenTask: onOpenTask),
    );
  }
}
```

The module is the only place this screen's cubit is provided, so `context.read<TaskListCubit>()` inside `TaskListView` always finds it.

## Composition root

```dart
// apps/tasks_app/lib/app/app_dependencies.dart
final class AppDependencies {
  const AppDependencies({required this.tasksRepository});

  final TasksRepository tasksRepository;

  static Future<AppDependencies> create() async {
    final database = await AppDatabase.open();
    return AppDependencies(tasksRepository: DriftTasksRepository(database));
  }
}
```

```dart
// apps/tasks_app/lib/app/router.dart
GoRouter buildRouter(AppDependencies dependencies) => GoRouter(
  routes: [
    GoRoute(
      path: '/tasks',
      builder: (context, state) => TaskListModule(
        tasksRepository: dependencies.tasksRepository,
        onOpenTask: (id) => context.go('/tasks/${id.value}'),
      ),
    ),
  ],
);
```

The app is the only package that imports both `tasks_data` and `tasks_presentation`.

## Pitfalls

- Pub resolves one version of each dependency for the whole workspace, so a version conflict in one package blocks every package.
- Declare a `dependency_overrides` entry once, in the root `pubspec.yaml`.
- `dart pub get` fails when a `pubspec.yaml` that is not a workspace member sits in a directory between the root and a member.
- Run code generation such as `build_runner` inside the package that owns the generated files, with `build_runner` in that package's `dev_dependencies`.
- A feature that only wraps a single repository call does not need a use case class.
  Add use cases when a rule combines several repositories.
