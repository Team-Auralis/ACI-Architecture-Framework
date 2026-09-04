# FORGE CYBER — Metrics

Status: definitions implemented in kernel outputs; baselines UNMEASURED (no live-stack
runs yet — Docker offline). Every number reported here must come from recorded evidence,
never estimates.

## Core Definitions

| Metric | Definition | Collection Point |
|---|---|---|
| MTTD | `Finding.emitted_at − first evidence event.ts` for same rule/window | DetectionEngine output vs SecurityEvent timestamps |
| MTTR | `SoarRecord(result=executed).ts − Finding.emitted_at` (+ human latency separately) | SOAR audit JSONL |
| Detection Yield | findings confirmed true-positive ÷ total findings, per rule | purple-loop review of range runs |
| False Positive Rate | false positives ÷ total findings, per rule | same |
| Approval Latency | approval.ts − request time, high-impact actions | SoarRecord fields |
| Rollback Success | rollbacks completing without residual effect ÷ attempted | rollback() outcomes in audit |
| Event Loss | events emitted by services ÷ events observed by kernel | producer counters vs ingest counters |
| Audit Completeness | SOAR attempts with audit record ÷ total attempts | must be 100% by construction; verified in tests |

## Current Honest Baseline

- MTTD / MTTR / yield / FP-rate: **unknown** — requires FORGE RANGE runs (T1–T8).
- Kernel functional correctness: covered by 25 unit tests in `tests/test_cyber_kernel.py`
  (windowing, thresholds, approval gates, TTL expiry, non-human approver rejection,
  default-deny authorizer, audit-on-deny, rollback gating).
- Platform suite health: 66 passed / 2 skipped (live-stack) / 0 failed at time of writing.

## Reporting Rules

1. Metrics are computed from the JSONL audit sink only — no hand-assembled numbers.
2. Any metric that cannot be computed due to event loss is reported as UNKNOWN with the
   loss figure attached, never interpolated.
3. Rule-level FP data feeds threshold tuning; tuning changes require a range re-run of the
   affected scenarios before adoption.

## Dashboards (planned, NOT BUILT)

- Per-rule finding counts and MTTD percentiles (p50/p95).
- High-impact action queue: pending approvals with age vs 15-min TTL.
- Kill-switch state timeline reconciled against KS-TAMPER findings.
