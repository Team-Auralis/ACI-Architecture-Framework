# National-Scale Operations

Coordinating an entire continent.

## Decentralized Governance
At a national scale, a single cloud region (e.g., `us-east-1`) cannot be the sole brain.
*   The United States deployment of ORION would consist of multiple regional Superclusters (East, West, Central).
*   Identity (Keycloak) and Policy (OPA) are globally replicated but evaluated locally.
*   If the East Coast loses all internet connectivity to the West Coast, the East Coast Supercluster continues to operate autonomously, handling East Coast incidents without relying on a central Washington D.C. server.
