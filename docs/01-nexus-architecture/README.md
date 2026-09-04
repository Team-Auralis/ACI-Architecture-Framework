# 02 ORION Architecture (NEXUS)

## 1. Purpose
NEXUS defines the complete, high-level system architecture of ORION. It maps out how the 12 modules interact, the technology choices, and the structural boundaries that prevent the system from degrading into a monolithic failure point.

## 2. Scope
Included: Data flows, component boundaries, source-of-truth mapping, and the macro-level event-driven architecture.
Excluded: Specific UI designs, specific AI model architectures, and deep deployment manifests.

## 3. Major Components
*   **System Context:** External actors interacting with ORION.
*   **Component Model:** The internal tech stack (Keycloak, OPA, FastAPI, PostgreSQL, NATS).
*   **Data Flow:** The exact traversal path of an event through the mesh.
*   **Boundaries:** The strict rules governing what components are allowed to know about each other.

## 4. Architecture
ORION uses an **Event-Driven, Decentralized Mesh Architecture**. It relies heavily on asynchronous message passing (NATS) rather than synchronous REST calls to ensure offline survival and low latency across satellite links.

## 5. Responsibilities
Ensure that the architecture remains strictly decoupled. No single component should become a bottleneck or a centralized failure point.

## 6. Relationships with other ORION parts
NEXUS is the blueprint. HAVEN (Civilian), SENTIENCE (AI), and ATLAS (Infrastructure) all operate within the boundaries defined here.

## 7. Future Roadmap
Transitioning from a Modular Monolith (Phase 1) to a fully distributed Edge/Cloud hybrid where components run natively on disconnected responder vehicles.

## 8. Trade-offs
Event-driven systems are harder to debug and trace than standard REST APIs. We trade observability simplicity for extreme resilience and uptime.

## 9. Risks
Eventual consistency. Because components operate asynchronously, there is a risk of data lagging between the edge and the cloud during network partitions.

## 10. Research Questions
How do we maintain global consistency of critical emergency state across isolated NATS Superclusters without massive satellite bandwidth overhead?

## 11. Security Considerations
Enforced via strict component boundaries. A compromised component (e.g., an AI worker) cannot mutate state directly; it must publish an intent that is validated elsewhere.

## 12. Current Status
**Phase 0:** Architecture conceptually locked and documented.
