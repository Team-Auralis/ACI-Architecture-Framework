# ORION: Global Scaling & Satellite Connectivity Research

This report synthesizes the current state-of-the-art for global event streaming (NATS) and Non-Terrestrial Network (NTN) satellite links, mapped directly to ORION's requirements.

## 1. Global NATS Architecture for ORION

To scale ORION globally, we do not stretch a single NATS cluster over the ocean. Instead, we use two built-in NATS topologies: **Superclusters** and **Leaf Nodes**.

### Superclusters (Region-to-Region)
*   **What it is:** A mesh of regional clusters connected via NATS Gateways.
*   **Why ORION needs it:** If a regional ORION node goes offline, the Supercluster survives. Gateways are "smart"—they only route an `incident.created` event across the Atlantic if there is an active subscriber (like a global dashboard) on the other side. This prevents wasting expensive satellite bandwidth.
*   **Implementation:** Deploy one NATS cluster per geographic zone (e.g., US-East, EU-West). Connect them via Gateway ports.

### Leaf Nodes (Edge-to-Cloud)
*   **What it is:** A lightweight, autonomous NATS server running on edge devices (like a responder vehicle or remote hospital) that creates an *outbound-only* connection to the central Supercluster.
*   **Why ORION needs it:** 
    1. **Firewall friendly:** Outbound-only means the edge node doesn't need exposed ports.
    2. **Offline resilience:** If the satellite link drops, the Leaf Node keeps routing local messages (e.g., local responder chat). When the link returns, it reconnects and syncs.

## 2. State-of-the-Art in NTN (Non-Terrestrial Networks)

The satellite industry is moving away from proprietary "bolt-on" hacks and toward **3GPP Standards (Releases 17, 18, and 19)**. For ORION, this means satellite links will behave natively like 5G terrestrial links.

### Key Developments for ORION
*   **Regenerative Payloads (Rel 19):** Older satellites were "bent pipes" (they just bounced signals back to earth). State-of-the-art satellites now process the signal directly onboard (putting the 5G base station/gNB in space). This allows satellites to route traffic to *each other* before beaming down, bypassing dead ground stations.
*   **Store-and-Forward (Rel 19):** Satellites can now hold IoT/emergency telemetry if a ground link isn't immediately available and forward it later. This aligns perfectly with ORION's delay-tolerant architecture.
*   **Direct-to-Device (D2D):** Standard smartphones will soon connect directly to satellites (without specialized hardware) using standard 3GPP protocols. "ORION Citizen" won't need a clunky satellite phone.

## 3. The Lazy Dev Synthesis: What This Means for Code

1.  **Stop building custom sync logic.** NATS Leaf Nodes handle the edge-to-cloud offline sync natively.
2.  **Don't build custom satellite adapters.** With 3GPP NTN standardization, ORION can treat a satellite link as a standard, high-latency 5G connection. Let the modem handle the Doppler shift and latency; ORION just needs to set aggressive timeouts and idempotency keys (which we already built).
3.  **Architectural Rule:** Keep high-frequency telemetry on the local Leaf Node. Only push critical events (`incident.created`) over the Supercluster gateway to preserve NTN bandwidth.
