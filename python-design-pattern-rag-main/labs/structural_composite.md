# Lab 21: The Composite Pattern (Structural)

## Objectives
- Represent part-whole hierarchies as trees and treat leaves and composites uniformly.
- Build nested structures through the shared `Component` interface.
- Discuss safety versus transparency of the `add`/`remove` operations.

## Background
The Composite pattern composes objects into tree structures. Clients call the same `operation` on a single leaf or on a deep composite; composites aggregate their children's results.

## Materials
- Lesson: `docs/structural_composite.md`
- Reference implementation: `patterns/structural/composite.py`

## Task Overview
Run the demo tree, build a deeper tree of your own, then compute an aggregate over it.

## Step-by-Step Instructions
1. Open `patterns/structural/composite.py` and review `Component`, `Leaf`, and `Composite`; note how `Composite.operation` aggregates children.
2. Run the script:
   ```bash
   python patterns/structural/composite.py
   ```
3. Build your own tree: a root composite containing two composites and three leaves spread across levels; print its `operation`.
4. Use `is_composite` to write a `count_leaves(component)` function that recursively counts leaves in any tree.
5. Verify your count against the tree you built.

## Expected Output
```text
Composite(Group2)[Composite(Group1)[Leaf(A) + Leaf(B)] + Leaf(C)]
```

## Exercises
1. Add a `NumericLeaf` with a value and implement a `total` operation that sums values through the tree.
2. Remove `add`/`remove` from the `Component` base class so only composites expose them (safety over transparency); update the client code and discuss what breaks.
3. Challenge: implement an iterator over the tree that yields leaves depth-first.

## Common Pitfalls
- Forgetting that leaf `add`/`remove` do nothing silently; decide whether they should raise instead.
- Deep recursion on very deep trees; consider an iterative traversal.
- Allowing a component to be added to two parents without a policy, which creates confusing structures.

## Deliverables
- Your custom tree and its aggregated output.
- The `count_leaves` function with a verified result.
