# Terrestrial Networks

Standard fiber optic backbones and 5G cellular networks.

## The Primary, Untrusted Medium
Under normal operating conditions, 99% of ORION traffic flows over standard terrestrial networks. However, AEGIS treats terrestrial networks as highly volatile.

*   **Public 5G:** Used by civilians and responders for high-bandwidth data. AEGIS assumes these networks will become instantly saturated during an emergency (the "Mother's Day Effect" where everyone calls simultaneously).
*   **Fiber Backhaul:** Used to connect regional NATS Superclusters. AEGIS assumes fiber lines are highly susceptible to physical destruction (earthquakes, backhoes). 

Because terrestrial networks are untrusted, every node is pre-configured to execute the Fallback Protocol the millisecond a connection timeout is detected.
