# ORION: Zero Trust Identity at the Disconnected Edge

## The Problem: The Brittle Control Plane
ORION requires strict Zero Trust authentication for every action. Standard Zero Trust architectures rely on a centralized identity provider (like a global Keycloak or SPIRE server). 

However, ORION edge nodes (e.g., responder vehicles) are designed to operate during severe network outages. If a local node loses connection to the central server, it cannot validate new tokens or authenticate new operators, effectively paralyzing the local network.

## The State-of-the-Art Solution: Nested SPIRE

To maintain Zero Trust in a disconnected environment, ORION should implement a **Nested SPIRE Topology**.

### How it works:
1.  **Hierarchical Trust:** Instead of all edge devices talking to the cloud, we deploy a "downstream" SPIRE server directly on the local ORION edge node.
2.  **Chain of Issuance:** While online, the edge SPIRE server authenticates with the global server and receives the authority to issue local SVIDs (SPIFFE Verifiable Identity Documents) to local devices.
3.  **Offline Survival:** When the satellite/cellular link is severed, the edge SPIRE server continues to function autonomously. It can issue, rotate, and validate cryptographic identities for local responders, allowing them to communicate securely over local mesh networks.

### Hardware Roots of Trust
To prevent a compromised edge node from issuing fake credentials, edge servers should leverage hardware-backed security (TPM or HSM modules) for Node Attestation. This guarantees the physical integrity of the edge server before it is allowed to issue local credentials.

### The Trade-off: Extended TTLs vs Revocation
When offline, an edge node cannot receive Certificate Revocation Lists (CRLs). If an operator's access is revoked globally, the edge node won't know until it reconnects. Therefore, ORION must balance the Time-To-Live (TTL) of offline credentials: long enough to survive a storm, but short enough to mitigate the risk of stolen devices.
