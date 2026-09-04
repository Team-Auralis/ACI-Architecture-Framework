# Integration Model

How external and legacy systems connect to ORION.

## The Edge Leaf Node Pattern
External systems (like legacy emergency dispatch software or custom satellite modems) should not be hard-coded into the core API. 

Instead, integrations operate via **NATS Leaf Nodes**:
1. A small integration script runs locally next to the external system.
2. It translates the external system's proprietary format into an ORION JSON Event.
3. It publishes the event to a local NATS Leaf Node.
4. The Leaf Node securely bridges the event outbound to the ORION Supercluster.

This isolates ORION from the brittleness of external APIs and relies entirely on standard event schemas.
