# Chaos & Physical Experiments

We do not trust vendor specs. We test physics.

## E-001: The Concrete Penetration Test
*   **Hypothesis:** A LoRaWAN environmental sensor can successfully transmit a 12-byte telemetry packet to an Edge Gateway through 3 stories of collapsed, reinforced concrete.
*   **Methodology:** Physical deployment of sensors in a controlled demolition site.
*   **Metrics:** Packet Delivery Ratio (PDR), Signal-to-Noise Ratio (SNR), and battery drain rate during re-transmission attempts.

## E-002: The Satellite Reconvergence Test
*   **Hypothesis:** A NATS Leaf Node can buffer 10,000 JSON events during a 45-minute satellite blackout and resynchronize with the global Supercluster in under 3 seconds upon reconnection without dropping a packet.
*   **Methodology:** Cloud-based simulation dropping the simulated uplink interface.
*   **Metrics:** Eventual Consistency Latency, CPU spike on the Leaf Node, and Duplicate Event Count (Idempotency verification).
