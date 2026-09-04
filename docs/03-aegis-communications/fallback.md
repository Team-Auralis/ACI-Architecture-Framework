# Fallback Protocol

The absolute sequence of degradation. This sequence is hard-coded into the networking logic of every ORION gateway.

1.  **Tier 1 (Gigabit / Real-Time):** Fiber Optic or Hardline Ethernet.
2.  **Tier 2 (Broadband / Real-Time):** Public 5G/LTE or Dedicated FirstNet Cellular.
3.  **Tier 3 (High Latency / Weather Dependent):** LEO Satellite Uplink (Starlink, etc.).
4.  **Tier 4 (Low Bandwidth / Asynchronous):** Direct-to-Device Satellite (Apple SOS) or LoRaWAN.
5.  **Tier 5 (Zero Connectivity / Store-and-Carry):** BLE/Wi-Fi Direct Civilian Mesh (waiting for physical transport).

The transition down the tiers is automatic. The transition back up the tiers occurs via aggressive polling to restore maximum bandwidth as quickly as possible.
