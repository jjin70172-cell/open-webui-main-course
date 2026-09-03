# Lab 27: The Proxy Pattern (Structural)

## Objectives
- Understand how a surrogate object controls access to a real subject.
- Add cross-cutting behavior (access checks, logging) without modifying the subject.
- Implement a new proxy variant of your own.

## Background
The Proxy pattern provides a placeholder for another object to control access, reduce cost, or add functionality. The proxy implements the same interface as the real subject, so clients use either transparently.

## Materials
- Lesson: `docs/structural_proxy.md`
- Reference implementation: `patterns/structural/proxy.py`

## Task Overview
Run the protection-proxy demo, then implement a caching proxy variant.

## Step-by-Step Instructions
1. Open `patterns/structural/proxy.py` and trace `Proxy.request`: access check, delegation to `RealSubject`, then logging.
2. Run the script:
   ```bash
   python patterns/structural/proxy.py
   ```
3. Modify `check_access` to deny access when a flag is `False`; verify the real subject is never called in that case.
4. Implement `CachingProxy` for a `DataService` subject with an expensive `fetch(key)` method (simulate cost with `time.sleep`): cache results per key and return cached values on repeat calls.
5. Call `fetch` twice with the same key and verify the second call is instant.

## Expected Output
```text
Client: Executing request through the proxy:
Proxy: Checking access before forwarding request...
RealSubject: Handling request.
Proxy: Logging the time of request.
```

## Exercises
1. Classify the demo proxy and your caching proxy using the standard names (protection proxy, cache proxy, virtual proxy, remote proxy).
2. Implement a virtual proxy that delays creating the real subject until the first request.
3. Challenge: add a hit/miss counter to the caching proxy and print the hit rate at the end.

## Common Pitfalls
- Letting the proxy change the subject's behavior beyond its stated concern (access, caching, logging).
- Forgetting that the proxy must implement the full subject interface or clients will break.
- Unbounded caches inside proxies; add eviction when the cache can grow.

## Deliverables
- The modified protection proxy with a denied-access run transcript.
- The `CachingProxy` with a before/after timing comparison.
