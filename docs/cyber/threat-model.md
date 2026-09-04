# FORGE CYBER — Threat Model (Grounded)

Scope: PROJECT ORION as built at current HEAD, restricted to threats **confirmed during
the red-team exercise of this session** plus their defensive coverage. Vision-level
threats live in `docs/05-veil-security/threat-model.md`; this document records what is
actually true today. Docker was offline: all "live" attack proofs below were executed
against unit-level harnesses or logic probes (`scripts/redteam_probe.py`), and items
marked NOT TESTED require the live stack.

## Method

STRIDE per subsystem, cross-referenced with confirmed findings from the session red-team
report (R-01..R-10) and kill chains (C1..C5). Each row maps to a FORGE CYBER detection or
a remediation status.

## Confirmed Findings → Coverage

| ID | Finding | STRIDE | Status @ HEAD | Detection / Control |
|---|---|---|---|---|
| R-01 | Phoenix Fallback blanket `except Exception` misclassifies validation/idempotency errors as DB-offline; publishes to NATS without DB row; returns 202 DEGRADED | T(Repudiation), I | OPEN | Needs error-classification before fallback; future NATS-UNKNOWN-SUBJECT + outbox reconciliation would catch orphan publishes |
| R-02 | Redis-down ⇒ unhandled ConnectionError in circuit check ⇒ 500 on protected routes; JWKS `{}` ⇒ all JWT 403 (full outage) | D | OPEN | Fail-closed path exists in pilot gate but API-wide handling missing |
| R-03 | Status updates return 200 with no persistence/outbox; silent loss when NATS down | T, R | OPEN | Outbox pattern required; audit gap flagged |
| R-04 | Open Redis write access ⇒ DEL `pilot:suspended*` defeats kill switch; SETEX `circuit_open:OPA` ⇒ fleet 503 (logic probe-proven) | E, D, T | MITIGATED: requirepass + credentialed URL + core/edge network segmentation (redis/postgres/nats/opa unreachable from edge tier); host ports removed | KS-TAMPER detection wired via emitter; live ACL verification pending Docker |
| R-05 | `/v1/assets` OPA-gated but `policy.rego` lacked `dashboard:view`+`assets` rule ⇒ 403 for everyone incl. operators | D | FIXED (Rule 2b added) | Rego rule + suite green |
| R-06 | Break-glass tokens stored plaintext | I | FIXED @ HEAD (SHA-256 hashed storage + identity binding) | f10/f2 tests green; BG-TOKEN-ABUSE covers replay attempts going forward |
| R-07 | NaN/Infinity coordinates accepted by pydantic ⇒ NOT NULL violation ⇒ Phoenix misfire | T | FIXED (`allow_inf_nan=False` + range validators on Location/AssetStatusUpdate + sanitized 422 handler — the raw handler crashed serializing `nan` echoes) | tests/test_r07_r09.py |
| R-08 | Secrets committed in git history | I | ROTATED in current tree (realm passwords, dashboard creds, TLS key untracked, Grafana env-driven) + guard tests; HISTORY SCRUB PREPARED (`scripts/security/scrub_history.py`, runbook `docs/cyber/secret-rotation-runbook.md`) — execution requires quiesced repo + coordinated force-push | Previously pushed secrets remain burned until provider-side rotation |
| R-09 | Global rate-limit bucket: citizen failures consume operator budget ⇒ operator 429 | D | FIXED (key_func partitions per JWT `sub`, IP fallback for anonymous/garbage tokens) | tests/test_r07_r09.py |
| R-10 | jose/starlette dependency risk flags | V/I | OPEN | Pin + advisory monitoring |

## Kill Chains → Defensive Posture

| Chain | Path | Current Barrier | Residual Risk |
|---|---|---|---|
| C1 | `.env` leak → KC admin → operator role → break-glass | Keycloak hardening (F12), BG role-gate + hashing @ HEAD | Git history still contains old secrets until scrubbed |
| C2 | Open OPA port → policy PUT → allow-all | compose port isolation landed (f7 test) | Live verification pending (Docker offline) |
| C3 | Open Redis → kill-switch flush / circuit forge | Partial network isolation | KS-TAMPER detection wired at integration stage |
| C4 | Open NATS → ReDoS payload / AI poisoning | Size cap (422) + mask_pii rewrite landed | AI fallback keyword extraction regression under review |
| C5 | Civilian input → dispatch manipulation | HITL distinct-human approval, expired/double-approve/double-dispatch all PASS | R-01 orphan-publish path remains |

## Assets & Trust Boundaries

1. **Break-glass authority** — highest-value target; now hashed, role-gated, identity-bound.
2. **Kill switch state (Redis)** — single point of safety authority; must be write-restricted.
3. **OPA policy store** — controls all authorization; must be read-only to services.
4. **NATS subjects** — command surface for assets; publisher allowlists required.
5. **Audit sinks** — must be append-only and off-box shippable.

## Explicitly NOT TESTED

- End-to-end exploitation of C1/C2/C3/C4 against live containers.
- P1.5-012 chaos drills (Redis/NATS/Postgres kill tests).
- e2e suite (skipped when stack unreachable).
- Rate-limit behavior under concurrent multi-node load.

## Top Remediation Queue (remaining)

1. Redis ACL + auth (completes R-04 mitigation).
2. Git history secret scrub + credential rotation (R-08 remainder).
3. Outbox/reconciliation for any remaining non-outbox publishes (R-03 class).
4. Wire FORGE CYBER kernel integration points once live stack is available.
