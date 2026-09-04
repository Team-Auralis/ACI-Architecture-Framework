# Threat Model

ORION assumes the following threats are active and capable:

1.  **Network Spoofing/MITM:** Attackers setting up fake cell towers (Stingrays) or fake BLE nodes to intercept mesh traffic. *Mitigated by End-to-End encryption and mTLS.*
2.  **Physical Edge Capture:** Hostile actors capturing an offline responder vehicle to extract database intelligence. *Mitigated by TPM-backed disk encryption and ephemeral keys.*
3.  **DDoS & Noise Flooding:** Adversaries flooding the NATS satellite uplink with garbage data to drown out real SOS signals. *Mitigated by strict QoS Traffic Prioritization (AEGIS) dropping unauthenticated packets at the extreme edge.*
4.  **Rogue AI (Hallucination/Poisoning):** An AI agent acting maliciously due to prompt injection. *Mitigated by Bounded Autonomy and the OPA firewall preventing state mutation.*
