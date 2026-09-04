# 04 Satellite & Communication Layer (AEGIS)

## 1. Purpose
AEGIS defines the physical and logical transport layers of ORION. While NEXUS defines the software architecture, AEGIS defines how bits actually move across a broken planet.

## 2. Scope
Included: Satellite/NTN integration, fallback protocols, mesh networking theory, traffic prioritization, and Edge Node uplinks.
Excluded: Software application logic, database schemas.

## 3. Major Components
*   **Terrestrial Backhaul:** Fiber and 5G networks (Primary).
*   **Non-Terrestrial Networks (NTN):** LEO satellite constellations (Fallback).
*   **IoT & Mesh:** LoRaWAN and BLE store-and-carry (Deep Edge).
*   **Traffic Shaper:** The QoS engine prioritizing critical SOS packets over general telemetry.

## 4. Architecture
AEGIS uses a **Graceful Degradation Model**. The system always attempts the highest-bandwidth route first. As infrastructure fails, the routing layer automatically shifts to slower, higher-latency mediums, culminating in completely asynchronous offline mesh networking.

## 5. Responsibilities
Ensure that if a NATS event needs to reach the Supercluster, AEGIS finds a physical route, even if it takes hours.

## 6. Relationships with other ORION parts
AEGIS provides the physical transport for **NEXUS** (the event mesh). **HAVEN** (civilian app) relies entirely on AEGIS's mesh and fallback protocols to function.

## 7. Future Roadmap
Direct-to-Device (D2D) satellite messaging (e.g., Apple SOS, AST SpaceMobile), allowing standard civilian smartphones to bypass the BLE mesh and hit satellites directly.

## 8. Trade-offs
In degraded states, AEGIS trades bandwidth for reachability. Real-time video streams are aggressively killed in favor of kilobyte-sized JSON SOS payloads.

## 9. Risks
Weather (e.g., heavy rain) degrading Ku/Ka-band satellite uplinks precisely when emergency communications are needed most.

## 10. Research Questions
Can we use AI (SENTIENCE) to dynamically adjust traffic shaping based on real-time satellite constellation positioning and weather patterns?

## 11. Security Considerations
All communication mediums (especially public 5G and open BLE meshes) are considered hostile. AEGIS assumes the physical layer is compromised; therefore, all payloads are secured via **VEIL** (mTLS and payload encryption).

## 12. Current Status
**Phase 0:** Transport layers modeled and fallback sequences defined.
