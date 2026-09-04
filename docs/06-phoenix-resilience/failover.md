# Active-Active Failover

There are no "Backup Data Centers" in ORION. Backup data centers require humans to press a button and execute a DNS swap, which takes minutes or hours.

## Global Routing
ORION utilizes a purely **Active-Active** global architecture.
*   **State:** The database (CockroachDB) spans multiple global regions. Every region is actively serving reads and writes. If Region A dies, Regions B and C automatically absorb the traffic.
*   **Events:** The NATS Event Mesh is deployed as a global Supercluster. Gateways continuously monitor connection health. If a gateway in Europe fails, traffic is seamlessly routed to the gateway in North America.

There is zero downtime during a cloud region failure.
