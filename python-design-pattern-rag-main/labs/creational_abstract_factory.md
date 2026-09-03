# Lab 11: The Abstract Factory Pattern (Creational)

## Objectives
- Understand how a factory interface can produce whole families of related products.
- Keep client code independent of concrete product classes.
- Add a new product family (Linux) to the existing GUI example.

## Background
The Abstract Factory pattern provides an interface for creating families of related objects without specifying their concrete classes. Each concrete factory guarantees that its products are compatible.

## Materials
- Lesson: `docs/creational_abstract_factory.md`
- Reference implementation: `patterns/creational/abstract_factory.py`

## Task Overview
Run the demo for both existing families, then add a complete Linux family.

## Step-by-Step Instructions
1. Open `patterns/creational/abstract_factory.py` and identify: abstract products (`Button`, `Checkbox`), concrete products (Windows/Mac variants), the abstract factory `GUIFactory`, and the client `Application`.
2. Run the script as provided (`os_type = "mac"`):
   ```bash
   python patterns/creational/abstract_factory.py
   ```
3. Change `os_type` to `"windows"` and run again; note that `Application` needed no changes.
4. Add `LinuxButton`, `LinuxCheckbox`, and `LinuxFactory`; extend the selection logic with a third branch.
5. Run with `os_type = "linux"` and verify the Linux widgets render.

## Expected Output
For `"mac"`:
```text
Render a Mac-style button.
Render a Mac-style checkbox.
```
For `"windows"` the equivalent Windows messages.

## Exercises
1. Add a third product type (`Menu`) to every family; observe how the abstract factory interface forces every family to stay complete.
2. Refactor the factory selection into a dictionary mapping `os_type -> factory class`.
3. Challenge: read `os_type` from an environment variable or config value instead of hard-coding it.

## Common Pitfalls
- Mixing products from different families (for example a Windows button with a Mac checkbox); the pattern exists precisely to prevent this.
- Forgetting to update every concrete factory when the abstract factory gains a new product method.
- Using Abstract Factory for a single product type; a simple Factory Method is enough there.

## Deliverables
- The completed Linux family with verified output for all three platforms.
- A product-family table (rows: families, columns: product types).
