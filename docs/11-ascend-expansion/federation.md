# Federation & Sovereign Clusters

How organizations collaborate without giving up control.

## The NATS Gateway Pattern
Assume the Red Cross and FEMA both run their own independent ORION deployments. They have their own Keycloak identity servers, their own Postgres databases, and their own NATS Superclusters.

During a massive hurricane, they need to share data.
*   They do not give each other API keys or database access.
*   Instead, they establish a **NATS Gateway** connection between their clusters.
*   They configure the Gateway to only pass specific event topics: e.g., `orion.incident.public.*`.
*   A Red Cross volunteer presses SOS. The event hits the Red Cross mesh, crosses the Federation Gateway, and instantly appears on the FEMA dashboard.

This guarantees data sovereignty. FEMA cannot see the Red Cross's private internal logistics topics (`orion.logistics.private.*`), but they can flawlessly coordinate on public emergencies.
