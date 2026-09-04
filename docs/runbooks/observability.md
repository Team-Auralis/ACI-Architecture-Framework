# Observability Runbook

## Purpose

Use ORION telemetry to detect SLO breaches, trace failed emergency flows, and provide evidence for incident review.

## Signals

| Signal | Source |
|---|---|
| API HTTP metrics | Prometheus scrape of `orion-api:8001` via `infra/prometheus/prometheus.yml`. |
| Worker metrics | Prometheus scrape of `orion-worker:8002`. |
| Worker processing latency | `worker_processing_latency_seconds`. |
| Worker duplicate drops | `worker_duplicates_dropped_total`. |
| Worker processed events | `worker_events_processed_total`. |
| Distributed traces | OpenTelemetry OTLP exporter configured by `OTEL_EXPORTER_OTLP_ENDPOINT`. |
| Mutation audit | `logs/chronos_audit.jsonl`. |
| Pilot events | `PILOT_SUSPENDED`, `PILOT_RESUMED`, `PILOT_GEOFENCE_REJECTED` in CHRONOS. |

## Dashboard Checks

1. API request rate and error rate.
2. `POST /v1/incidents` latency p50/p95/p99.
3. `POST /v1/incidents` `4xx` and `5xx` breakdown.
4. Worker processing latency histogram.
5. Worker duplicate drop rate.
6. Outbox unpublished row count.
7. Redis availability and key write failures.
8. NATS connection and JetStream consumer lag.
9. OPA and Keycloak request failures.

## Alert Thresholds

| Alert | Page |
|---|---|
| SOS p95 latency > 1s for 15 minutes | SEV-2 |
| SOS create 5xx rate > 1% for 5 minutes | SEV-1 |
| Any unauthorized dispatch suspected | SEV-0 |
| Outbox unpublished backlog grows for 5 minutes | SEV-1 |
| Worker processed counter flat while NATS has pending `incident.*` messages | SEV-1 |
| Duplicate drop counter rises suddenly | SEV-2, SEV-1 if paired with user-visible duplicates |
| OPA circuit breaker open | SEV-1 |
| Keycloak circuit breaker open with stale JWKS only | SEV-2, SEV-1 if auth fails |
| Pilot geofence misconfiguration | SEV-1 and fail closed |

## Trace Walk

For one SOS:

1. Start with the API span around `POST /v1/incidents`.
2. Confirm trace headers were injected into the NATS message.
3. Follow `process_nats_message` in the worker.
4. Confirm DB write or CRDT merge happened once.
5. Confirm any AI triage event led to a recommendation, not direct dispatch.

## CHRONOS Review

Use CHRONOS to answer who changed what and when. Review:

- `POST`, `PUT`, `PATCH`, `DELETE` API mutation entries.
- Break-glass activation entries.
- Pilot suspend/resume/rejection entries.
- Dispatch approval/rejection mutation entries.

Never edit CHRONOS in place during incident response. Copy evidence into the incident report instead.

