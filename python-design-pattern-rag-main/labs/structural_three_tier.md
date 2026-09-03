# Lab 28: The Three-Tier Architecture Pattern (Structural)

## Objectives
- Separate an application into presentation, logic, and data tiers.
- Enforce the rule that each tier talks only to its neighbor.
- Add a feature end-to-end across all three tiers.

## Background
Three-tier architecture splits an application into a presentation layer (user interaction), a logic layer (validation and business rules), and a data layer (storage). Each tier depends only on the tier directly below it.

## Materials
- Lesson: `docs/structural_three_tier.md`
- Reference implementation: `patterns/structural/three_tier.py`

## Task Overview
Run the interactive task manager, identify the tier boundaries in the single file, then add a "remove task" feature through all three tiers.

## Step-by-Step Instructions
1. Open `patterns/structural/three_tier.py` and mark the three sections: data layer (`_tasks_db`, `save_task`, `fetch_all_tasks`), logic layer (`add_task`, `get_all_tasks`), presentation layer (`show_menu`, `run_cli`).
2. Run the interactive CLI (use a real terminal, since it reads keyboard input):
   ```bash
   python patterns/structural/three_tier.py
   ```
3. Add a task, view tasks, try adding an empty task to trigger the validation error, then exit.
4. Implement "remove task" end-to-end:
   - data layer: `delete_task(index)`
   - logic layer: `remove_task(index)` with bounds validation
   - presentation layer: menu option 3 that reads an index and reports success or error
5. Test the new option, including an out-of-range index.

## Expected Output
An interactive session such as:
```text
=== Task Manager ===
1. Add Task
2. View Tasks
3. Exit
Choose an option: 1
Enter the task: Study design patterns
Task added.
```

## Exercises
1. Split the file into `data.py`, `logic.py`, and `presentation.py` modules with one-directional imports; verify the import graph has no cycles.
2. Replace the in-memory list with a JSON file in the data layer without changing the other tiers.
3. Challenge: add unit tests for the logic layer that never touch the presentation layer.

## Common Pitfalls
- Letting the presentation layer call the data layer directly, which bypasses validation.
- Putting business rules in the data layer or UI formatting in the logic layer.
- Sharing mutable data structures across tiers instead of passing copies.

## Deliverables
- A session transcript showing add, view, validation error, and your new remove feature.
- The three-tier feature implementation with tier boundaries clearly marked.
