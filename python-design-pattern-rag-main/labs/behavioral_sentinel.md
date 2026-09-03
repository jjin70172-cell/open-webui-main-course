# Lab 06: The Sentinel Object Pattern (Behavioral)

## Objectives
- Understand why a unique sentinel object can represent "no value" more precisely than `None`.
- Use sentinels to distinguish "argument not provided" from "argument explicitly set to `None`".
- Use a sentinel as an end-of-stream marker.

## Background
A sentinel is a unique, distinguishable object that signals a special condition. Because identity comparison (`is`) is used, a sentinel can never be confused with any legitimate user value, including `None`.

## Materials
- Lesson: `docs/behavioral_sentinel.md`
- Reference implementation: `patterns/behavioral/sentinel.py`

## Task Overview
Run the four demo scenarios, explain the behavioral difference between `MISSING` and `None`, then create a sentinel of your own.

## Step-by-Step Instructions
1. Open `patterns/behavioral/sentinel.py` and review the `Sentinel` class, the `MISSING` and `END_OF_STREAM` instances, and `process_items`.
2. Before running, predict the output of the three `process_items` calls (all items, limit of 2, and `None`).
3. Run the script and verify:
   ```bash
   python patterns/behavioral/sentinel.py
   ```
4. Trace how `consume_stream` stops when it encounters `END_OF_STREAM`.
5. Create your own sentinel `NOT_SET` and write a function `greet(name=NOT_SET)` that prints a default greeting when no name is provided but still accepts `None` as a valid (anonymous) input.

## Expected Output
The demo prints four sections: processing all items, processing up to 2 items, skipping because `max_items=None`, and stream consumption that stops at the `END_OF_STREAM` sentinel.

## Exercises
1. Rewrite `process_items` using a `None` default instead of `MISSING` and show a call where the behavior becomes ambiguous.
2. Add a `__bool__` method to `Sentinel` that always returns `False` and discuss whether this helps or hurts clarity.
3. Challenge: implement a small cache where `MISSING` distinguishes "key absent" from "key stored with value `None`".

## Common Pitfalls
- Comparing sentinels with `==` instead of `is`; identity is what guarantees uniqueness.
- Creating a new sentinel instance per call instead of reusing a module-level constant.
- Using `None` as a sentinel when `None` is also a valid user value.

## Deliverables
- Your prediction table for the three `process_items` scenarios, confirmed by the run.
- The `greet` function demonstrating `NOT_SET` versus `None`.
