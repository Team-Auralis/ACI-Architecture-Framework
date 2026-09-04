# The Cyber Range

A sandbox for destruction.

## Red Teaming the Mesh
The Cyber Range is an air-gapped deployment of the ORION architecture. Security engineers are tasked with breaking it.

**Attack Scenarios:**
1.  **The Rogue Node:** We grant the Red Team full SSH access to a simulated Edge Node vehicle. They must attempt to extract the database keys from the TPM, forge a SPIFFE workload identity, and poison the global NATS mesh.
2.  **The Stingray:** Simulating a fake cellular tower to execute a Man-In-The-Middle (MITM) attack against civilian HAVEN users, verifying that the mTLS and payload encryption prevents data leakage.
3.  **The Broadcast Storm:** Injecting a routing loop into the BLE mesh to see if the TTL (Time-to-Live) counters correctly kill the infinite packet loop before it crashes the civilians' phones.
