# FORGE RANGE — Cyber Range Plan

Status: PLAN ONLY. The range has never been exercised end-to-end because Docker was
offline throughout this program phase. Everything below is designed but NOT TESTED.

FORGE RANGE is the isolated rehearsal environment where FORGE CYBER detections and SOAR
playbooks are validated against scripted adversary behavior before any reliance is placed
on them.

## Isolation Requirements

- Dedicated docker-compose profile (`--profile forge-range`); no shared networks, volumes,
  or ports with the pilot stack.
- Synthetic data only: seeded fake assets/incidents/users; no production credentials.
- Range teardown script must remove all containers, volumes, and temp files.
- Host egress disabled for range containers except an internal registry mirror.

## Topology

```
[adversary container]──┐
                       ├─> [range net] ── api ── postgres ── redis ── nats ── opa ── keycloak
[simulator scripts]────┘                                        │
                                                          [event tap] ──> FORGE CYBER kernel ──> audit JSONL
```

## Scenario Catalog

Each scenario = setup script + adversary actions + expected Finding IDs + expected SOAR
behavior. Mapped from confirmed findings so the range replays real weaknesses.

| ID | Scenario | Adversary Actions | Expected Detection | Expected Response |
|---|---|---|---|---|
| T1 | Credential brute force | 6 failed logins in 60s | AUTH-BRUTEFORCE | alert only (medium) |
| T2 | Impossible travel | tokens used from far geos <1h apart | IMPOSSIBLE-TRAVEL | high finding; step-up prompt |
| T3 | Break-glass spike | 3 mints within 1h | BG-SPIKE | critical; human review task |
| T4 | Kill-switch tamper | non-operator resume attempt via direct service call | KS-TAMPER | deny + critical alert |
| T5 | Policy burst probe | >10 OPA-denied requests | POLICY-DENY-BURST | medium; subject throttled |
| T6 | Rogue publisher | publish to `asset.dispatch` off-allowlist | NATS-UNAUTHORIZED-PUBLISHER | critical; publisher quarantined (manual) |
| T7 | Oversize/ReDoS payload | 300KB payload; adversarial email string | PAYLOAD-OVERSIZE; latency SLO check | reject 422; no degradation |
| T8 | Asset teleport | position jump >160km/h | ASSET-TELEPORT | high; dispatch freeze recommendation |

## Purple Loop

1. Run scenario → capture events/Finding/SOAR records.
2. Diff actual vs expected table above.
3. Any miss = detection bug or telemetry gap → file issue → fix → rerun.
4. Record MTTD (event→finding) and MTTR (finding→resolved action) into metrics.md.

## Exit Criteria (before any production reliance)

- All T1–T8 produce the expected findings with zero false positives across a clean-run
  triple.
- SOAR high-impact actions are impossible without distinct-human approval (negative tests:
  self-approval, AI-prefix approver, expired TTL each fail).
- Audit sink contains a record for every execution attempt including denials.

## Safety Controls Inside the Range

- No outbound network from adversary container after setup.
- All destructive SOAR actions in-range target synthetic state only.
- Range shares no secrets with pilot environment (separate realm export, separate keys).
