# Lab 19: The Adapter Pattern (Structural)

## Objectives
- Understand how an adapter translates an incompatible interface into the one the client expects.
- Identify Target, Adaptee, and Adapter roles.
- Write an adapter for a new third-party-style class.

## Background
The Adapter pattern wraps an object with an incompatible interface and exposes it through the interface the client already uses. The client never needs to know about the adaptee.

## Materials
- Lesson: `docs/structural_adapter.md`
- Reference implementation: `patterns/structural/adapter.py`

## Task Overview
Run the demo, explain the translation performed by the adapter, then write your own adapter.

## Step-by-Step Instructions
1. Open `patterns/structural/adapter.py` and identify `Target` (expected interface), `Adaptee` (incompatible interface), and `Adapter` (translator).
2. Run the script:
   ```bash
   python patterns/structural/adapter.py
   ```
3. Explain exactly what the adapter does to the adaptee's reversed string before returning it.
4. Write a `FahrenheitSensor` class with `read_fahrenheit()` and a `CelsiusAdapter` that exposes `request()` returning the temperature in Celsius, matching the `Target` interface.
5. Use client code that accepts only `Target` objects and verify both the original target and your adapter work through the same call.

## Expected Output
```text
Target: The default behavior.
Adaptee: .eetpadA eht fo roivaheb laicepS
Adapter: (TRANSLATED) Special behavior of the Adaptee.
```

## Exercises
1. Implement a class adapter (inherit from both `Target` and `Adaptee`) and compare it with the object adapter used here.
2. Adapt a real Python library object (for example a file-like object or `dict`) to a small custom interface of your own.
3. Challenge: build a two-way adapter where changes through the adapter are written back to the adaptee.

## Common Pitfalls
- Putting business logic inside the adapter; it should translate, not transform behavior beyond the interface mismatch.
- Adapting too early: if you control both interfaces, changing one is often simpler.
- Creating adapter chains (adapter of an adapter), which obscure the data flow.

## Deliverables
- The run transcript of the reference demo.
- Your `CelsiusAdapter` implementation with a client that uses it through the `Target` interface.
