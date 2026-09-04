# 03 Civilian Platform (HAVEN)

## 1. Purpose
HAVEN is the first real-world civilian interface built on top of the ORION mesh. It is a mobile application and operator dashboard designed to function during complete infrastructure blackouts.

## 2. Scope
Included: Smartphone mesh networking (BLE/Wi-Fi Direct), delay-tolerant SOS routing, civilian identity management, and the operator triage dashboard.
Excluded: Hardware manufacturing, specialized military interfaces.

## 3. Major Components
*   **HAVEN Mobile App:** The civilian-facing smartphone application (React Native/Flutter).
*   **HAVEN Operator Dashboard:** The Next.js web application for emergency dispatchers.
*   **Mesh Engine:** The background service managing device-to-device Bluetooth gossip.

## 4. Architecture
HAVEN operates as a client to the NEXUS architecture. It interacts with the FastAPI Gateway when online, and defaults to a local delay-tolerant mesh network when offline.

## 5. Responsibilities
Ensure that a civilian can trigger an SOS even with zero bars of cellular service, trusting that the message will eventually route through the mesh.

## 6. Relationships with other ORION parts
HAVEN relies on **AEGIS** (Communications) for the physical routing of offline mesh packets, and is governed entirely by **VEIL** (Security) for civilian identity.

## 7. Future Roadmap
Integration with native OS emergency features (e.g., Apple satellite SOS API) and autonomous drone deployment for localized network bridging.

## 8. Trade-offs
To achieve extreme battery life during disasters, HAVEN's offline mesh operates with very high latency (store-and-carry). It trades real-time chat for guaranteed, eventual delivery.

## 9. Risks
Malicious actors flooding the mesh with fake SOS signals to execute a Denial of Service attack on responders.

## 10. Research Questions
How do we cryptographically verify civilian identity offline without connecting to the central Keycloak server?

## 11. Security Considerations
All SOS packets must be signed by the civilian's private key. Relay phones in the mesh cannot read the contents of the SOS; they only route the encrypted payload.

## 12. Current Status
**Phase 1:** Concept defined, initial operator dashboard scaffolded in Next.js.
