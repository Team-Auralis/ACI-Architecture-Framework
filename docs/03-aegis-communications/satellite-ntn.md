# Satellite & Non-Terrestrial Networks (NTN)

When the terrestrial grid collapses, AEGIS relies on Non-Terrestrial Networks (NTN).

## Low Earth Orbit (LEO) vs Geosynchronous (GEO)
*   **GEO (Traditional):** High latency (500ms+), massive bandwidth, but requires large, stationary dishes. Not suitable for moving responder vehicles or real-time event meshes.
*   **LEO (e.g., Starlink, OneWeb):** Low latency (30-50ms). This is the primary fallback for ORION Responder Vehicles. 

## Integration with ORION
Responder vehicles equipped with LEO flat-panel antennas act as **Mobile NATS Leaf Nodes**. 
1.  The vehicle drives into a blackout zone.
2.  The vehicle establishes a LEO uplink to the global internet.
3.  The local NATS Leaf Node establishes a secure TLS tunnel over the satellite link to the ORION Supercluster.
4.  Local civilians and responders connect to the vehicle via local Wi-Fi or LoRaWAN. Their packets are bridged over the satellite link.

## High Packet Loss Assumption
Even with LEO, satellite links drop due to weather, obstructions, or constellation handoffs. The system handles this via strict **Idempotency Keys** on the application layer, ensuring that a dropped satellite connection during a transmission does not duplicate a rescue order when retried.
