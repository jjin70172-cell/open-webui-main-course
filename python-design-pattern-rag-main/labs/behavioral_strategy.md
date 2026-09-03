# Lab 08: The Strategy Pattern (Behavioral)

## Objectives
- Understand how a family of interchangeable algorithms can be selected at runtime.
- Replace conditional branching with pluggable strategy objects.
- Add a new strategy without modifying the context.

## Background
The Strategy pattern defines a set of algorithms behind a common interface so the client can swap them at runtime. The context delegates the work to whichever strategy it currently holds.

## Materials
- Lesson: `docs/behavioral_strategy.md`
- Reference implementation: `patterns/behavioral/strategy.py`

## Task Overview
Run the sorting demo with three strategies, then implement a strategy of your own.

## Step-by-Step Instructions
1. Open `patterns/behavioral/strategy.py` and identify the strategy interface, the three concrete strategies, and the `SortContext`.
2. Before running, compute the expected results for the data `[5, 3, 9, 1, 3, 9]` under ascending, descending, and unique sorting.
3. Run the script and verify:
   ```bash
   python patterns/behavioral/strategy.py
   ```
4. Implement `TopThreeStrategy` that returns the three largest values in descending order.
5. Swap it into the context with `set_strategy` and verify the result `[9, 9, 5]`.

## Expected Output
```text
Ascending: [1, 3, 3, 5, 9, 9]
Descending: [9, 9, 5, 3, 3, 1]
Unique: [1, 3, 5, 9]
```

## Exercises
1. Refactor a real `if/elif` chain of your choice (for example a discount calculator) into strategies.
2. Make `SortContext` accept a default strategy so the constructor argument becomes optional.
3. Challenge: let strategies be registered by name and selected from a string at runtime.

## Common Pitfalls
- Creating many tiny strategy classes for trivial one-line differences; sometimes a function is enough.
- Forgetting that strategies should be interchangeable: if the client must know which strategy is active, the abstraction leaks.
- Confusing Strategy with State: strategies are chosen by the client and do not switch themselves.

## Deliverables
- The script extended with `TopThreeStrategy` and its verified output.
- A one-paragraph comparison of Strategy versus State.
