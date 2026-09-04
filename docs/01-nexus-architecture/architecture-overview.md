# Architecture Overview

ORION rejects the traditional microservice-heavy REST architecture for Phase 1. Complex microservices require high-bandwidth, stable networks—the exact opposite of a disaster zone.

## The Modular Monolith & Event Mesh
Instead, ORION utilizes a **Modular Monolith backed by a Global Event Mesh**.

1.  **The API Gateway (FastAPI):** Acts purely as an ingest and egress layer. It performs no business logic. It handles HTTP idempotency and delegates authorization.
2.  **The Policy Engine (OPA):** Operates as a sidecar. It contains the hardcoded logical rules for the system.
3.  **The State Store (PostgreSQL):** The immutable ledger of what has happened.
4.  **The Event Mesh (NATS):** The actual nervous system. Once an action is approved and saved, it is broadcast to the mesh. All other modules (Workers, AI agents, Dashboards) subscribe to this mesh asynchronously.

This design ensures that if the downstream workers or AI systems crash, the core ability to ingest and broadcast an SOS remains untouched.
