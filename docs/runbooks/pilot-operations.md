# Closed Pilot Operations Runbook

## Purpose

Run the geofenced closed pilot safely with a partnered emergency response organization.

## Pre-Flight

- Partner agency has signed off on geofence, operating window, abort triggers, and escalation contacts.
- `PILOT_MODE=1`.
- `PILOT_GEOFENCE` is set to the approved `min_lat,min_lon,max_lat,max_lon`.
- OPA actions `pilot:status`, `pilot:suspend`, and `pilot:resume` are enforced.
- SRE runbooks are available to operators.
- Backup/restore has been measured.
- AEGIS hardware devices are inventoried if enabled.
- Pilot kill switch has been tested in a non-production rehearsal.

## Start of Pilot Window

1. Confirm `/v1/pilot/status` shows correct geofence and `suspended = false`.
2. Confirm API, dashboard, OPA, Keycloak, Postgres, Redis, NATS, worker, and observability are healthy.
3. Send one synthetic in-geofence SOS and confirm it flows end to end.
4. Confirm one synthetic out-of-geofence SOS is rejected with `403`.
5. Record start time and operator roster.

## Suspend Pilot

Call `POST /v1/pilot/suspend` with a detailed reason when any mandatory abort trigger occurs.

Abort triggers include:

- Physical dispatch without explicit operator approval.
- Repeated asset OCC conflicts.
- Uncontrolled event replay.
- PII found unmasked.
- SOS acceptance p95 above 1 second for more than 15 minutes.
- Availability below 99.9% during the pilot window.
- Suspected unauthorized operator access.

Suspension returns all ingestion attempts as `503` and writes `PILOT_SUSPENDED` to CHRONOS.

## Resume Pilot

Only resume after:

- Root cause is understood.
- Mitigation is deployed.
- Partner-agency contact approves.
- Incident commander approves.
- `/v1/pilot/status` is checked immediately after resume.

Known limitation: pilot suspension is in-memory and resets on API restart. If the API restarts during a suspended incident, treat that as unsafe until an operator explicitly confirms whether to re-suspend or resume.

## Exit

At the end of the pilot:

1. Stop new pilot ingestion.
2. Export only approved operational metrics.
3. Review CHRONOS for dispatch, break-glass, pilot, and mutation events.
4. File a post-pilot report.
5. Purge or anonymize pilot data within the approved retention window unless legally required otherwise.

