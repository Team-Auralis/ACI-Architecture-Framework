# ORION SRE Runbooks

**Status:** P1.5-015 baseline runbook set.

These runbooks define the first operator-ready procedures for deploying, observing, responding to, and recovering ORION during the Phase 1.5 hardening gate. They are intentionally conservative: if an action could affect public safety, operators must preserve human authorization, fail closed, and record the action in CHRONOS or the incident log.

## Runbook Index

| Runbook | Use when |
|---|---|
| [Deployment](deployment.md) | Promoting a new ORION build, changing configuration, or preparing a pilot environment. |
| [Incident Response](incident-response.md) | SOS ingestion, event mesh, dashboard, AI recommendation, or dispatch behavior is degraded. |
| [Observability](observability.md) | Checking Prometheus, Grafana, traces, logs, SLOs, and alert evidence. |
| [Disaster Recovery](disaster-recovery.md) | Backing up or restoring PostgreSQL, measuring RTO, or recovering from storage loss. |
| [Security and Break-Glass](security-break-glass.md) | OPA, Keycloak, policy circuit breakers, PII leakage, or audited emergency override handling. |
| [AEGIS Hardware Gateway](aegis-hardware-gateway.md) | LoRaWAN or direct-radio hardware ingress is failing, replaying, or producing invalid events. |
| [Closed Pilot Operations](pilot-operations.md) | Running, suspending, resuming, or exiting the geofenced partner pilot. |

## Severity Model

| Severity | Definition | Initial response target |
|---|---|---|
| SEV-0 | Potential public-safety harm, unauthorized physical dispatch, total SOS ingestion loss, or confirmed data exposure. | Page incident commander immediately; suspend pilot if active. |
| SEV-1 | Critical service degradation: API, Postgres, NATS, Redis, OPA, Keycloak, dashboard, or AEGIS ingress prevents normal operations. | Triage within 5 minutes. |
| SEV-2 | SLO breach, repeated retries, degraded dispatch recommendations, delayed worker processing, or partial observability loss. | Triage within 15 minutes. |
| SEV-3 | Non-urgent operational defect, documentation gap, dashboard cosmetic issue, or single recoverable failed probe. | Track in backlog. |

## Non-Negotiables

- AURA, dashboard status, AI triage, and AEGIS ingress are display or ingestion surfaces only; none may authorize dispatch.
- Physical asset dispatch requires explicit operator approval via `POST /v1/dispatch/recommendations/{id}/action`.
- OPA is rechecked immediately before dispatch action execution.
- If both database persistence and NATS publication are unavailable for a new SOS, the API must return `503`; do not claim acceptance.
- Pilot mode must fail closed on invalid geofence configuration.
- Break-glass access must be time-bound, justified, and audited.
- Docker is currently a known local blocker for live chaos drills; do not run Docker-based drills until the host daemon is restored.

## Core SLOs

| SLO | Target | Primary evidence |
|---|---|---|
| SOS acceptance latency | p95 under 1 second | API HTTP metrics and trace spans. |
| Availability | 99.9% during pilot window | API health, dashboard availability, incident creation success rate. |
| Event loss | Zero accepted SOS events lost | `outbox_events`, NATS/JetStream delivery, worker processed counters. |
| Autonomous dispatch | Zero | Dispatch recommendations table and CHRONOS mutation logs. |
| PII leakage | Zero unmasked civilian PII in persisted incident messages | Incident table sampling and CHRONOS review. |

