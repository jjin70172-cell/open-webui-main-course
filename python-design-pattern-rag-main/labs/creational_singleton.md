# Lab 18: The Singleton Pattern (Creational)

## Objectives
- Understand how a metaclass can guarantee exactly one instance of a class.
- Verify single identity and shared state across references.
- Recognize the well-known drawbacks of singletons (testing, hidden global state).

## Background
The Singleton pattern ensures a class has only one instance and provides a global point of access to it. The reference implementation uses the `SingletonMeta` metaclass, which caches instances in `_instances`.

## Materials
- Lesson: `docs/creational_singleton.md`
- Reference implementation: `patterns/creational/singleton.py`

## Task Overview
Run the demo, verify identity and shared state, then explore how the metaclass behaves with multiple singleton classes.

## Step-by-Step Instructions
1. Open `patterns/creational/singleton.py` and study `SingletonMeta.__call__`: the instance is created only when the class is not yet in `_instances`.
2. Run the script:
   ```bash
   python patterns/creational/singleton.py
   ```
3. Verify that `a is b` holds and that increments through either reference are visible to both (final value `2`).
4. Define a second class `Logger(metaclass=SingletonMeta)` and confirm that each class gets its own single instance (`Singleton() is not Logger()` and two `Logger()` calls return the same object).
5. Write a short paragraph: why can this global shared state make unit testing harder?

## Expected Output
```text
Singleton value from 'a': 2
Singleton value from 'b': 2
```

## Exercises
1. Add a `reset` class method to `SingletonMeta` (for testing) that clears the cached instance, and write a unit test that uses it.
2. Compare this metaclass implementation with a module-level global instance; list one advantage of each.
3. Challenge: make the metaclass thread-safe with a lock and explain what race condition it prevents.

## Common Pitfalls
- Treating the singleton as a convenient global variable; hidden dependencies make code harder to reason about and test.
- Forgetting that constructor arguments are ignored after the first creation (the cached instance is returned regardless).
- Assuming singletons are safe across threads without explicit synchronization.

## Deliverables
- The run transcript plus your two-class experiment output.
- A short paragraph on singleton testability and one mitigation strategy.
