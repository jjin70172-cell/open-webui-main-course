# Lab 12: The Borg (Monostate) Pattern (Creational)

## Objectives
- Understand how sharing `__dict__` gives many instances one shared state.
- Compare Borg with Singleton: shared state versus single identity.
- Add configuration keys to the shared configuration object.

## Background
The Borg pattern lets any number of instances exist but makes them all share the same internal state by assigning the class-level `_shared_state` dictionary to each instance's `__dict__`.

## Materials
- Lesson: `docs/creational_borg.md`
- Reference implementation: `patterns/creational/borg.py`

## Task Overview
Run the configuration demo, verify that state is shared while identity is not, then extend the configuration.

## Step-by-Step Instructions
1. Open `patterns/creational/borg.py` and study `Borg.__init__`: the single line `self.__dict__ = self._shared_state` is the whole trick.
2. Run the script:
   ```bash
   python patterns/creational/borg.py
   ```
3. Record the answers to the two final questions: are `config1` and `config2` the same object? Do they share state?
4. Add a `language` setting with default `"en"`: extend the one-time initialization block and `set_config`.
5. From a third `AppConfig` instance, change `language` and verify the change is visible through `config1`.

## Expected Output
```text
Are config1 and config2 the same object? No
Do they share the same state? Yes
```

## Exercises
1. Write a comparison script that creates both a Borg config and a Singleton config, then prints identity (`is`) and state-sharing results side by side.
2. Subclass `AppConfig` and check whether the subclass shares state with the parent class; explain the result.
3. Challenge: make the shared state copy-on-write or thread-safe with a lock, and discuss the cost.

## Common Pitfalls
- Assuming Borg restricts instantiation; it does not - only state is shared.
- Forgetting the one-time initialization guard, so defaults overwrite values set by other instances.
- Ignoring thread safety: a shared `__dict__` is global mutable state.

## Deliverables
- The extended configuration with the `language` key and observed shared behavior.
- A two-column comparison of Borg versus Singleton (identity, state, instantiation).
