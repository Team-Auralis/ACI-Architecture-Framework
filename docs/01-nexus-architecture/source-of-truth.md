# Source of Truth Matrix

In distributed systems, overlapping authorities lead to split-brain failures. 

**Core Rule: If two systems claim to be authoritative for the same fact, the architecture is unfinished.**

| Domain | Question | Authoritative System |
| :--- | :--- | :--- |
| **Identity** | "Who is this user/device?" | **Keycloak** (or edge SPIRE) |
| **Policy** | "Are they allowed to do this?" | **OPA** (Open Policy Agent) |
| **State** | "What is the current status?" | **PostgreSQL** (or CockroachDB) |
| **Events** | "What actions just occurred?" | **NATS** (Event Fabric) |
| **Audit** | "Who did what and when?" | **Append-Only Audit Log** |

If the API tries to evaluate policy, or if NATS tries to store permanent relational state, the architecture has been violated.
