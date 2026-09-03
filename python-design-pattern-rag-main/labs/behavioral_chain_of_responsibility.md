# Lab 01: The Chain of Responsibility Pattern (Behavioral)

## Objectives
- Understand how a request is passed along a chain of handlers.
- Practice building and modifying a handler chain dynamically.
- Observe how the pattern decouples the sender of a request from its receivers.

## Background
In the Chain of Responsibility pattern, each handler decides either to process a request or to forward it to the next handler in the chain. The client only knows the first handler, which keeps senders and receivers loosely coupled.

## Materials
- Lesson: `docs/behavioral_chain_of_responsibility.md`
- Reference implementation: `patterns/behavioral/chain_of_responsibility.py`

## Task Overview
Run the reference implementation, trace how different requests travel through the chain, then extend the chain with a handler of your own.

## Step-by-Step Instructions
1. Open `patterns/behavioral/chain_of_responsibility.py` and review the `Handler` base class: `set_next`, `handle`, and `pass_to_next`.
2. Run the script:
   ```bash
   python patterns/behavioral/chain_of_responsibility.py
   ```
3. For every request in the demo, record which handler processed it and which handlers it passed through.
4. Run the bundled unit tests:
   ```bash
   python -m unittest discover -s patterns/behavioral -p "chain_of_responsibility.py" -v
   ```
5. Add a new `RabbitHandler` that handles the request `"Carrot"`, insert it into the chain, and verify that the request reaches it.

## Expected Output
The demo prints a handling message for each recognized request (for example `"Cat: I'll eat the Fish."`) and, for unrecognized requests, prints `"Can't handle ..., passing to next..."` traces until the end of the chain, where it reports that no handler remains.

## Exercises
1. Reorder the chain and predict how the traces change before running the script again.
2. Modify `pass_to_next` so an unhandled request returns `"Unhandled: <request>"` instead of `None`; update the unit tests accordingly.
3. Challenge: build the chain from a list of handlers using a loop instead of chained `set_next` calls.

## Common Pitfalls
- Forgetting that `set_next` returns the *next* handler, so `a.set_next(b).set_next(c)` links `b` to `c`, not `a` to `c`.
- Assuming some handler will always process the request; always handle the unhandled (`None`) case.
- Creating a circular chain, which causes infinite recursion.

## Deliverables
- A modified script containing your additional handler and passing unit tests.
- A trace table mapping each test request to the handlers it visited.
