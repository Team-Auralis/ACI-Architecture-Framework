# Data Governance & Privacy

In emergency response, data privacy is a life-or-death responsibility.

## Cryptographic Shredding
When a civilian sends an SOS, it contains their exact GPS coordinates and medical status. 
ORION must retain the metadata (Time, Disaster Type, Response Latency) to train the **MIRROR** simulation and **SENTIENCE** AI, but keeping the PII (Personally Identifiable Information) forever is a massive security liability.

Instead of trying to "delete" rows across a distributed, append-only event mesh, ORION uses **Cryptographic Shredding**.
The PII payload is encrypted with a unique, one-time symmetric key. That key is stored in a secure Key Management System (KMS). When the incident is closed and the data retention period expires, the KMS permanently deletes the key. The encrypted PII scattered across the global database and event logs instantly becomes mathematical noise, impossible to decrypt.
