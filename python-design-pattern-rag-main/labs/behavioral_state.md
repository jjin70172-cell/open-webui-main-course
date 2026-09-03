# Lab 07: The State Pattern (Behavioral)

## Objectives
- Understand how delegating behavior to state objects makes an object appear to change its class.
- Implement state transitions driven by the states themselves.
- Compare the State pattern with the Strategy pattern.

## Background
The State pattern lets an object alter its behavior when its internal state changes by delegating work to a current state object. Transitions can be triggered by the context or by the states themselves.

## Materials
- Lesson: `docs/behavioral_state.md`
- Reference implementation: `patterns/behavioral/state.py`

## Task Overview
Run the toggling context demo, trace the transitions, then add a third state with a different transition rule.

## Step-by-Step Instructions
1. Open `patterns/behavioral/state.py` and review `Context.transition_to`, `Context.request`, and the two concrete states.
2. Before running, predict the output of three consecutive `request` calls starting from `ConcreteStateA`.
3. Run the script and verify:
   ```bash
   python patterns/behavioral/state.py
   ```
4. Add `ConcreteStateC` with the rule: A -> B -> C -> A. Update the transitions and run again with three `request` calls.
5. Draw the state transition diagram for your three-state machine.

## Expected Output
```text
Context: Transitioning to ConcreteStateB
State A: Handling and switching to B.
Context: Transitioning to ConcreteStateA
State B: Handling and switching to A.
Context: Transitioning to ConcreteStateB
State A: Handling and switching to B.
```

## Exercises
1. Move the transition logic out of the states and into the context; discuss which design is easier to extend.
2. Add a `LockedState` that refuses to transition until an `unlock` method is called on the context.
3. Challenge: log the full sequence of visited states and assert it matches your diagram in a unit test.

## Common Pitfalls
- Forgetting to call `set_context` on the new state during a transition, so the state cannot trigger further transitions.
- Scattering transition rules across many classes so the state machine becomes impossible to follow; keep a diagram.
- Confusing State with Strategy: states transition automatically as part of the workflow, strategies are usually chosen by the client.

## Deliverables
- The extended three-state implementation with its observed output.
- A state transition diagram (text-based is fine).
