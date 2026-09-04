# Disaster Recovery & Resynchronization

When a Degraded Edge Node finally regains its satellite uplink, the reconciliation process begins.

## The Resync Burst
1.  The NATS Leaf Node detects the uplink and immediately flushes its queued events to the global Supercluster.
2.  Simultaneously, it subscribes to the missed events from the global cluster.

## Conflict Resolution
Because the edge node was modifying state while offline, and the cloud was modifying state while online, merge conflicts will occur (e.g., both the cloud and the edge tried to assign a helicopter to the same incident).

ORION resolves this via **Idempotency** and **CRDTs (Conflict-Free Replicated Data Types)** where applicable, or via strict timestamp-based Last-Write-Wins rules for basic status updates. The reconciliation must happen automatically without human operator intervention.
