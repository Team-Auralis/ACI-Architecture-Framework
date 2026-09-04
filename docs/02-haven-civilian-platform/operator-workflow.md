# Operator Workflow

The triage process for dispatchers using the Next.js Dashboard.

## Ingestion & Clustering
When a disaster occurs, an operator may receive 10,000 SOS events in 5 minutes. The dashboard does not show a raw list.
*   **Spatial Clustering:** The UI relies on spatial logic (powered by Postgres/CockroachDB) to group overlapping coordinates into a single "Incident Zone".
*   **Priority Queue:** Medical emergencies override property damage.

## Action & Authorization
When an operator decides to dispatch a unit:
1.  Operator selects the Incident and clicks "Dispatch Medevac".
2.  The UI sends a `POST /v1/dispatch` request.
3.  **Crucial Security Check:** The backend OPA engine checks if this specific operator is authorized to dispatch air units in this specific geographic zone.
4.  If OPA returns `ALLOW`, the event is published to NATS, and the downstream system alerts the medevac unit.
