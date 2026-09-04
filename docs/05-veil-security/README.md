# 06 Security & Zero Trust (VEIL)

## 1. Purpose
VEIL is the security foundation of ORION. Because ORION operates over hostile, fractured, and public networks (cellular, mesh, satellite), traditional perimeter security (VPNs, firewalls) is useless. VEIL enforces absolute Zero Trust at every layer.

## 2. Scope
Included: Identity management (AuthN), policy enforcement (AuthZ), encryption, threat modeling, and edge workload identity.
Excluded: Physical security of command centers, personnel background checks.

## 3. Major Components
*   **Keycloak:** Central Identity Provider (IdP) for human operators.
*   **SPIFFE/SPIRE:** Workload Identity for machines, edge nodes, and AI agents.
*   **Open Policy Agent (OPA):** The deterministic authorization firewall.
*   **mTLS Fabric:** Mutual TLS for all machine-to-machine communication.

## 4. Architecture
VEIL decouples security from application logic. The FastAPI gateway does not decide if an action is safe; it delegates authentication to Keycloak/SPIRE and authorization to OPA.

## 5. Responsibilities
Ensure that a compromised edge node, a hallucinating AI, or a intercepted satellite transmission cannot breach the global state of the network.

## 6. Relationships with other ORION parts
VEIL governs everything. It dictates the Bounded Autonomy of **SENTIENCE** (AI) and secures the payloads traversing **AEGIS** (Comms).

## 7. Future Roadmap
Post-quantum cryptography for satellite uplinks to protect against "harvest now, decrypt later" attacks.

## 8. Trade-offs
Zero Trust adds latency. Evaluating an OPA policy and verifying a JWT signature takes milliseconds, which adds up in a deeply nested microservice chain. We trade this microsecond performance for absolute cryptographic certainty.

## 9. Risks
If the central SPIRE server is unreachable for an extended period, edge nodes may fail to rotate their short-lived certificates, causing the local mesh to lock itself out (the "offline credential rotation" problem).

## 10. Research Questions
How to maintain secure credential rotation on a completely disconnected edge node running on battery power for 3 weeks?

## 11. Security Considerations
Assume the network is already breached. Assume the physical edge node has been captured by a hostile actor.

## 12. Current Status
**Phase 1:** OPA sidecar integration and basic JWT validation are operational in the Phase 0/1 codebase.
