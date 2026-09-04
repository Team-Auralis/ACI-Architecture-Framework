# Terminology

## The 12 Parts of ORION
*   **AURA:** 01 Core Vision
*   **NEXUS:** 02 Architecture
*   **HAVEN:** 03 Civilian Platform
*   **AEGIS:** 04 Satellite & Communication Layer
*   **SENTIENCE:** 05 AI Orchestration Layer
*   **VEIL:** 06 Security & Zero Trust
*   **PHOENIX:** 07 Resilience & Emergency Systems
*   **MIRROR:** 08 Digital Twin & Simulation
*   **ATLAS:** 09 Cloud, Edge & Infrastructure
*   **OMNIS:** 10 Data & Intelligence Fabric
*   **FORGE:** 11 Research, Testing & Cyber Range
*   **ASCEND:** 12 National/Planetary Expansion

## Technical Terms
*   **Supercluster:** A mesh of regional NATS clusters connected via Gateways for global routing.
*   **Leaf Node:** A lightweight NATS server deployed at the edge that syncs outbound to the Supercluster.
*   **OPA:** Open Policy Agent. The deterministic firewall that evaluates all authorization requests.
*   **Idempotency Key:** A unique hash attached to a request ensuring that repeated transmissions resulting from network drops do not duplicate operations.
*   **SPIFFE/SPIRE:** The framework used for Zero Trust workload identity issuance, especially crucial in nested edge environments.
