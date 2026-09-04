# Analytics & Intelligence Extraction

How we query billions of rows without breaking the system.

## The Analytical Warehouse
Operational databases (Postgres) are optimized for single-row inserts and lookups. If an analyst wants to know the average response time to medical SOS signals during hurricane conditions over the last 5 years, running that query on Postgres will lock tables and crash the system.

OMNIS streams all NATS events into an asynchronous analytical warehouse (e.g., ClickHouse or Apache Iceberg) hosted entirely in the Cloud Core. 
This allows infinite complex querying by Data Scientists and Strategic Planners without ever touching the live operational mesh.
