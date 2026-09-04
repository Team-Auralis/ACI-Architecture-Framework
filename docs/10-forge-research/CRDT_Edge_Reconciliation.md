# Deep Research: Database CRDTs & Edge State Reconciliation

## The Problem
ORION Edge Nodes (Responder Vehicles) carry a local PostgreSQL database and a local NATS Leaf Node. When a satellite link drops, they enter "Degraded Mode" and continue operating autonomously. 

If Responder A (offline) updates the status of Incident 123 to `triaged`, and Command Center (online) simultaneously updates Incident 123 to `evacuating`, a severe database merge conflict occurs when the Edge Node regains connectivity. 

Traditional relational databases (PostgreSQL) use strict ACID transactions. They are not designed to merge conflicting offline writes automatically. If we rely on standard database replication, the node will either overwrite the cloud data (destroying Command's updates) or the cloud will overwrite the edge (destroying the Responder's updates).

## State of the Art Solutions

### 1. The Legacy ElectricSQL Model (Bidirectional CRDTs)
Early "local-first" solutions attempted to bake Conflict-Free Replicated Data Types (CRDTs) directly into the relational database. 
*   **How it worked:** Every row and column in Postgres was wrapped in a mathematical CRDT wrapper. If two disconnected users edited the same row, the math guaranteed that once they reconnected, both databases would mathematically converge to the exact same state without needing human intervention.
*   **The Flaw:** CRDTs on relational data are incredibly heavy. It balloons the database size (storing tombstones and vector clocks for every single cell) and makes standard SQL queries extremely complex.

### 2. The PowerSync Model (Last-Write-Wins & Sync Engines)
Modern solutions (like PowerSync and the newer Electric "Shapes" architecture) abandoned strict full-database CRDTs.
*   **How it works:** The edge runs a local SQLite (or PGlite) database. When it reconnects, it streams its queued writes back to the central Postgres database.
*   **Conflict Resolution:** It relies on simple **Last-Write-Wins (LWW)** based on timestamps, or pushes the conflict to the application layer to resolve.

## The ORION Architectural Decision

Because ORION is an emergency system, "Last-Write-Wins" is dangerous. If Command updates an incident to `evacuating` at 12:00, and a responder offline updates it to `triaged` at 12:01, the responder's write will "win" when they reconnect at 14:00, incorrectly reverting the global state back to `triaged`.

Therefore, ORION adopts a **Hybrid Event-Sourced CRDT Approach**:

### 1. Banning Mutability (Event Sourcing)
We do not use `UPDATE` statements for critical data.
We use **Append-Only Event Sourcing** over NATS. 
*   Instead of updating the incident row, the edge node publishes an event: `{"type": "incident.status_changed", "new_status": "triaged", "timestamp": "12:01"}`.
*   The cloud publishes: `{"type": "incident.status_changed", "new_status": "evacuating", "timestamp": "12:00"}`.
*   Because these are discrete events, **there is no database conflict**. The events are simply interleaved in the NATS log.

### 2. Semantic CRDTs for Projections
The `UPDATE` conflict is avoided, but the Next.js Dashboard still needs to know the *current* state.
The NATS Workers that read the event log and build the Postgres "Read View" utilize **Semantic CRDTs**.

We define an absolute state-machine hierarchy:
`reported` -> `triaged` -> `dispatching` -> `evacuating` -> `resolved`

When the NATS Worker processes the backlog after a reconnection, it uses a **Max-State CRDT**. It doesn't matter what order the timestamps arrived in. The math dictates that `evacuating` is a mathematically "higher" state than `triaged`. 

If the worker sees the `triaged` event arrive *after* the `evacuating` event, it mathematically ignores it. The global state remains `evacuating`.

## Conclusion
ORION explicitly rejects bidirectional database-level sync (like symmetric Postgres logical replication) for edge nodes. It relies entirely on NATS JetStream queuing to append offline events, and deterministic state-machine CRDTs in the worker layer to rebuild the localized relational view without conflict.
