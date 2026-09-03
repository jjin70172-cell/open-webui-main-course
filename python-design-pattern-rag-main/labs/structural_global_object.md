# Lab 25: The Global Object Pattern (Structural)

## Objectives
- Understand module-level shared objects as a lightweight alternative to enforced singletons.
- Split a simulated single-file example into real modules.
- Discuss the trade-offs of globally shared state.

## Background
The Global Object pattern exposes a shared object through a module-level declaration. Other modules import the same instance, giving centralized access to configuration or registries without a strict singleton mechanism.

## Materials
- Lesson: `docs/structural_global_object.md`
- Reference implementation: `patterns/structural/global_object.py`

## Task Overview
The reference file simulates three modules (`config.py`, `service.py`, `main.py`) inside one file for readability, so running it directly raises `ModuleNotFoundError`. Your task is to split it into the three real files and make it run.

## Step-by-Step Instructions
1. Open `patterns/structural/global_object.py` and locate the three commented sections: `# config.py`, `# service.py`, and `# main.py`.
2. Confirm the failure mode by running it:
   ```bash
   python patterns/structural/global_object.py
   ```
3. Create a scratch folder (for example `lab25/`) and split the file into `config.py` (`AppConfig` and `global_config`), `service.py` (the two service functions), and `main.py` (the `main` function and entry point).
4. Remove the now-unneeded in-function imports or keep them; run:
   ```bash
   python lab25/main.py
   ```
5. Verify that changes made in `main` (environment, debug mode, API key) are visible inside `service` through the shared object.

## Expected Output
```text
[Service] Running in production mode.
[Service] Debug mode is enabled.
[Service] Updated API key to: SECRET-123
[Main] Confirmed API key: SECRET-123
```

## Exercises
1. Add a `feature_flags` dictionary to `AppConfig` and toggle a flag from `main` that `service` reads.
2. Replace the global object with an explicitly passed dependency (constructor injection) and compare the two styles.
3. Challenge: write a unit test for `service.initialize_service` that resets `global_config` first; note why reset is necessary.

## Common Pitfalls
- Importing the module in different ways so Python creates two module instances with two different globals (for example running the same file as `__main__` and importing it as a module).
- Hidden dependencies: readers cannot see which functions rely on the global without searching.
- Mutable global state persisting across tests; always reset it in test setup.

## Deliverables
- The three split files running successfully with the expected output.
- A short note on when a global object is acceptable versus when dependency injection is safer.
