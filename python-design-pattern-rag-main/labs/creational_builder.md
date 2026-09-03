# Lab 13: The Builder Pattern (Creational)

## Objectives
- Understand how construction of a complex product is separated from its representation.
- Use a Director to define reusable construction recipes.
- Add a new construction step and a new recipe.

## Background
The Builder pattern separates step-by-step construction from the final product. The same construction process (Director) can create different representations by using different builders.

## Materials
- Lesson: `docs/creational_builder.md`
- Reference implementation: `patterns/creational/builder.py`

## Task Overview
Run the minimal and full product recipes, then add `PartC` and a new recipe.

## Step-by-Step Instructions
1. Open `patterns/creational/builder.py` and identify the roles: `Product`, `Builder` (interface), `ConcreteBuilder`, and `Director`.
2. Run the script:
   ```bash
   python patterns/creational/builder.py
   ```
3. Note that `get_product` resets the builder - build twice and confirm no parts leak between products.
4. Add `build_part_c` to the `Builder` interface and `ConcreteBuilder`.
5. Add a `build_premium_product` recipe to the Director that includes all three parts, run it, and verify `PartA, PartB, PartC`.

## Expected Output
```text
Minimal product: PartA
Full product: PartA, PartB
```

## Exercises
1. Create a second `ConcreteBuilder` that produces parts with different names (for example `"WoodenPartA"`) and run the same Director recipes with it.
2. Remove the Director and drive the builder directly from client code; discuss when each style is preferable.
3. Challenge: make `Product.list_parts` render an ordered list showing the construction order.

## Common Pitfalls
- Forgetting `reset` in `get_product`, so the next product inherits leftover parts.
- Letting the Director know concrete builders; it should depend only on the `Builder` interface.
- Using Builder for simple objects with two or three fields; a plain constructor is clearer.

## Deliverables
- The extended builder with `PartC` and the premium recipe, with verified output.
- A short note on when to use a Director versus client-driven construction.
