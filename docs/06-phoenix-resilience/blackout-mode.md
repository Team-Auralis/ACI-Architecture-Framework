# Blackout Mode

When a device (e.g., a civilian smartphone running HAVEN) loses absolutely all connectivity to any ORION Edge Node.

## System Behavior
1.  **UI Shift:** The HAVEN app visually shifts to a red "Blackout Mode" theme so the user understands the severe latency constraint.
2.  **Store and Carry:** The phone activates BLE scanning. It acts purely as a delay-tolerant storage node.
3.  **Asynchronous Gossip:** When it detects another civilian phone, it mathematically merges their respective encrypted SOS databases. 
4.  **Zero-Knowledge Relay:** The civilian has no idea they are carrying other people's SOS signals, and they cannot read them. They are merely a physical transport layer walking toward an eventual Edge Node.
