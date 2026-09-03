# Lab 14: Method Chaining / Fluent Builder (Creational)

## Objectives
- Build complex objects with a readable, chainable fluent interface.
- Combine validation, undo, and final `build` verification in one builder.
- Trigger and handle validation errors deliberately.

## Background
Method chaining (fluent interface) lets each configuration method return the builder itself, so calls can be chained into a single readable expression. The `PizzaBuilder` demo adds input validation and an undo stack on top.

## Materials
- Lesson: `docs/creational_chaining.md`
- Reference implementation: `patterns/creational/chaining.py`

## Task Overview
Run the pizza demo, then deliberately break the rules to see how validation responds, and use `undo` to recover.

## Step-by-Step Instructions
1. Open `patterns/creational/chaining.py` and check which methods return `self` and where `_save_state` is called.
2. Run the script:
   ```bash
   python patterns/creational/chaining.py
   ```
3. Write your own chain that builds a small thin-crust pizza with one topping and default sauce; print the resulting dictionary.
4. Deliberately trigger each kind of validation error and record the exception messages:
   - `set_size("giant")`
   - `add_topping("mushrooms")` twice
   - `build()` without setting size and crust
5. Build a chain, call `undo()` after a mistake, and verify the builder returns to its previous state.

## Expected Output
The demo prints a dictionary such as:
```text
{'size': 'large', 'crust': 'stuffed', 'toppings': ['pepperoni', 'mushrooms'], 'cheese': False, 'sauce': 'bbq'}
```

## Exercises
1. Add `set_extra_cheese` and validate that it can only be used when cheese is enabled.
2. Add a `__str__` method to render the built pizza as a human-readable sentence.
3. Challenge: implement `redo` alongside `undo`.

## Common Pitfalls
- Forgetting `return self` in one method silently breaks the chain (the next call fails on `None`).
- Validating only at the end instead of at each step, which produces confusing error messages late.
- Saving state *after* the mutation instead of before it, which makes `undo` restore the wrong snapshot.

## Deliverables
- Your own valid pizza chain and its output.
- A table of the three validation errors you triggered with their messages.
- A demonstration of `undo` recovering from a mistake.
