# Lab 20: The Bridge Pattern (Structural)

## Objectives
- Understand how separating abstraction from implementation lets both vary independently.
- Avoid the class explosion of an inheritance grid.
- Add a new shape and a new renderer without touching existing classes.

## Background
The Bridge pattern decouples an abstraction from its implementation by holding the implementation as a reference instead of inheriting it. Without the bridge, M shapes times N renderers means M x N classes.

## Materials
- Lesson: `docs/structural_bridge.md`
- Reference implementation: `patterns/structural/bridge.py`

## Task Overview
Run the circle demo with two renderers, then add a square and a third renderer.

## Step-by-Step Instructions
1. Open `patterns/structural/bridge.py` and identify the implementation hierarchy (`Renderer`, `VectorRenderer`, `RasterRenderer`) and the abstraction hierarchy (`Shape`, `Circle`).
2. Run the script:
   ```bash
   python patterns/structural/bridge.py
   ```
3. Count the classes needed here versus an inheritance approach for 2 shapes x 2 renderers.
4. Add `Square(Shape)` and a `SvgRenderer` implementation.
5. Combine every shape with every renderer and print all results; verify you added only 2 classes to support 4 combinations.

## Expected Output
```text
Drawing Circle as lines.
Drawing Circle as pixels.
```

## Exercises
1. Add a `resize(factor)` method to the abstraction and show how renderers stay unaffected.
2. Discuss: what happens at runtime if a shape is constructed without a renderer? Add a guard or a default.
3. Challenge: add a `Triangle` and a `AsciiRenderer`; list the final class count versus the inheritance-grid count.

## Common Pitfalls
- Coupling the abstraction to a concrete renderer (for example instantiating `VectorRenderer` inside `Shape`), which destroys the bridge.
- Creating the bridge for a single dimension of variation; it pays off only with two or more orthogonal dimensions.
- Forgetting that the implementation interface must be designed around what abstractions need, not around existing classes.

## Deliverables
- The extended shape/renderer matrix output.
- A short calculation comparing class counts: bridge vs inheritance grid.
