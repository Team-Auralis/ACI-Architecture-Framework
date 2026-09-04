# Data Architecture

ORION does not dump everything into a single monolithic database.

## CQRS & Event Sourcing
ORION utilizes Command Query Responsibility Segregation (CQRS).
*   **The Write Path (Command):** When an SOS is received, it hits FastAPI, clears OPA, and is written to PostgreSQL as an immutable state change. This path must be lightning-fast and highly available.
*   **The Read Path (Query):** The Next.js Dashboard does not run complex `JOIN` queries against the write database. Instead, a NATS Worker listens to the `incident.created` events and builds a highly optimized "Read View" (e.g., a materialized view or a Redis cache) specifically tailored for the UI.

This prevents the dashboard from crashing the ingestion engine when 5,000 operators refresh their screens simultaneously.
