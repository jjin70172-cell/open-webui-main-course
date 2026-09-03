# Lab 22: The Decorator Pattern (Structural)

## Objectives
- Add responsibilities to individual objects dynamically without affecting other objects of the same class.
- Stack multiple decorators and observe how order changes the result.
- Relate the pattern to Python's `@decorator` syntax.

## Background
The Decorator pattern wraps an object in decorator classes that share the component interface. Each decorator adds behavior before or after delegating to the wrapped object, keeping classes open for extension but closed for modification.

## Materials
- Lesson: `docs/structural_decorator.md`
- Reference implementation: `patterns/structural/decorator.py`

## Task Overview
Run the demo, stack decorators in different orders, then write a decorator with real behavior.

## Step-by-Step Instructions
1. Open `patterns/structural/decorator.py` and note that `Decorator` holds a `Component` and forwards `operation` to it.
2. Run the script:
   ```bash
   python patterns/structural/decorator.py
   ```
3. Wrap the component as `DecoratorB(DecoratorA(component))` and compare with `DecoratorA(DecoratorB(component))`; record both outputs.
4. Add `UpperDecorator` that uppercases the wrapped result.
5. Stack three decorators and verify the final string shows all layers applied in nesting order.

## Expected Output
The demo prints the plain component result, then results with `DecoratorA` and `DecoratorB` layers wrapped around it, for example `DecoratorB(DecoratorA(ConcreteComponent))`.

## Exercises
1. Write a `TimingDecorator` around a function-like component that reports how long `operation` took.
2. Compare this pattern with Python's `@functools.wraps` decorator syntax in a short paragraph: what do they share, and how do they differ?
3. Challenge: make decorators configurable at runtime from a list of decorator classes applied in a loop.

## Common Pitfalls
- Making decorators depend on the concrete component class instead of the component interface.
- Forgetting that wrapping order changes behavior; document the intended order.
- Creating too many small decorator classes where a single parameterized decorator would do.

## Deliverables
- Both stacking-order outputs with an explanation of the difference.
- Your `UpperDecorator` and the three-layer result.
