# Lab 24: The Flyweight Pattern (Structural)

## Objectives
- Understand how sharing common (intrinsic) state across many objects saves memory.
- Separate intrinsic state from extrinsic (context-specific) state.
- Verify reuse through the flyweight factory's cache.

## Background
The Flyweight pattern minimizes memory usage by sharing as much data as possible between similar objects. Shared intrinsic state lives in the flyweight; unique extrinsic state is passed in by the client at call time.

## Materials
- Lesson: `docs/structural_flyweight.md`
- Reference implementation: `patterns/structural/flyweight.py`

## Task Overview
Run the car demo, count creations versus reuses, then simulate a larger fleet to show the savings.

## Step-by-Step Instructions
1. Open `patterns/structural/flyweight.py` and identify the intrinsic state (`shared_state`, the car type) and the extrinsic state (the license plate passed to `operation`).
2. Run the script:
   ```bash
   python patterns/structural/flyweight.py
   ```
3. Count how many flyweights were created versus reused, and verify with `list_flyweights`.
4. Simulate a fleet of 1000 cars drawn from only 5 car types; print the number of flyweight objects in the cache at the end.
5. Explain in one paragraph how memory scales with fleet size versus with the number of car types.

## Expected Output
```text
Factory: Creating new Flyweight for 'Sedan'
Flyweight: Shared [Sedan] | Unique [ABC-123]
Factory: Creating new Flyweight for 'SUV'
Flyweight: Shared [SUV] | Unique [XYZ-999]
Factory: Reusing existing Flyweight for 'Sedan'
Flyweight: Shared [Sedan] | Unique [DEF-456]
Factory: 2 flyweight(s) in cache:
 - Sedan
 - SUV
```

## Exercises
1. Add a `Truck` type and mixed fleet data; verify the cache grows by exactly one entry.
2. Compare object counts with `sys.getsizeof` or a simple counter between a flyweight design and a naive per-car object design.
3. Challenge: make the factory thread-safe and explain which operation needs protection.

## Common Pitfalls
- Storing extrinsic state inside the flyweight; it must stay shareable and therefore immutable per key.
- Applying flyweight prematurely; it only pays off with large numbers of objects sharing large state.
- Forgetting to externalize the unique data, which corrupts other clients' views.

## Deliverables
- The creation/reuse counts for the demo run.
- Your 1000-car simulation result and the memory-scaling explanation.
