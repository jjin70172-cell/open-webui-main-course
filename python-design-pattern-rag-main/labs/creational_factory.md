# Lab 15: The Factory Method Pattern (Creational)

## Objectives
- Understand how delegating instantiation to subclasses keeps the creator decoupled from concrete products.
- Distinguish the roles: Product, ConcreteProduct, Creator, ConcreteCreator.
- Add a new product and creator pair.

## Background
The Factory Method pattern defines an interface for creating objects but lets subclasses decide which class to instantiate. The creator's business logic works against the abstract product only.

## Materials
- Lesson: `docs/creational_factory.md`
- Reference implementation: `patterns/creational/factory.py`

## Task Overview
Run both creators, then extend the family with a third product.

## Step-by-Step Instructions
1. Open `patterns/creational/factory.py` and identify the four roles listed above.
2. Run the script:
   ```bash
   python patterns/creational/factory.py
   ```
3. Explain why `Creator.some_operation` works without knowing which concrete product exists.
4. Add `ConcreteProductC` returning `"Result from ConcreteProductC"` and `ConcreteCreatorC` that produces it.
5. Extend the loop at the bottom to include `ConcreteCreatorC` and verify the third line of output.

## Expected Output
```text
Creator: Working with Result from ConcreteProductA
Creator: Working with Result from ConcreteProductB
```

## Exercises
1. Make `Creator` a concrete class with a default `factory_method` returning `ConcreteProductA`, so subclasses can override optionally.
2. Move the creator selection behind a function `get_creator(kind: str) -> Creator` and call it with `"A"`, `"B"`, and `"C"`.
3. Challenge: add a unit test asserting every concrete creator returns a product that satisfies the `Product` interface.

## Common Pitfalls
- Putting product-specific logic inside the creator; the creator must depend only on the abstract `Product`.
- Confusing Factory Method with Abstract Factory: Factory Method creates one product via inheritance; Abstract Factory creates families via composition.
- Overusing the pattern: if there is only one product type, call its constructor directly.

## Deliverables
- The extended script with `ConcreteProductC` / `ConcreteCreatorC` and verified output.
- A two-line comparison of Factory Method versus Abstract Factory.
