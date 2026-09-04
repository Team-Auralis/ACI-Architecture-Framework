# 10 Data & Intelligence Fabric (OMNIS)

## 1. Purpose
OMNIS is the circulatory system of ORION. It governs how data is ingested, routed, stored, analyzed, and eventually destroyed. It ensures that the right intelligence reaches the right node at the exact right time, without flooding the network.

## 2. Scope
Included: Data architecture (CQRS/Event Sourcing), event fabric routing, telemetry standards, storage primitives, and data governance.
Excluded: The physical transport of the data (handled by AEGIS) and the cognitive reasoning applied to the data (handled by SENTIENCE).

## 3. Major Components
*   **The Event Fabric:** NATS JetStream.
*   **The State Store:** PostgreSQL / CockroachDB.
*   **The Telemetry Lake:** Time-series storage for sensor data.
*   **The Object Store:** MinIO (S3-compatible) for edge-distributed media.

## 4. Architecture
OMNIS strictly separates operational state from historical telemetry. We do not run analytical queries on the same database that handles life-or-death SOS ingest. It utilizes Command Query Responsibility Segregation (CQRS) and Event Sourcing patterns.

## 5. Responsibilities
Ensure zero data loss for critical events (SOS), while aggressively sampling and pruning non-critical telemetry to save bandwidth.

## 6. Relationships with other ORION parts
OMNIS relies on **NEXUS** (the event mesh), feeds massive data to **MIRROR** (Digital Twin), and provides the training material for **SENTIENCE** (AI).

## 7. Future Roadmap
Global Data Mesh. Moving away from a centralized data warehouse to a federated model where data remains at the edge and queries are distributed globally.

## 8. Trade-offs
To preserve satellite bandwidth, OMNIS aggressively downsamples telemetry at the edge. We trade high-fidelity historical data in the cloud for real-time operational survivability.

## 9. Risks
Data Gravity. If edge nodes collect terabytes of drone video, it becomes physically impossible to move that data to the cloud.

## 10. Research Questions
How do we efficiently synchronize distributed Vector Databases across a fragmented network to support RAG (Retrieval-Augmented Generation) for edge AI agents?

## 11. Security Considerations
Data Governance mandates strict PII scrubbing. An SOS signal contains highly sensitive medical data. OMNIS must mathematically guarantee that once an incident is closed, the PII is cryptographically shredded while preserving the metadata for AI training.

## 12. Current Status
**Phase 1:** Core PostgreSQL state and basic NATS event passing are implemented.
