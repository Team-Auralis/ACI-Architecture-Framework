# FORGE CYBER — Defensive Architecture

Status: KERNEL IMPLEMENTED AND TESTED (66 passed / 2 skipped, `tests/test_cyber_kernel.py`). Live-stack integration NOT TESTED (Docker unavailable during build).

FORGE CYBER is PROJECT ORION's defensive cybersecurity program: an observability-driven
detection and response layer that treats every security-relevant action in the platform as
an auditable event stream, applies deterministic detections, and executes response actions
under strict human authority. It is defensive-only by construction.

## Design Principles

1. **Defense only.** Every component detects, records, correlates, or responds defensively.
   There are no offensive modules in this program.
2. **AI advises, humans authorize.** Detection confidence scoring may be assisted by
   automation; no automated actor can approve a high-impact response. Approver identity is
   checked against a denylist of non-human prefixes (`ai-`, `sentience-`, `svc-`, `system`).
3. **Default-deny authorizer.** A SOAR action executes only if an injected authorization
   callable explicitly returns True for that action/scope pair. Unknown scope ⇒ deny.
4. **Every attempt is audited.** Both granted and denied executions append a structured
   record to an append-only JSONL audit sink, including policy decision reason.
5. **Fail-safe, not fail-open.** Missing approval, expired TTL, unknown scope, or missing
   authorizer all resolve to "not executed", never to "execute".

## Components

| Component | File | Responsibility |
|---|---|---|
| Event schema | `services/cyber/oses.py` | Normalized `SecurityEvent` (source, category, actor identity, timestamp UTC, attributes) + geo distance helper |
| Detection engine | `services/cyber/detections.py` | Thread-safe sliding-window rules over the normalized stream; emits `Finding`s separating OBSERVED evidence from INFERRED interpretation |
| Response engine (SOAR) | `services/cyber/soar.py` | Policy-gated playbook execution with impact tiers, distinct-human approval, TTL, rollback, full audit trail |

## Data Flow

```
[ORION services]                    [FORGE CYBER kernel]
 auth failures        ─┐
 break-glass mint/use ─┤             ┌─> DetectionEngine ─> Finding ─┐
 kill-switch changes  ─┼── SecurityEvent ─>            │              ├─> SOAR execute()
 OPA denials          ─┤             └─> window state     │              │      │ allow? approve?
 NATS publishers      ─┤                                              └──────┴──> SoarRecord ─> JSONL audit sink
 payload anomalies    ─┘                                                            │
 geo/velocity checks  ─┘                                                       rollback() if needed
```

Events enter through `SecurityEvent.create()` which stamps UTC time and normalizes
identity fields; nothing in the kernel trusts caller-supplied timestamps for windowing.

## Detection Catalog (implemented, unit-tested)

| Rule ID | Signal | Window / Threshold | Severity |
|---|---|---|---|
| AUTH-BRUTEFORCE | repeated auth failures per identity | >5 in 300s | medium→high |
| IMPOSSIBLE-TRAVEL | successive geolocations | >1200 km/h implied and >500 km apart | high |
| BG-SPIKE | break-glass mints | >2 in 3600s | critical |
| BG-OFFHOURS | break-glass use | 20:00–06:00 local | medium |
| BG-TOKEN-ABUSE | expired/replayed token attempts | any | high |
| KS-TAMPER | non-operator resume, outcome mismatch, resume without active suspension | any | high |
| POLICY-DENY-BURST | OPA denials per subject | >10 in 600s | medium |
| NATS-UNKNOWN-SUBJECT | publish to unregistered subject | any | low |
| NATS-UNAUTHORIZED-PUBLISHER | publisher not on subject allowlist | any | critical |
| PAYLOAD-OVERSIZE | payload above cap (256 KiB default) | any | low |
| ASSET-TELEPORT | asset position delta | >160 km/h | high |

## SOAR Safety Contract

Every `ActionSpec` carries: name, scope, impact tier (`low|medium|high`),
expected_effect, rollback spec, and reason string. Execution requires ALL of:

1. Authorizer callable returns True for (action, scope) — default deny otherwise;
2. Impact tier `high`: an approval from a *distinct human* principal (requester ≠ approver,
   approver not matching non-human prefixes), captured within a 15-minute validity window,
   not future-stamped;
3. Audit record written regardless of outcome (`SoarRecord`: id, ts, actor, approver,
   policy decision, result, error).

`rollback(record_id)` re-runs the same gates before undoing an executed action.

## Trust Boundaries

- **Kernel boundary:** services emit events; they cannot invoke SOAR directly except
  through the same authorizer path as humans.
- **Audit boundary:** JSONL sink is append-only from the kernel's perspective; rotation
  and off-box shipping are operator duties (see metrics.md).
- **Authority boundary:** approvals are bound to human principal IDs at capture time and
  are single-use per action execution.

## Integration Points (planned wiring, NOT TESTED)

- `apps/api/security.py` failure paths → AUTH-BRUTEFORCE events.
- Break-glass mint/verify in `apps/api/main.py` → BG-* events.
- `apps/api/pilot.py` suspend/resume → KS-TAMPER events.
- OPA denial middleware → POLICY-DENY-BURST events.
- NATS ingress validation → NATS-* events.
- Asset telemetry ingest → ASSET-TELEPORT / IMPOSSIBLE-TRAVEL events.
