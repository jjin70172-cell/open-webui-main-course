# Lab 17: The Prototype Pattern (Creational)

## Objectives
- Understand object creation by cloning an existing prototype instead of calling constructors.
- Distinguish deep copy from shallow copy behavior.
- Use cloning when object creation is costly or configuration-heavy.

## Background
The Prototype pattern creates new objects by copying a prototypical instance. In Python, `copy.deepcopy` is the typical mechanism, ensuring the clone is fully independent of the original.

## Materials
- Lesson: `docs/creational_prototype.md`
- Reference implementation: `patterns/creational/prototype.py`

## Task Overview
Clone and modify a shape without affecting the original, then explore the shallow/deep copy difference.

## Step-by-Step Instructions
1. Open `patterns/creational/prototype.py` and review `Prototype.clone` and the `Shape` class.
2. Run the script:
   ```bash
   python patterns/creational/prototype.py
   ```
3. Verify the original keeps `color=blue` and `position=(10, 20)` while the clone moved and turned green.
4. Change `clone` to use `copy.copy` (shallow copy) and modify the clone's nested state (for example replace `position` with a list and mutate it); observe whether the original is affected.
5. Restore `deepcopy` and add a `Rectangle` subclass with `width`/`height`; confirm cloning works for it without writing new clone code.

## Expected Output
```text
Original: Shape(color=blue, position=(10, 20))
Cloned: Shape(color=green, position=(15, 15))
Original after cloning: Shape(color=blue, position=(10, 20))
```

## Exercises
1. Add a prototype registry (a dictionary of named prototypes) and create objects by name.
2. Benchmark constructor-based creation versus cloning for an object with an expensive `__init__`.
3. Challenge: implement `clone` with `__class__(**self.__dict__)` and find a case where it breaks (hint: nested mutable attributes).

## Common Pitfalls
- Using shallow copy when objects contain nested mutable structures, which silently shares state between original and clone.
- Forgetting that circular references need `deepcopy` support.
- Cloning when a plain constructor call would be cheaper and clearer.

## Deliverables
- The run transcript showing clone independence.
- A short report on what changed when you switched to shallow copy.
