# System Context

How ORION fits into the external world.

## External Actors
1.  **Civilian Devices (HAVEN):** Smartphones connecting via Wi-Fi Direct/BLE mesh or cellular to reach the ORION gateway.
2.  **Responder Edge Nodes:** Vehicles equipped with satellite modems running local ORION instances (NATS Leaf Nodes) that act as regional hubs.
3.  **IoT Sensor Grid:** Deploy-and-forget LoRaWAN sensors (flood, fire) transmitting telemetry to ORION edge gateways.
4.  **Satellite Infrastructure (AEGIS):** 3GPP Non-Terrestrial Networks providing the ultimate backhaul when terrestrial fiber is severed.
5.  **Command Center Dashboards:** High-level operators viewing real-time aggregated intelligence.

ORION acts as the translation and routing layer between these highly fragmented, untrusted, and unreliable external actors.
