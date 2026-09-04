# Mesh Networking (Civilian Device-to-Device)

## The Problem
During a severe disaster (e.g., a massive earthquake), commercial cellular infrastructure (eNodeBs, cell towers) will fail. Civilians cannot rely on standard LTE/5G to communicate with the ORION network. While emergency responders will carry dedicated satellite hardware or LoRaWAN transmitters, civilians will only have their standard smartphones.

## State-of-the-Art: Delay-Tolerant Smartphone Mesh
To solve this, the **HAVEN Civilian Platform** must utilize decentralized mesh networking directly between smartphones, bypassing cellular towers.

### Core Technologies
1.  **Transport Layer (Wi-Fi Direct & Bluetooth Low Energy):**
    *   **BLE:** Used for constant, low-power peer discovery.
    *   **Wi-Fi Direct:** Automatically negotiated once a peer is found to transfer high-bandwidth data (e.g., a photo of a collapsed bridge).
2.  **Protocol (Delay-Tolerant / Store-and-Carry):**
    *   Unlike traditional routing which requires an end-to-end path, ORION will utilize protocols similar to the **Bramble Protocol** (used by Briar).
    *   **How it works:** A civilian sends an SOS. The app uses BLE to pass the encrypted SOS to five nearby phones. Those users physically walk to other areas. Their phones automatically "gossip" the encrypted SOS to *more* phones. 
    *   Eventually, one of those phones walks into range of an **ORION Edge Gateway** (e.g., a responder vehicle with a NATS Leaf Node and satellite link). The gateway receives the gossiped SOS and publishes it to the global Supercluster.

## Architectural Trade-offs
*   **Battery Drain:** Constant BLE/Wi-Fi scanning drains smartphone batteries quickly. The ORION app must aggressively duty-cycle its radios.
*   **Latency:** This is a "store-and-carry" network. Latency is measured in minutes or hours, not milliseconds. Therefore, all civilian mesh payloads must be treated as asynchronous events with strict **Idempotency Keys** to prevent the global NATS cluster from processing the same SOS 500 times when 500 phones eventually reach a gateway.