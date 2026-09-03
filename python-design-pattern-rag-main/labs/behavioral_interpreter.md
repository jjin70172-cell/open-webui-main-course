# Lab 03: The Interpreter Pattern (Behavioral)

## Objectives
- Understand how a grammar can be represented as a tree of expression objects.
- Distinguish terminal expressions from non-terminal expressions.
- Extend a tiny arithmetic language with a new operator.

## Background
The Interpreter pattern defines a representation for a language's grammar and evaluates sentences of that language by traversing the expression tree. It suits small, well-defined grammars such as simple arithmetic.

## Materials
- Lesson: `docs/behavioral_interpreter.md`
- Reference implementation: `patterns/behavioral/interpreter.py`

## Task Overview
Predict and verify the result of the demo expression, then add multiplication to the language.

## Step-by-Step Instructions
1. Open `patterns/behavioral/interpreter.py` and identify:
   - the `Context` (holds variable values),
   - the terminal expression `Variable`,
   - the non-terminal expressions `Add` and `Subtract`.
2. Before running, compute the expected result of the demo expression `x + (y - z)` with `x = 10`, `y = 5` and `z` undefined. Note how `Variable.interpret` treats a missing variable.
3. Run the script and confirm your prediction:
   ```bash
   python patterns/behavioral/interpreter.py
   ```
4. Implement a `Multiply` non-terminal expression and build the expression `(x + y) * z` with `z = 3`.
5. Verify the new expression evaluates to `45`.

## Expected Output
```text
Result: 15
```
because `z` is missing from the context and defaults to `0`: `10 + (5 - 0) = 15`.

## Exercises
1. Add a `Constant` terminal expression so numbers can appear directly in expressions.
2. Change `Variable.interpret` to raise a `KeyError` for missing variables instead of defaulting to `0`; observe how the demo behaves.
3. Challenge: write a small parser that converts the string `"x + y * z"` into the corresponding expression tree.

## Common Pitfalls
- Forgetting that missing variables silently default to `0` in the reference implementation, which can hide typos.
- Building the expression tree with the wrong nesting order (tree shape determines evaluation order).
- Using Interpreter for large grammars; for complex languages a real parser is more maintainable.

## Deliverables
- Your prediction of the demo result with a one-line justification, confirmed by the actual run.
- The extended script containing the `Multiply` expression and its verified output.
