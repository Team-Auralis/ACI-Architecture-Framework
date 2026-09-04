# Physical Pilot Scenario Matrix — ORION Phase 1.5

**STATUS: DEFINED / NOT EXECUTED.** Every scenario below must be executed against the live pilot deployment with a signed witness record (timestamped log export + operator sign-off). Software-test green does NOT satisfy evidence requirements.

Legend — Safety boundary: the invariant that must hold if the scenario fails.

| # | Scenario | Expected result | Safety boundary | Evidence required | Pass/Fail |
|---|---|---|---|---|---|
| 1 | Normal SOS (in-fence, authenticated) | `200`, incident persisted, outbox event published, AI triage < 10s | No event loss; HITL unchanged | API log line, DB row, NATS message dump | ☐ |
| 2 | Duplicate SOS (same Idempotency-Key) | Second request returns cached response, single incident created | No duplicate dispatch recommendations | Both responses + single DB row | ☐ |
| 3 | Unauthorized SOS (no token / citizen on admin path) | `403`; nothing persisted | Zero state mutation | API log, empty DB query | ☐ |
| 4 | AI unavailable (Ollama stopped) | Deterministic keyword fallback triages; incident still processed | Ingestion unaffected; no auto-dispatch | Sentinel logs showing fallback | ☐ |
| 5 | AI timeout (>2s) | Same as #4 within bounded latency | Event-loop not blocked > 2s | Latency metric | ☐ |
| 6 | NATS interruption mid-SOS | Incident committed; outbox replays after reconnect; zero loss | DB commit is source of truth | Outbox row before/after + replay log | ☐ |
| 7 | PostgreSQL interruption mid-SOS | `503` to client (fail-closed) or degraded-mode via NATS only if bus healthy; NO silent drop | Client always gets explicit outcome | Response capture + server logs | ☐ |
| 8 | Operator REJECTS recommendation | Rec → `REJECTED`; asset stays `IDLE` | No physical movement | DB rows + audit entry | ☐ |
| 9 | Operator APPROVES recommendation | Asset IDLE→DISPATCHED with OCC; event emitted; rec immutable thereafter | Single-actor transition; expiry >10min blocked | DB version bump, audit, asset telemetry | ☐ |
| 10 | Kill switch activated | All ingestion `503`; **dispatch approval also blocked**; status endpoint reports suspended | No new physical-action authorizations post-switch | Probe during suspension | ☐ |
| 11 | Geofence violation | `403` + audit `PILOT_GEOFENCE_REJECTED`; corners inclusive per bbox test | Fence deterministic at ±GPS-accuracy margin | Rejected payload + audit line | ☐ |
| 12 | Device disconnect mid-session | No orphaned partial incidents; retry safe via idempotency | At-most-once incident creation | Client + server correlation IDs | ☐ |
| 13 | Hardware packet corruption (AEGIS) | HMAC validation rejects; packet dropped + counted | Corrupt data never reaches triage | AEGIS reject counter | ☐ |
| 14 | Hardware link loss (LoRa/radio) | Buffer-and-forward on reconnect; duplicates suppressed by dedup | No silent loss, no double-count | Link metrics + dedup counter | ☐ |
| 15 | Recovery after full outage | Services restart in order; **asset table NOT wiped/reseeded over live state**; outbox drains; pilot remains SUSPENDED until explicit resume | Restart cannot silently re-enable ingestion or destroy state | Startup logs, asset row continuity, pilot status | ☐ |

## Blocking notes (as of red-team review @ HEAD `3b1570c`)

- Scenarios 13–14 are **NOT EXECUTABLE**: no AEGIS hardware gateway exists (`services/aegis/` is empty).
- Scenario 15 was MITIGATED at HEAD: `seed_assets.seed()` now skips unless `SEED_DB=1` AND skips when assets already exist. Live restart evidence still required.
- Scenario 10 was fixed and unit-tested at HEAD (kill switch gates dispatch approval via `enforce_pilot_active()`). Live evidence still required.
- NEW blocker found by red team: `/v1/assets` now requires OPA action `dashboard:view` on resource `assets`, but `policy/opa/policy.rego` only permits that action for resource `admin` — default-deny makes the endpoint 403 for everyone, including operators. Add the missing rule.

