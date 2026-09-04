# Edge Connectivity

How the extreme edge of the network connects back to the core.

## The Edge Nodes
An ORION Edge Node is typically a ruggedized server sitting in a responder vehicle, a fire watchtower, or a temporary evacuation camp.

## Local Meshes
These Edge Nodes project local connectivity bubbles:
*   **Wi-Fi 6 / 5G Private Networks (CBRS):** Providing high-bandwidth local connectivity for responders within 1 mile.
*   **LoRaWAN Gateways:** Listening for miles around for tiny, low-power telemetry pings from environmental sensors.

When the Edge Node's satellite uplink goes down, the local mesh **does not die**. Responders connected to the same vehicle can still chat, update local maps, and coordinate. The NATS Leaf Node simply queues the "global" events until the satellite link returns.
