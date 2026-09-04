# Immutable Benchmarks

Code that does not pass these benchmarks is rejected.

## 1. Latency Budgets (Online)
*   **API Gateway Ingest:** < 50ms (from POST to returning 200 OK).
*   **OPA Policy Evaluation:** < 10ms.
*   **NATS Global Propagation:** < 200ms (to hit every regional Supercluster).

## 2. Survivability Budgets (Degraded)
*   **Offline Transition:** The Edge Node must recognize a satellite drop and switch to Degraded Mode in < 2 seconds.
*   **Consumer Idempotency:** A Worker must reject a duplicate event payload in < 5ms (cache hit).

## 3. Scale Budgets
*   **Mesh Density:** The HAVEN app must successfully route a packet through a 10-hop BLE civilian mesh without timing out.
