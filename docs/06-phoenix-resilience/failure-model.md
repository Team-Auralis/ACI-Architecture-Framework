# Failure Model

ORION anticipates and engineers against four primary failure domains:

1.  **Transport Failure (The Cut Fiber):** Terrestrial infrastructure is destroyed. The system must immediately failover to AEGIS satellite/NTN links.
2.  **Edge Isolation (The Blackout):** Heavy weather knocks out the satellite uplink. The Edge Node is now completely isolated. It must transition to Degraded Mode.
3.  **Hardware Death (The Flooded Server):** A responder vehicle's physical server is destroyed. The local mesh must immediately failover to another nearby responder vehicle's Edge Node via BLE/Wi-Fi Direct.
4.  **Cloud Region Loss (The Active-Active Failover):** A massive event takes down an entire AWS/GCP region. The CockroachDB and NATS Supercluster architecture must instantly route traffic to a surviving global region.
