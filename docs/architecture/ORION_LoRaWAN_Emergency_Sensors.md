# ORION: Planetary Sensor Nervous System (IoT)

## The Problem
ORION cannot rely solely on humans with smartphones to report emergencies. We need a massive, deploy-and-forget network of environmental sensors (flood gauges, wildfire sniffers, structural integrity monitors) that can operate for a decade without a battery change, even when local cellular grids are destroyed.

## State-of-the-Art LPWAN (Low Power Wide Area Networks)

### 1. eMTC / LTE-M (The Cellular Approach)
*   **Pros:** Uses existing cell towers. High reliability, handles mobile assets (like tracking a moving ambulance) very well.
*   **Cons:** Consumes more power (5-10 year battery life). Requires paying monthly carrier fees per SIM card. Most importantly, **it relies on commercial cellular towers**, which are the first to fail during a hurricane or earthquake.

### 2. LoRaWAN (The Independent Approach)
*   **Pros:** Ultra-low power. Sensors spend 99% of their life asleep and wake asynchronously to transmit. Achieves 10-15+ year battery life on a coin cell. Operates on unlicensed spectrum, meaning **we can deploy our own private gateways**.
*   **Cons:** Extremely low bandwidth (bytes, not megabytes). Only suitable for "heartbeat" or "alarm" signals.

## ORION Architecture Recommendation
**LoRaWAN for fixed sensors, bridging to NATS via Edge Gateways.**

To build the ORION nervous system, we will use LoRaWAN for all deploy-and-forget environmental sensors. 
1.  **Private Infrastructure:** We deploy solar-powered LoRaWAN gateways on high ground, fire towers, and responder vehicles. 
2.  **No Cellular Dependency:** When the commercial grid dies, our LoRaWAN sensors still transmit to our private gateways.
3.  **The NATS Bridge:** The gateway runs a NATS Leaf Node. When it receives a LoRaWAN packet (e.g., "Water Level Critical"), the Leaf Node translates it into a JSON `incident.created` event and routes it to the Supercluster.
