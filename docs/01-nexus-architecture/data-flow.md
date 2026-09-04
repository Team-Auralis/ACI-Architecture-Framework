# Data Flow

The exact traversal of an event through the ORION mesh.

1.  **Request Ingestion:** A client sends a `POST` request with an `Idempotency-Key` header.
2.  **Authentication Verification:** The API validates the JWT token against Keycloak's public keys.
3.  **Authorization Request:** The API constructs an authorization context (User ID, Role, Action, Resource) and queries the OPA sidecar.
4.  **Policy Evaluation:** OPA evaluates the context against its Rego rules and returns `ALLOW` or `DENY`. (If DENY -> HTTP 403).
5.  **Idempotency Check:** The API checks PostgreSQL for the `Idempotency-Key`. If found, it returns the cached response and halts.
6.  **State Mutation:** The API inserts the new record into PostgreSQL.
7.  **Event Publication:** The API constructs an `incident.created` JSON event and publishes it to the NATS broker.
8.  **API Response:** The API returns HTTP 200 to the client.
9.  **Asynchronous Processing:** A Worker receives the event from NATS, checks its local consumer idempotency cache, and processes the business logic.
