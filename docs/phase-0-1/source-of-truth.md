# Source-of-Truth Matrix

| Question | Source of truth |
| --- | --- |
| Who is the user? | Keycloak |
| Is the user allowed to perform the action? | OPA |
| What incident exists? | PostgreSQL |
| What event occurred? | NATS/event layer |
| What important action happened? | Audit state |

**Core rule:** If two systems claim to be authoritative for the same fact, the architecture is unfinished.
