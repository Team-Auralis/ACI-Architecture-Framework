# Phase 1.5: Deployment Hardening Gate

**Status:** IN PROGRESS // PRE-FLIGHT

While Phase 1 successfully established the functional core of the ORION platform (API, Mesh, AI, Dispatch), the system is classified as a **Technically Validated Prototype**. Before it can be exposed to public networks or relied upon by real emergency responders, it must pass this critical hardening gate.

## Objectives

### 1. Operational Controls (Human-in-the-Loop) - ?? CLEARED (Implementation) / ?? PENDING (E2E OPA)
- [x] Implement explicit operator approval workflows for physical asset dispatch. *(Completed: P1.5-009 DispatchRecommendation API)*
- [x] Transition AI strictly to a classify -> recommend -> explain paradigm. *(Completed: P1.5-009 Worker refactored to queue instead of dispatch)*
- [x] Implement a **Policy Recheck** step immediately preceding physical dispatch to prevent UI bypass. *(Completed: OPA checks in the action endpoint)*
- [x] **Asset State Machine & OCC**: Implement deterministic state tracking for responder assets using Optimistic Concurrency Control. *(Completed: P1.5-010)*
- [x] **HITL Safety Verification**: Authenticated, authorized, time-bounded, concurrency-safe, and auditable HITL approval verified (3/3 test suite passed via Break-Glass OPA bypass). 
- [ ] **End-to-End Validation**: Normal live OPA approval-path integration remains pending.

### 2. Observability & SRE
- [x] Deploy Prometheus and Grafana for metrics visualization.
- [x] Implement OpenTelemetry distributed tracing across the API and CRDT workers. *(Completed: Trace propagation over NATS headers verified)*
- [x] Define measurable Service Level Objectives (SLOs) (e.g., < 1s SOS acceptance latency, > 99.9% availability).

### 3. Reliability & Recovery - ?? CLEARED (Test Scope) / ?? PENDING (Scale)
- [x] Test deterministic max-state merge strategies under load (CRDT semantics).
- [x] **NATS Silent Loss Bug Fixed**: Transactional Outbox pattern implemented so database commits and NATS publishes are atomic. *(Completed: P1.5-007)*
- [x] **Worker Deduplication**: Transitioned from in-memory LRU cache to persistent Redis deduplication. *(Completed: P1.5-008)*
- [x] Design and test PostgreSQL backup/restore procedures. *(Completed: P1.5-011 dr_backup_restore.py)*
- [x] **Live DR Drill**: A live backup/restore drill measured an RTO of 1.60 seconds for a 0.21 MB test snapshot.
- [ ] **Production Scale DR**: Production-scale recovery evidence remains pending.
- [ ] Run failure/recovery drills on NATS cluster partitions.

### 4. Security & Privacy - ?? CURRENT FOCUS
- [x] Implement application-layer rate limiting and abuse protection with measurable metrics. *(Completed: SlowAPI implemented)*
- [x] **Data Minimization (PII Masking)**: Implemented regex engine to scrub SSN, Phone, and Emails from SOS messages before ingestion. *(Completed: P1.5-013)*
- [x] **Secret Stripping**: Stripped local developer passwords from codebase defaults. *(Completed: P1.5-013)*
- [ ] Migrate from .env files to a production Secret Manager with automated credential rotation.
- [ ] Execute an independent, third-party penetration test. *(Scope + acceptance criteria defined: docs/governance/pentest-scope.md — STATUS: PENDING, no tester engaged)*

### 5. Hardware Integration & Infrastructure
- [x] Implement AEGIS Hardware Gateway for LoRaWAN / Radio ingestion. *(P1.5-014: normalized adapters, validation, radio HMAC, and tests)*
- [x] Establish SRE runbooks for deployment. *(Completed: P1.5-015 docs/runbooks baseline)*

### 6. The Final Gate: Closed Pilot - ?? BLOCKED
- [ ] Run a controlled, authenticated pilot with a partnered emergency response organization in a geofenced area. *(P1.5-016 ?" Constraints finalized: geofence ingestion gate + operator kill switch in apps/api/pilot.py, OPA pilot actions, and docs/governance/pilot-plan.md. Pilot execution pending partner agency + remaining entry criteria.)*
