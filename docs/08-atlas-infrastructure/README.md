# 09 Cloud, Edge & Infrastructure (ATLAS)

## 1. Purpose
ATLAS is the compute substrate of ORION. It defines exactly where and how code executes, ranging from massive multi-region cloud clusters down to ruggedized battery-powered servers bolted into the trunks of responder vehicles.

## 2. Scope
Included: Cloud environments, edge hardware specs, containerization strategies, distributed compute topologies, and deployment models.
Excluded: Software logic, database schemas, and NATS topic routing (defined in NEXUS and OMNIS).

## 3. Major Components
*   **The Global Core (Cloud):** The central aggregated state (AWS/GCP/Azure).
*   **The Tactical Edge (Vehicles/Camps):** High-compute physical nodes deployed in the field.
*   **The Deep Edge (Sensors/Drones):** Low-compute, low-power end devices.
*   **Container Orchestrator:** The runtime managing workloads across the spectrum.

## 4. Architecture
ATLAS employs a **Heavy Edge / Decentralized** architecture. Unlike traditional IoT where edge devices are "dumb" sensors reporting to a "smart" cloud, ORION edge nodes are fully autonomous micro-clouds capable of sustaining local operations indefinitely.

## 5. Responsibilities
Ensure that the ORION software stack (FastAPI, OPA, NATS, Postgres) has a deterministic, immutable execution environment regardless of whether it's running in Virginia or the middle of the Pacific Ocean.

## 6. Relationships with other ORION parts
ATLAS provides the physical and virtual compute for **NEXUS** (Architecture). It is physically transported by **AEGIS** (Comms).

## 7. Future Roadmap
Full Kubernetes (KubeEdge/K3s) orchestration stretching from the cloud down to the tactical edge nodes, allowing seamless live-migration of AI workloads to moving vehicles.

## 8. Trade-offs
A "Heavy Edge" requires buying expensive, ruggedized servers for every responder vehicle. We trade capital expenditure (CapEx) for absolute operational survivability.

## 9. Risks
Configuration Drift. If an edge node is offline for 3 months, its container images and security patches will be severely out of date when it reconnects.

## 10. Research Questions
How to automatically and securely pull 20GB of container image updates to a fleet of 500 edge nodes over a highly constrained satellite connection without suffocating SOS traffic?

## 11. Security Considerations
Edge nodes are physically exposed. ATLAS mandates TPM-backed full disk encryption and secure boot to ensure that a stolen edge node cannot be reverse-engineered or used as a trojan horse to breach the Supercluster.

## 12. Current Status
**Phase 0/1:** Docker Compose is standard for local and edge deployments. Kubernetes is explicitly deferred.
