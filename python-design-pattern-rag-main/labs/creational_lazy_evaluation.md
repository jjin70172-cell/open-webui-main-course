# Lab 16: Lazy Evaluation (Creational)

## Objectives
- Understand how deferring expensive computation until first use saves time and resources.
- Use a decorator to turn a method into a cached, lazily computed property.
- Verify that the computation happens exactly once.

## Background
Lazy evaluation delays an expensive operation until its result is actually needed, then caches the result. The `lazy_property` decorator stores the value under `_lazy_<name>` after the first computation.

## Materials
- Lesson: `docs/creational_lazy_evaluation.md`
- Reference implementation: `patterns/creational/lazy_evaluation.py`

## Task Overview
Run the report generator demo, observe that the first access is slow and the second is instant, then add a second lazy property.

## Step-by-Step Instructions
1. Open `patterns/creational/lazy_evaluation.py` and study the `lazy_property` decorator: note where the cache attribute is checked and set.
2. Run the script:
   ```bash
   python patterns/creational/lazy_evaluation.py
   ```
3. Observe the three phases: object creation (no computation yet), first access (computes, ~2 seconds), second access (cached, instant).
4. Confirm the message `Computing 'summary'...` appears exactly once.
5. Add a lazy property `top_ten` that returns the ten largest values; access it twice and verify it also computes only once.

## Expected Output
```text
Step 1: Object created, report not yet generated.
Step 2: Accessing the summary for the first time (will compute)...
Computing 'summary'...
Report Summary:
 - Total: 1000000
 - Min: 1
 - Max: 1000000
 - Average: 500000.5
Step 3: Accessing the summary again (should be cached)...
Report Summary:
 ...
```
(with no second `Computing` message)

## Exercises
1. Add an `invalidate` method that deletes the cache attribute so the next access recomputes.
2. Measure memory or time savings: create 1000 `ReportGenerator` objects and never access `summary`; discuss what was avoided.
3. Challenge: make the decorator thread-safe so two threads cannot trigger the computation twice.

## Common Pitfalls
- Forgetting that the cached value is stored on the instance; two instances compute independently.
- Using lazy evaluation for cheap operations, adding overhead without benefit.
- Returning mutable cached objects that callers can accidentally modify.

## Deliverables
- A transcript of the run showing the computation happened exactly once.
- The additional `top_ten` lazy property with its verification.
