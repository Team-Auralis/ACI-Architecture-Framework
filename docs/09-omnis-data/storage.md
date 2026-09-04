# Storage Primitives

Data lives in different houses depending on its shape.

1.  **Relational State (PostgreSQL / CockroachDB):** The absolute source of truth for incidents, dispatch orders, and user roles. Requires strict ACID compliance.
2.  **Event Log (NATS JetStream):** The immutable, append-only ledger of everything that happened. Used to replay state if a database crashes.
3.  **Time-Series (TimescaleDB):** Optimized for massive ingestion of numerical telemetry (sensor readings, GPS tracks).
4.  **Object Storage (MinIO):** S3-compatible blob storage deployed at the edge. If a civilian uploads a 5MB photo of a collapsed building, it is stored in the local MinIO bucket on the responder vehicle. Only a low-res thumbnail is sent to the cloud to save bandwidth.
