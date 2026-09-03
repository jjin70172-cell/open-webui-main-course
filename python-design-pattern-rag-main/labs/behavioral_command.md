# Lab 02: The Command Pattern (Behavioral)

## Objectives
- Understand how encapsulating a request as an object decouples the invoker from the receiver.
- Identify the four roles of the pattern: Command, ConcreteCommand, Invoker, and Receiver.
- Extend the example with a new receiver and command.

## Background
The Command pattern turns a request into a standalone object that carries all the information needed to perform an action. This enables parameterization of clients, queuing of requests, and undo support.

## Materials
- Lesson: `docs/behavioral_command.md`
- Reference implementation: `patterns/behavioral/command.py`

## Task Overview
Run the remote-control demo, map each class to its pattern role, then add a new device and commands for it.

## Step-by-Step Instructions
1. Open `patterns/behavioral/command.py` and label each class with its role: `Command` (abstract command), `TurnOnCommand`/`TurnOffCommand` (concrete commands), `RemoteControl` (invoker), `Light` (receiver).
2. Run the script:
   ```bash
   python patterns/behavioral/command.py
   ```
3. Add a `Stereo` receiver with `turn_on`, `turn_off`, and `set_volume(level)` methods.
4. Create `StereoOnCommand` and `StereoVolumeCommand` concrete commands and submit them through the same `RemoteControl`.
5. Verify the output shows the stereo operations in submission order.

## Expected Output
```text
Light is ON
Light is OFF
```
After your extension, the stereo messages should also appear in the order they were submitted.

## Exercises
1. Add an `undo` method to the `Command` interface and implement it for the light commands (store the previous state in the command).
2. Modify `RemoteControl` so it executes commands only when a `run_all` method is called (queue semantics).
3. Challenge: add a `MacroCommand` that holds several commands and executes them as one.

## Common Pitfalls
- Letting the invoker call receiver methods directly; the invoker should only know `execute`.
- Forgetting to pass the receiver into the concrete command's constructor.
- Storing mutable state in a command object that is shared between invocations.

## Deliverables
- The extended script with the `Stereo` receiver and at least two new commands.
- A short paragraph explaining how the invoker stays decoupled from receivers.
