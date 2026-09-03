# Lab 23: The Facade Pattern (Structural)

## Objectives
- Provide a simplified interface over a set of subsystem classes.
- Reduce coupling between client code and complex subsystems.
- Extend the facade when the subsystem grows.

## Background
The Facade pattern hides the complexity of a subsystem behind a single high-level interface. Clients call one method on the facade instead of orchestrating many subsystem calls themselves.

## Materials
- Lesson: `docs/structural_facade.md`
- Reference implementation: `patterns/structural/facade.py`

## Task Overview
Run the facade demo, compare client code with and without the facade, then add a third subsystem.

## Step-by-Step Instructions
1. Open `patterns/structural/facade.py` and identify the two subsystems and the `Facade.operation` that orchestrates them.
2. Run the script:
   ```bash
   python patterns/structural/facade.py
   ```
3. Write client code that achieves the same result *without* the facade by calling subsystem methods directly; compare the two clients' line counts and coupling.
4. Add `SubsystemC` with an `operation_c1` method and include it in `Facade.operation`.
5. Run again and verify the facade output now includes the third subsystem's message.

## Expected Output
```text
SubsystemA: Ready!
SubsystemA: Go!
SubsystemB: Fire!
```

## Exercises
1. Add a second facade method (for example `shutdown`) that calls a different combination of subsystem operations.
2. Discuss where the facade should live architecturally if subsystems are separate packages.
3. Challenge: compare Facade with Adapter and Mediator in a three-row table (purpose, direction of communication, what changes).

## Common Pitfalls
- Turning the facade into a god object that contains business logic instead of delegating.
- Forcing every client through the facade when some advanced clients legitimately need direct subsystem access.
- Letting the facade leak subsystem types into its own interface.

## Deliverables
- The side-by-side comparison of facade vs direct client code.
- The extended facade including `SubsystemC` with verified output.
