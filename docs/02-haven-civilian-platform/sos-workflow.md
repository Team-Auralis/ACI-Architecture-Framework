# SOS Workflow

How a civilian SOS propagates through HAVEN.

## The Online Path (Optimal)
1.  Civilian opens app and presses "Medical SOS".
2.  App sends a signed `POST /v1/incidents` to the ORION FastAPI gateway.
3.  OPA validates the civilian's token.
4.  State is saved, event published to NATS.
5.  Operator Dashboard updates in <100ms.

## The Offline Path (Degraded / Disaster)
1.  Civilian opens app and presses "Medical SOS". App detects no cellular connection.
2.  App encrypts the SOS payload, signs it, and attaches an `Idempotency-Key` and `TTL` (Time To Live).
3.  **Mesh Broadcast:** App broadcasts the payload via Bluetooth Low Energy (BLE).
4.  **Store and Carry:** A passing volunteer's phone (also running HAVEN) receives the BLE packet. The volunteer's phone has no internet either. It stores the packet.
5.  **Relay:** The volunteer walks 2 miles to an evacuation center.
6.  **Uplink:** The evacuation center has a Responder Vehicle with a satellite uplink running an ORION Leaf Node.
7.  The volunteer's phone connects to the Leaf Node and dumps the cached SOS payload.
8.  The Leaf Node bridges the packet to the global Supercluster.
9.  Operator Dashboard updates. The latency was 45 minutes, but the message survived.
