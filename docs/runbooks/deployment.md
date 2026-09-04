# Deployment Runbook

## Purpose

Deploy ORION API, worker, dashboard, observability, and supporting services without weakening the Phase 1.5 safety boundary.

## Pre-Deployment Checklist

- Confirm change approval under `docs/governance/change-control.md`.
- Confirm secrets come from environment injection or the approved secret manager path; do not add credentials to code or docs.
- Confirm required environment variables are present:
  - `DATABASE_URL`
  - `NATS_URL`
  - `REDIS_URL`
  - `KEYCLOAK_JWKS_URL`
  - `JWT_AUDIENCE`
  - `JWT_ISSUER`
  - `OPA_URL`
  - `OTEL_EXPORTER_OTLP_ENDPOINT`
  - `AEGIS_DEVICE_SECRETS_JSON` when direct radio ingress is enabled
  - `PILOT_MODE` and `PILOT_GEOFENCE` when running the closed pilot
- Confirm SLO dashboards and alerting are reachable before traffic is shifted.
- Confirm rollback owner and incident commander for the release window.

## Local Validation

Docker is currently a known blocker on the host. Until Docker is restored, validate with local tests and builds only:

```powershell
pytest -q tests
npm run lint --prefix apps/dashboard
npm run build --prefix apps/dashboard
```

Do not run `docker-compose`, container kill drills, or live chaos scripts until the user confirms Docker has been restarted.

## Deployment Steps

1. Build and test the exact revision to be deployed.
2. Apply database migrations before starting new API workers.
3. Start dependencies in this order: PostgreSQL, Redis, NATS/JetStream, OPA, Keycloak, observability collectors.
4. Start API instances and confirm `/metrics` is exposed.
5. Start the CRDT worker and confirm it exposes worker metrics on port `8002`.
6. Start AEGIS gateway only after NATS connectivity and device-secret configuration are confirmed.
7. Start the dashboard after API and Keycloak are reachable.
8. Send a synthetic authenticated SOS inside the pilot geofence if pilot mode is enabled.
9. Confirm the synthetic event appears in Postgres, the outbox is published, the worker processes the event, and the dashboard renders it.
10. Remove the synthetic incident or mark it clearly as test data per the partner-agency procedure.

## Post-Deployment Checks

- API p95 SOS acceptance latency is below 1 second.
- `outbox_events` has no growing backlog of `published = false`.
- Worker `worker_events_processed_total` increases for synthetic events.
- Worker `worker_duplicates_dropped_total` does not climb unexpectedly.
- OPA and Keycloak circuit breakers are closed.
- No Next.js error overlay or dashboard console errors are present.
- CHRONOS receives mutation log entries for the deployment validation actions.

## Rollback

1. Stop traffic to the new API/dashboard version.
2. Keep PostgreSQL and NATS running unless they are the faulty component.
3. Revert to the previous known-good build.
4. If pilot traffic is active and safety is uncertain, call `POST /v1/pilot/suspend` with a detailed reason.
5. If schema changes are involved, follow the database rollback plan or restore procedure in [Disaster Recovery](disaster-recovery.md).

