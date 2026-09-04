# Resilience Model

Enterprise software aims for High Availability (HA). ORION requires **Continuous Survivability**.

## The Illusion of 99.99% Uptime
Cloud providers guarantee 99.99% uptime *within their data centers*. During a natural disaster, the cloud data center is perfectly fine, but the fiber optic lines connecting the disaster zone to the cloud are severed. To the responders on the ground, the uptime is 0%.

## The ORION Survivability Paradigm
ORION is built on the assumption that the "Cloud" is a luxury, not a requirement.
The resilience model dictates that compute and state must push as far to the edge as possible. An ORION Edge Node (Responder Vehicle) must contain enough localized compute (FastAPI), localized state (PostgreSQL/SQLite), and localized routing (NATS Leaf Node) to function as a complete mini-ORION deployment if the global umbilical cord is cut.
