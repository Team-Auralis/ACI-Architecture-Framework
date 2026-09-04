# Component Model

The internal technology stack of the ORION Reflex Loop.

## 1. Identity Provider (Keycloak)
*   **Role:** Authentication. Answers "Who are you?"
*   **Tech:** Standard OIDC/SAML provider. At the edge, this will interface with SPIFFE/SPIRE for local workload identity.

## 2. Policy Firewall (Open Policy Agent - OPA)
*   **Role:** Authorization. Answers "Are you allowed to do this?"
*   **Tech:** Evaluates Rego policies deterministically. It runs decoupled from the application logic.

## 3. Gateway (FastAPI)
*   **Role:** Ingest, Orchestration, and Idempotency.
*   **Tech:** Python asynchronous framework. It validates the payload, queries OPA, writes to Postgres, and publishes to NATS.

## 4. State Authority (PostgreSQL)
*   **Role:** Relational truth and Idempotency cache.
*   **Tech:** Standard relational database. Will eventually be migrated to CockroachDB for global, active-active spatial distribution.

## 5. Event Fabric (NATS)
*   **Role:** Asynchronous messaging and global routing.
*   **Tech:** NATS Server. Supports Superclusters for regional bridging and Leaf Nodes for edge offline-survival.

## 6. Worker Pool (Python/Go)
*   **Role:** Business logic execution.
*   **Tech:** Subscribes to NATS subjects (e.g., `incident.created`), performs deduplication, executes logic (AI routing, notifications), and optionally publishes a new event.
