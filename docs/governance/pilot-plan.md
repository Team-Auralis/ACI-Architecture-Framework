# ORION Closed Pilot Plan (P1.5-016)

**Status:** CONSTRAINTS FINALIZED // EXECUTION PENDING PARTNER AGENCY

This document defines the binding constraints for the first real-world ORION deployment: a controlled, authenticated pilot with a single partnered emergency response organization inside a geofenced area. These constraints are enforced in code, not by policy alone.

## 1. Scope

- Single partner agency; named operator accounts only.
- Civilian ingestion (HAVEN) limited to pre-agreed participant devices.
- Duration: fixed window agreed with the partner agency, during their normal operating hours.
- The pilot runs in **PILOT_MODE**, which restricts all SOS ingestion to a configured geofence.

## 2. Geofence Constraint

Ingestion outside the fence is rejected with `403` at the API edge (see `apps/api/pilot.py`).

| Setting | Value |
|---|---|
| Enable | `PILOT_MODE=1` |
| Fence | `PILOT_GEOFENCE="min_lat,min_lon,max_lat,max_lon"` |

- Format is an axis-aligned bounding box; final coordinates are locked with the partner agency before go-live. Candidate region: `17.60,83.10,17.85,83.35` (Visakhapatnam metro).
- **Fail-closed**: if `PILOT_GEOFENCE` is missing or malformed while `PILOT_MODE=1`, ingestion returns `503` rather than running unrestricted.
- Fence changes take effect on process restart (env-driven); coordinate changes require change control sign-off (`docs/governance/change-control.md`).

## 3. Kill Switch

Any authorized operator can halt the pilot instantly, without redeploying:

| Endpoint | Effect |
|---|---|
| `POST /v1/pilot/suspend` | Blocks **all** incident ingestion with `503`. Requires a detailed reason (>= 20 chars). |
| `POST /v1/pilot/resume` | Lifts suspension. |
| `GET /v1/pilot/status` | Reports mode, fence, and suspension state. |

- All three require the `operator` role via OPA actions `pilot:suspend` / `pilot:resume` / `pilot:status`.
- Suspension overrides everything — including valid geofenced traffic.
- Every suspend/resume/rejection is written to the CHRONOS audit trail (`logs/chronos_audit.jsonl`: `PILOT_SUSPENDED`, `PILOT_RESUMED`, `PILOT_GEOFENCE_REJECTED`).
- Known limitation: the kill switch is in-memory and resets on API restart. Restart during a suspended state must be treated as a resume event and re-approved explicitly.

## 4. Mandatory Abort Triggers

Operators MUST suspend the pilot if any of the following occur:

1. Any physical dispatch executed without explicit operator approval (HITL violation).
2. Asset state machine conflict that cannot be resolved (repeated `409 OCC` conflicts).
3. Duplicate/uncontrolled event replay observed in the mesh (Outbox/JetStream anomaly).
4. PII discovered unmasked in any stored message.
5. SLO breach sustained for > 15 minutes (SOS acceptance > 1s p95, availability < 99.9%).
6. Any suspected unauthorized access to operator accounts.

## 5. Operational Constraints (inherited from Phase 1.5)

- AI may classify → recommend → explain only. Physical dispatch requires human approval via `POST /v1/dispatch/recommendations/{id}/action` (P1.5-009), re-checked against OPA immediately before execution.
- Assets move through the deterministic state machine protected by optimistic concurrency (P1.5-010).
- SOS ingestion rate-limited at 5/minute per client (SlowAPI); abuse patterns reviewed daily.
- No event loss tolerance: DB commits + NATS publishes remain atomic via the Transactional Outbox (P1.5-007).

## 6. Data Handling

- PII (emails, phone numbers, SSNs) is regex-scrubbed from civilian messages before persistence (P1.5-013, `apps/api/security.py`).
- Pilot data is stored in the pilot Postgres instance only; export requires partner-agency approval.
- Retention: pilot incidents are purged or anonymized within 30 days of pilot exit unless legally required otherwise.
- Secrets come from environment injection only; no credentials in code (P1.5-013).

## 7. Entry Criteria (all must be green)

- [x] HITL dispatch queue enforced (P1.5-009)
- [x] Asset state machine + OCC (P1.5-010)
- [x] Transactional Outbox (P1.5-007) and persistent dedup (P1.5-008)
- [x] PII masking and secret stripping (P1.5-013)
- [x] Backup/restore procedure measured (P1.5-011)
- [ ] Chaos drills passed on NATS/Postgres partitions (P1.5-012) — *blocked on Docker*
- [x] AEGIS hardware gateway (P1.5-014)
- [x] SRE runbooks (P1.5-015)
- [ ] Partner agency sign-off on geofence coordinates and abort triggers
- [ ] Penetration test completed without critical findings

## 8. Exit Criteria

- >= 500 authenticated SOS events processed with zero lost messages.
- Zero autonomous dispatches; 100% of dispatches human-approved.
- SLOs met for the full pilot window.
- Post-pilot report filed under `docs/` and reviewed in governance.

## 9. Rollback

Suspension via kill switch is the primary rollback. If the API itself is compromised, revoke the pilot Keycloak realm clients and block ingress at the load balancer. Restore procedures per `scripts/dr_backup_restore.py` (P1.5-011).
