# ORION Secure AI-Orchestrated Resilient Communication & Coordination

## 1. The Core Objective (ORION 0.1)
**Goal:** Prove two devices can communicate via a simulated SOS workflow, with an independent policy engine validating the action.

**One sentence objective:**
> Two authenticated devices → submit SOS → OPA independently authorizes it → FastAPI persists the incident → event bus publishes `incident.created` → dashboard receives/displays it.

---

## 2. Source of Truth (The Most Important Principle)
This matrix prevents scope creep and spaghetti logic.

| Decision | Authority |
| :--- | :--- |
| Who is the user? | **Keycloak** |
| Is the action permitted? | **OPA** |
| What incident exists? | **PostgreSQL** |
| What happened asynchronously? | **NATS/event log** |
| Was the operation audited? | **Audit store** |

---

## 3. Final V0.1 Architecture

```text
                 ┌─────────────────────┐
                 │  Mobile / Test App  │
                 └──────────┬──────────┘
                            │
                            ▼
                    ┌──────────────┐
                    │   FastAPI    │
                    │  API Layer   │
                    └──────┬───────┘
                           │
                 ┌─────────┴─────────┐
                 │                   │
                 ▼                   ▼
            ┌─────────┐        ┌──────────┐
            │ Keycloak│        │   OPA    │
            │ Identity│        │  Policy  │
            └─────────┘        └────┬─────┘
                                    │
                             ALLOW / DENY
                                    │
                                    ▼
                              ┌──────────┐
                              │PostgreSQL│
                              └────┬─────┘
                                   │
                              incident.created
                                   │
                                   ▼
                               ┌───────┐
                               │ NATS  │
                               └───┬───┘
                                   │
                    ┌──────────────┴──────────────┐
                    ▼                             ▼
              Dummy Worker                 Future AI Agent
                    │
                    ▼
             Next.js Dashboard
```

**Do not add Kubernetes, microservices, Kafka, service mesh, Terraform, multi-region deployment, satellite hardware, or autonomous AI in V0.1.**

---

## 4. API Contract - POST /v1/incidents
**Request:**
```json
{
  "type": "SOS",
  "location": {
    "latitude": 17.6868,
    "longitude": 83.2185
  },
  "message": "Emergency assistance required",
  "source": "mobile"
}
```

**Response:**
```json
{
  "incident_id": "INC-01J...",
  "status": "CREATED",
  "created_at": "2026-08-17T12:30:00Z"
}
```
*Authorization happens **before** the database write.*

---

## 5. Event Contract - incident.created
```json
{
  "event_id": "evt-123",
  "event_type": "incident.created",
  "version": 1,
  "timestamp": "2026-08-17T12:30:00Z",
  "incident_id": "INC-123",
  "actor_id": "user-456",
  "incident_type": "SOS",
  "correlation_id": "req-789"
}
```

---

## 6. OPA Policy Firewall

**Citizen SOS Flow:**
```text
authenticated user
        +
action = create_incident
        +
type = SOS
        ↓
       ALLOW
```

**Negative Path (CRITICAL):**
```text
role = citizen
        +
GET /admin
        ↓
       DENY
```
*FastAPI asks. OPA decides.*

---

## 7. Definition of Done (ORION 0.1)

Your team should not call Phase 0 complete until this exact demo works:

1. User logs into mobile app
2. User presses SOS
3. FastAPI receives request
4. Keycloak authenticates user
5. OPA evaluates policy -> **ALLOW**
6. PostgreSQL stores incident
7. NATS publishes `incident.created`
8. Worker receives event
9. Dashboard shows incident
10. Audit record exists

**The Negative Test:**
1. Unprivileged user hits Admin endpoint
2. OPA -> **DENY**
3. HTTP 403
4. **No unauthorized state change**

---

## 8. Development & Scaffolding Plan
1. **Infrastructure Owner:** Stands up `docker-compose.yml` (Keycloak, OPA, Postgres, NATS).
2. **Security Owner:** Configures Keycloak realms and OPA Rego policies.
3. **Backend Owner:** Connects FastAPI to Keycloak, OPA, Postgres, and NATS.
4. **Frontend Owner:** Builds dashboard to read API without needing to know how infra works.

*The infrastructure scaffold is the first executable milestone.*
