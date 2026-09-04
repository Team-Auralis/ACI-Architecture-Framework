# ORION SECURITY AUDIT BRIEF
**Version:** 1.0 (Phase 1.5 Hardening Gate)
**Classification:** RESTRICTED
**Target Audience:** External Red Team / Security Validation Partners

## 1. Engagement Scope
This document outlines the architecture, assumed boundaries, and explicit targets for the ORION Phase 1.5 external security audit. The purpose of this engagement is to validate that the ORION platform can safely operate in a closed, physical pilot environment without risking uncontrolled dispatch of responder assets or exposing PII.

### In Scope
- **FastAPI Surface Area:** All /v1/* endpoints, specifically SOS ingestion, incident queries, asset status updates, and dispatch recommendations.
- **Authentication Boundary:** Keycloak JWT issuance and FastAPI verification logic.
- **Authorization Boundary:** OPA policy enforcement and the Break-Glass bypass mechanism.
- **Data Integrity:** The Transactional Outbox pattern between PostgreSQL and NATS, specifically looking for race conditions or stale data overwrites.
- **Pilot Controls:** The Geofence constraint engine and the distributed Redis-backed Kill Switch.

### Out of Scope (DO NOT TEST)
- Denial of Service (DoS) attacks against the live physical infrastructure (e.g., flooding LoRaWAN hardware gateways).
- Social engineering or phishing of authorized operators.
- Exploitation of underlying cloud provider infrastructure (e.g., AWS/GCP hypervisor escapes).
- Destructive data manipulation that permanently corrupts the PostgreSQL schemas (use designated test tenants only).

## 2. Architectural Boundaries & Expectations

### 2.1 Authentication & Authorization
**Model:** Zero-Trust (Decoupled Identity & Policy)
- **Identity (Keycloak):** All endpoints (except public civilian ingestion) require a valid JWT issued by the ORION Keycloak realm. The API verifies the signature using Keycloak's public JWKS endpoint.
- **Policy (OPA):** The API does not contain hardcoded RBAC rules. It delegates authorization decisions to the Open Policy Agent (OPA) via HTTP POST. 
- **Break-Glass:** A dedicated bypass mechanism exists. An operator can supply a valid \X-Break-Glass-Token\ mapped to an active \BreakGlassSession\ in the database to securely bypass the OPA network call during critical outages.

### 2.2 Human-in-the-Loop (HITL) Dispatch
ORION no longer supports autonomous physical dispatch. The AI is restricted to a \classify -> recommend -> explain\ paradigm.
- **State Machine:** Assets cannot be directly forced into a \DISPATCHED\ state via the standard status endpoint.
- **TTL & Expiry:** Dispatch recommendations expire after 10 minutes (600s).
- **Concurrency:** Optimistic Concurrency Control (OCC) using SQLAlchemy \ersion_id_col\ guarantees that double-approvals resulting from network jitter or concurrent operator actions will fail safely with a \StaleDataError\.
- **Attribution:** The JWT \subject\ is cryptographically bound to the final \esolved_by\ field of the recommendation.

### 2.3 Physical Pilot Safety Controls
To prevent real-world chaos during the pilot:
- **Geofence:** Ingestion endpoints evaluate incoming coordinates against a rigid \min_lat,min_lon,max_lat,max_lon\ bounding box.
- **Kill Switch:** A fail-closed, Redis-backed kill switch completely freezes ingestion and downstream dispatch approvals. If Redis is partitioned or unavailable, the system defaults to suspended.

## 3. Known Limitations & Acceptable Risks
- **Test Snapshots:** Disaster Recovery RTO has been validated (1.60s) on a 0.21MB test snapshot. Production-scale CRDT merge recovery under massive load is pending Phase 2 telemetry validation.
- **Secret Management:** The application currently relies on environment variables (\.env\) for component binding (PostgreSQL passwords, Keycloak admin credentials). Migration to a dynamic secret manager (e.g., HashiCorp Vault) is scheduled for Phase 2.

## 4. Execution Rules of Engagement
1. All automated scanning must be throttled to respect the \SlowAPI\ rate limits (default: 5 req/minute per IP on ingestion).
2. Report any findings related to complete system lockout (e.g., inadvertently triggering the Kill Switch globally via unauthenticated vectors) immediately as a Sev-1.
3. Use the provided \scripts/security_probe.py\ script as a baseline reference for intended integration tests.

