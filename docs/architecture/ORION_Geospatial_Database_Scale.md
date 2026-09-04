# ORION: Global Geospatial Data Scale

## The Problem
ORION must route emergency responders (assets) to incidents (SOS signals) globally in real time. This requires complex geospatial queries (e.g., `ST_DWithin` to find the 5 closest helicopters to a coordinate). Standard PostgreSQL with the PostGIS extension is incredibly powerful, but it does not scale horizontally. If we put the entire planet's telemetry into one database, it will buckle.

## The State-of-the-Art Solutions

### 1. Citus + PostGIS (Distributed PostgreSQL)
*   **How it works:** Citus shards a standard PostgreSQL database across multiple physical nodes. Because it's a pure extension, you get 100% of the advanced PostGIS spatial functions.
*   **The Catch:** It requires manual sharding (e.g., sharding by `country_id`). If an incident occurs on a border, cross-shard spatial joins can become extremely expensive and slow.

### 2. CockroachDB (Native Distributed Spatial)
*   **How it works:** CockroachDB built a custom spatial indexing engine (divide-the-space quad-trees) from scratch rather than relying on PostGIS's R-Trees. 
*   **The Benefit:** It is designed for multi-region, active-active global survival. If the US-East region goes offline, EU-West takes over seamlessly. The database handles the sharding of geometry data automatically.
*   **The Catch:** It is highly compatible with PostGIS, but does not support 100% of its obscure analytical functions.

## ORION Architecture Recommendation
**CockroachDB Spatial.** 

ORION is an operational, high-survival system, not a batch analytics warehouse. Our spatial queries are relatively simple: distances, containment, and radius searches. We need the data to survive the loss of an entire data center more than we need advanced cartographic projections. By using CockroachDB, we get native, globally distributed geographic routing out of the box, ensuring the "State" layer matches the global survival capability of the NATS "Event Mesh" layer.
