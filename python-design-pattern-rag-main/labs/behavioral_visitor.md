# Lab 10: The Visitor Pattern (Behavioral)

## Objectives
- Understand how new operations can be added over a set of element classes without modifying them.
- Implement the double-dispatch mechanism (`accept` + `visit_*`).
- Add a new visitor that performs a different operation over the same elements.

## Background
The Visitor pattern separates an operation from the object structure it works on. Each element provides `accept(visitor)`, which calls back the visitor's type-specific `visit_*` method - this is double dispatch.

## Materials
- Lesson: `docs/behavioral_visitor.md`
- Reference implementation: `patterns/behavioral/visitor.py`

## Task Overview
Run the demo, trace the double dispatch, then add an exporting visitor.

## Step-by-Step Instructions
1. Open `patterns/behavioral/visitor.py` and trace one full call: `element.accept(visitor)` -> `visitor.visit_element_a(element)`.
2. Run the script:
   ```bash
   python patterns/behavioral/visitor.py
   ```
3. Add `ElementC` with its own `operation_c` and extend the `Visitor` interface with `visit_element_c`.
4. Implement `ExportVisitor` that returns each element's data as a single CSV line instead of printing it.
5. Run both visitors over a list containing all three element types and verify the outputs.

## Expected Output
```text
Visitor: Processing ElementA logic
Visitor: Processing ElementB logic
```

## Exercises
1. Collect results in the visitor (for example a running total) instead of printing; discuss how visitor state accumulates across elements.
2. Discuss what must change when a new element type is added, and why this is the pattern's main cost.
3. Challenge: implement an `XMLExportVisitor` and compare its output with the CSV visitor.

## Common Pitfalls
- Forgetting to add a `visit_*` method for every element type in every visitor (Python won't check this for you; abstract methods help).
- Breaking encapsulation by exposing element internals just to please a visitor.
- Choosing Visitor when element types change often; the pattern is best when elements are stable and operations grow.

## Deliverables
- The extended element set and your `ExportVisitor` with sample output.
- A short note on when Visitor is and is not appropriate.
