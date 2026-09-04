# Recovery Testing (Chaos Engineering)

Resilience is a muscle. If you do not exercise it, it atrophies.

## The ORION Game Days
ORION engineers utilize **Chaos Engineering** to prove the system works.
*   **Simulated Cuts:** In staging (and eventually production), automated scripts randomly kill PostgreSQL nodes, sever NATS Gateway connections, and arbitrarily inject 5000ms latency into internal network routes.
*   **Blackhole Testing:** Randomly blocking the IP ranges of simulated Edge Nodes to force them into Degraded Mode, verifying they continue to serve local traffic, and then restoring the IPs to verify the resynchronization burst occurs flawlessly without dropping events.

If a component cannot survive the Chaos Engineering suite, it is removed from the architecture.
