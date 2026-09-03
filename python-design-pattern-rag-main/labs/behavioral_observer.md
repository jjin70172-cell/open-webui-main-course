# Lab 05: The Observer Pattern (Behavioral)

## Objectives
- Understand one-to-many dependency and automatic notification.
- Practice attaching and detaching observers at runtime.
- Add a new observer type without modifying the subject.

## Background
The Observer pattern defines a subject that keeps a list of observers and notifies them whenever its state changes. It is the backbone of event-driven systems.

## Materials
- Lesson: `docs/behavioral_observer.md`
- Reference implementation: `patterns/behavioral/observer.py`

## Task Overview
Run the demo, observe how attach/detach changes who receives notifications, then add observers of your own.

## Step-by-Step Instructions
1. Open `patterns/behavioral/observer.py` and review `Subject.attach`, `Subject.detach`, and `Subject.notify`.
2. Run the script:
   ```bash
   python patterns/behavioral/observer.py
   ```
3. Record which observers receive each of the two notifications and explain why.
4. Add a third `ConcreteObserver` named `"Observer3"` and attach it before the first notification.
5. Implement a `LoggingObserver` that stores every message in a list instead of printing; after the demo, print the collected log.

## Expected Output
```text
Subject: Attached an observer.
Subject: Attached an observer.
Subject: Notifying observers...
Observer1 received update: State has changed!
Observer2 received update: State has changed!
Subject: Detached an observer.
Subject: Notifying observers...
Observer2 received update: Another change occurred.
```

## Exercises
1. Add a guard so attaching the same observer twice is rejected.
2. Give the subject its own state (for example a counter) and have observers read it from the notification instead of receiving a message string (pull vs push models).
3. Challenge: make `notify` robust so that one observer raising an exception does not stop the others from being notified.

## Common Pitfalls
- Forgetting to detach observers, which can keep unused objects alive (memory leaks in long-running apps).
- Modifying the observer list while iterating over it in `notify`.
- Assuming notification order is meaningful; treat observers as an unordered set unless the design says otherwise.

## Deliverables
- The extended script with the additional observers and their observed output.
- A short comparison of the push model used here versus a pull model.
