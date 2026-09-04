# Phase 2 — FORGE CYBER (Defensive Security Program)

Phase 2 hardens ORION's defenses and proves them, rather than expanding features.

## Delivered (tested)

- `services/cyber/` kernel: normalized security-event schema, 11-rule detection engine,
  policy-gated SOAR with distinct-human approval, TTL, rollback, append-only audit.
  25/25 unit tests green (`tests/test_cyber_kernel.py`).
- Kernel wiring live: `services/cyber/emitter.py` emits security events from auth
  failures, break-glass mint/use/denials, OPA denials, and kill-switch suspend/resume
  to a JSONL sink when `FORGE_CYBER_EVENTS` is set (inert by default)
  (`tests/test_cyber_wiring.py`).
- Full platform suite green: **87 passed / 2 skipped / 0 failed**.
- R-04 completed at config level: Redis requirepass + credentialed URL + edge/core
  network segmentation so the datastore tier is unreachable from edge containers
  (`tests/test_r04_hardening.py`).
- R-08 rotation executed in current tree: realm passwords rotated, dashboard
  direct-grant password env-driven, TLS private key untracked, Grafana password
  env-driven; guard tests `tests/test_no_secrets.py`; history scrub prepared via
  `scripts/security/scrub_history.py` + `docs/cyber/secret-rotation-runbook.md`.
- Red-team blockers closed this phase: R-01 (exception classification + idempotent
  replay), R-05 (rego Rule 2b), R-07 (finite/range coordinate validation + sanitized
  422 handler), R-09 (subject-partitioned rate keys) — regression-tested in
  `tests/test_r07_r09.py`.

## Documentation

- `docs/cyber/architecture.md` — component model, safety contract, trust boundaries.
- `docs/cyber/threat-model.md` — grounded STRIDE mapping of session-confirmed findings
  R-01..R-10 and chains C1..C5 with remediation status.
- `docs/cyber/range-plan.md` — FORGE RANGE topology, scenarios T1–T8, exit criteria.
- `docs/cyber/metrics.md` — MTTD/MTTR/yield definitions and reporting rules.

## Open Work (in priority order)

1. Execute git-history scrub (`scripts/security/scrub_history.py --execute`) during a
   quiesced window with coordinated force-push; rotate provider-side credentials
   (see `docs/cyber/secret-rotation-runbook.md`).
2. Live verification of R-04 segmentation + Redis ACL behavior once Docker is
   available (compose config is static-tested only).
3. Build FORGE RANGE profile and execute scenarios T1–T8; record first real MTTD/MTTR
   baselines into `docs/cyber/metrics.md`; verify emitter → DetectionEngine pipeline
   end-to-end.
