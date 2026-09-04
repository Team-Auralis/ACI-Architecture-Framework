# Traffic Prioritization (QoS)

During a disaster, bandwidth over a Tier 3 (Satellite) or Tier 4 (LoRaWAN) link is precious. AEGIS ruthlessly enforces Quality of Service (QoS) rules at the NATS Leaf Node level before pushing data over the uplink.

## Priority Queue
1.  **P0 (Critical Life Safety):** Civilian SOS signals, Responder distress calls, Authorization Tokens. **Always routed.**
2.  **P1 (Operational Coordination):** Dispatch orders, text-based chat between responder units, critical infrastructure alarms. **Routed if P0 queue is empty.**
3.  **P2 (Telemetry):** Non-critical sensor data, GPS tracking updates. **Aggressively throttled/sampled.** (e.g., sending GPS every 5 minutes instead of every 5 seconds).
4.  **P3 (High Bandwidth Data):** Video streaming, high-res photos, software updates. **Blocked entirely** on degraded links unless manually overridden by a Command Center operator with high-level OPA clearance.
