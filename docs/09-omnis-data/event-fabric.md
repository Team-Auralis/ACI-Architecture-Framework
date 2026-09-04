# The Event Fabric (NATS JetStream)

The backbone of OMNIS.

## Topics and Wildcards
Data is routed using hierarchical subject namespaces.
*   `orion.incident.created.medical`
*   `orion.telemetry.sensor.waterlevel`

This allows massive flexibility. An AI agent might subscribe to `orion.incident.*` to analyze all emergencies, while a specific regional dashboard might subscribe to `orion.incident.*.florida`.

## Delivery Guarantees
*   **At-Most-Once:** Used for telemetry (`waterlevel`). If a packet drops, we don't care; another one is coming in 60 seconds.
*   **Exactly-Once (Idempotent At-Least-Once):** Used for critical events (`incident.created`). NATS JetStream ensures the message is persisted to disk and delivered. The consumer worker utilizes Idempotency Keys to ensure it doesn't process the rescue order twice if NATS accidentally delivers it twice.
