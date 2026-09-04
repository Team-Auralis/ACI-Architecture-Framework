# Core Engineering Principles

Every line of code and architectural decision in ORION must adhere to these absolute principles.

## 1. The Prime Directive
> **Do not build the ecosystem first. Build one complete ORION nervous-system reflex first.**

Before expanding, we must prove the core loop works perfectly:
**Input → Identity → Policy → State → Event → Response → Audit**

## 2. Bounded Autonomy
AI and automated systems are powerful but fundamentally untrustworthy. They must never possess direct credentials to mutate system state. They propose actions; an independent, deterministic policy engine (OPA) authorizes them.

## 3. Idempotency by Default
We assume network failure is a constant, not an anomaly. Every action must be safely retriable without causing duplicate state mutations or duplicate physical responses.

## 4. Zero Trust at the Edge
Trust nothing. Not the network, not the device, not the user. Identity must be cryptographically proven and authorization continuously verified, even when an edge node is severed from the central cloud.

## 5. Offline Survival (Graceful Degradation)
When connectivity drops, local nodes must not crash. They must switch to a degraded mode, queuing events locally and serving local meshes, resynchronizing only when the connection is restored.
