# Lab 09: The Template Method Pattern (Behavioral)

## Objectives
- Understand how an algorithm skeleton can fix the overall order while letting subclasses fill in the steps.
- Distinguish abstract steps, base (shared) steps, and optional hooks.
- Create a new subclass variant without touching the base class.

## Background
The Template Method pattern defines the structure of an algorithm in a base class and defers selected steps to subclasses. Subclasses redefine those steps without changing the algorithm's structure.

## Materials
- Lesson: `docs/behavioral_template_method.md`
- Reference implementation: `patterns/behavioral/template_method.py`

## Task Overview
Run both concrete variants, map each method of the template to its role, then add a third variant that overrides a hook.

## Step-by-Step Instructions
1. Open `patterns/behavioral/template_method.py` and classify every method called by `template_method` as base operation, required (abstract) operation, or hook.
2. Run the script and compare the two variants' outputs:
   ```bash
   python patterns/behavioral/template_method.py
   ```
3. Explain why `ConcreteClassB` prints an extra line compared with `ConcreteClassA`.
4. Create `ConcreteClassC` that overrides `hook_2` instead of `hook_1` and verify the output order still follows the template.
5. Discuss: what would happen if a subclass tried to reorder the steps? (Hint: it cannot, and that is the point.)

## Expected Output
```text
== A version ==
Base: Doing the bulk of the work (1)
ConcreteClassA: Implemented required_operation_1
Base: Doing the bulk of the work (2)
ConcreteClassA: Implemented required_operation_2

== B version ==
Base: Doing the bulk of the work (1)
ConcreteClassB: Implemented required_operation_1
Base: Doing the bulk of the work (2)
ConcreteClassB: Hook 1 overridden
ConcreteClassB: Implemented required_operation_2
```

## Exercises
1. Implement a real-world template such as a data pipeline: `extract -> validate -> transform -> load`, with `validate` as a hook that defaults to doing nothing.
2. Mark `template_method` as final-by-convention (document that subclasses must not override it) and explain why.
3. Challenge: add a hook that receives the intermediate result of the previous step.

## Common Pitfalls
- Letting subclasses override the template method itself, destroying the fixed algorithm order.
- Creating too many abstract steps, which burdens every subclass; prefer hooks with default behavior.
- Deep inheritance trees built on templates; keep the hierarchy shallow.

## Deliverables
- The method-role table for `template_method`.
- The `ConcreteClassC` variant with its observed output.
