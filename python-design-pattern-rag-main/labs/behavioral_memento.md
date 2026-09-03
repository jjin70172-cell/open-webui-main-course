# Lab 04: The Memento Pattern (Behavioral)

## Objectives
- Understand how an object's state can be captured and restored without breaking encapsulation.
- Identify the three roles: Originator, Memento, and Caretaker.
- Build a multi-step undo mechanism on top of the reference implementation.

## Background
The Memento pattern captures an object's internal state into a memento object so it can be restored later. The caretaker keeps the history but never inspects or modifies the stored state.

## Materials
- Lesson: `docs/behavioral_memento.md`
- Reference implementation: `patterns/behavioral/memento.py`

## Task Overview
Run the text-editor demo, explain each role, then extend the history to support several undo steps.

## Step-by-Step Instructions
1. Open `patterns/behavioral/memento.py` and label the roles: `TextEditor` (originator), `Memento` (state snapshot), `History` (caretaker).
2. Run the script:
   ```bash
   python patterns/behavioral/memento.py
   ```
3. Trace the demo by hand: what is stored in the memento, and what does `undo` restore?
4. Extend the demo code: write three separate sentences, backing up before each write, then call `undo` twice and print the content after each undo.
5. Verify the content walks back through the history in reverse order.

## Expected Output
```text
Current content: Hello, world!
After undo: Hello,
```

## Exercises
1. Add a `redo` capability to the `History` caretaker (hint: keep a second stack for undone mementos).
2. Make `TextEditor.save` defensive by returning a copy of the state so the memento cannot be tampered with.
3. Challenge: limit the history to the last `N` snapshots and drop the oldest ones.

## Common Pitfalls
- Backing up *after* the change instead of before it, which makes undo restore the wrong state.
- Letting the caretaker read or edit memento contents; only the originator should interpret them.
- Storing mementos by reference to mutable state instead of capturing an immutable snapshot.

## Deliverables
- The extended script demonstrating multi-step undo with its observed output.
- A role diagram mapping each class in the file to Originator / Memento / Caretaker.
