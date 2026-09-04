# Identity Management

Identity is the foundation of Zero Trust. You cannot authorize an action if you do not know mathematically who is requesting it.

## Human Identity (Keycloak)
*   Used for Dispatch Operators, Admins, and eventually Civilians.
*   Issues standard JSON Web Tokens (JWTs) via OIDC.
*   Supports federated logins (e.g., integrating with a local police department's existing Active Directory).

## Machine & Workload Identity (SPIFFE/SPIRE)
*   Used for API Gateways, NATS Workers, AI Agents, and Edge Nodes.
*   API keys and passwords are banned in ORION. They leak.
*   Instead, SPIRE issues highly ephemeral, short-lived X.509 certificates (SVIDs) to workloads based on cryptographic attestation (e.g., verifying the binary hash of the NATS worker before handing it a certificate).
*   **Nested Edge:** A responder vehicle runs a local SPIRE agent. Even if the satellite link drops, the local agent can issue short-lived certs to the laptops and drones connected to that specific vehicle.
