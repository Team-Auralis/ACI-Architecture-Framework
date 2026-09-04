# Incident Response Runbook

## Purpose

Provide a fast, repeatable response path for ORION production incidents while preserving human authorization and auditability.

## First Five Minutes

1. Assign an incident commander and scribe.
2. Declare severity using [README.md](README.md).
3. Check whether the closed pilot is active via `GET /v1/pilot/status`.
4. If there is possible public-safety harm, unauthorized dispatch, PII leakage, or uncontrolled replay, suspend the pilot immediately.
5. Capture evidence before restarting services: API logs, worker logs, NATS status, Redis status, Postgres status, dashboard screenshot, and CHRONOS tail.

## Common Symptoms

| Symptom | Likely area | Immediate checks |
|---|---|---|
| SOS create fails with `503` | Postgres and/or NATS unavailable; pilot suspended; OPA unavailable | API logs, `/v1/pilot/status`, OPA circuit keys in Redis, NATS connection. |
| SOS create returns `202 ACCEPTED_DEGRADED_MODE` | Postgres failed but NATS accepted fallback | Confirm NATS persisted event; open SEV-1 to restore DB. |
| Dashboard stuck on connection failed | API, Keycloak, OPA, or dashboard env mismatch | Browser console, API `/v1/incidents`, Keycloak token endpoint, OPA logs. |
| Incidents accepted but not triaged | AI worker or NATS subscription issue | Worker logs, JetStream consumers, `worker_events_processed_total`. |
| Recommendations appear but assets do not move | Human approval or OPA action blocked | Recommendation status, OPA decision, asset state. |
| Duplicate incidents or repeated processing | Outbox/JetStream retry or Redis dedupe issue | `processed:{event_id}` Redis keys, worker duplicate counter, outbox rows. |

## SOS Ingestion Triage

1. Confirm the request reached the API.
2. Confirm auth and OPA returned allow.
3. Confirm pilot geofence did not reject the request.
4. Confirm PII masking occurred before persistence.
5. Confirm an `Incident` row exists.
6. Confirm a matching `OutboxEvent` row exists.
7. Confirm the outbox publisher marked the row `published = true`.
8. Confirm NATS/JetStream delivered `incident.created`.
9. Confirm worker processed the event and acknowledged it.

If both Postgres and NATS are unavailable, ORION must fail closed with `503`.

## Dispatch Safety Triage

1. Inspect `dispatch_recommendations`.
2. Confirm AI wrote only a `PENDING` recommendation.
3. Confirm any `APPROVED` status corresponds to an explicit operator request.
4. Confirm OPA allowed `dispatch:action` at approval time.
5. Confirm asset was `IDLE` before transition to `DISPATCHED`.
6. If any dispatch occurred without approval, classify as SEV-0 and suspend pilot.

## Event Mesh Triage

1. Check NATS connectivity from API and worker.
2. Check JetStream stream `incidents` for subjects `incident.*` and `network.*`.
3. Check durable consumers `crdt_sync_engine`, `pathfinder_engine`, and `sentience_ai`.
4. Check Redis for dedupe key writes.
5. Check outbox backlog. A growing backlog means API DB commits are not reaching NATS.

## Closure Criteria

- Root cause is identified.
- Mitigation is deployed or rollback completed.
- SLOs are back within target.
- Pilot suspension is either still active with an owner or explicitly resumed.
- CHRONOS and the incident report include timeline, decisions, affected IDs, and follow-up actions.

