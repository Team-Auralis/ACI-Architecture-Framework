# Degraded Mode

When an Edge Node (Responder Vehicle) loses its satellite uplink but maintains its local Wi-Fi 6 / LoRaWAN mesh.

## System Behavior
1.  **State Freezing:** The local database marks itself as `disconnected`. It can no longer fetch global updates.
2.  **Local Serving:** Responders connected to the vehicle can still view the cached map, read cached dispatch orders, and communicate with each other over the local Wi-Fi.
3.  **Event Queuing:** If a responder updates an incident status, the FastAPI gateway processes it locally, saves it to the local DB, and publishes it to the local NATS Leaf Node. The Leaf Node **queues** the outbound event.
4.  **Local Auth:** The local SPIRE server handles short-lived credential rotation for local drones and laptops, bypassing the need for the central cloud Keycloak server.
