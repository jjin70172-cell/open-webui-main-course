# Lab 26: The Prebound Method Pattern (Structural)

## Objectives
- Understand how binding a method to a local name avoids repeated attribute lookup.
- Use `functools.partial` to prebind arguments.
- Measure the performance difference on a hot loop.

## Background
The Prebound Method pattern binds an instance method to a local variable (or uses `functools.partial`) so that tight loops and callback registrations skip repeated dynamic lookup. It improves clarity and can improve performance.

## Materials
- Lesson: `docs/structural_prebound_method.md`
- Reference implementation: `patterns/structural/prebound_method.py`

## Task Overview
Run the benchmark, interpret the timings, then apply prebinding in a callback scenario.

## Step-by-Step Instructions
1. Open `patterns/structural/prebound_method.py` and review the three techniques shown: dynamic `getattr` lookup, local prebinding, and `functools.partial`.
2. Run the script:
   ```bash
   python patterns/structural/prebound_method.py
   ```
3. Record the two timings and note which approach is faster on your machine (results vary; the difference is small for tiny workloads).
4. Increase the task list to 100,000 entries and rerun; observe how the gap changes.
5. Write an event dispatcher that registers prebound methods in a dictionary (`{"text": proc.process_text, ...}`) and dispatches tasks through it.

## Expected Output
Processing messages for each task, followed by two timing lines similar to:
```text
Time without prebinding: 0.000123 seconds
Time with prebinding: 0.000045 seconds
```

## Exercises
1. Explain in your own words why `proc.process_text` evaluates the lookup once while `getattr(proc, "process_text")` inside a loop evaluates it every iteration.
2. Use `partial` to prebind both the method and a prefix argument; show the resulting call site.
3. Challenge: profile the loop with `cProfile` and identify where the lookup cost appears.

## Common Pitfalls
- Prebinding too early when the target object may be replaced later; the bound reference keeps pointing at the old object.
- Optimizing code that is not a measured bottleneck; profile first.
- Confusing prebound methods with closures that capture loop variables by reference.

## Deliverables
- Your timing table for the original and the 100,000-task run.
- The dictionary-based dispatcher using prebound methods.
