# Zero Trust Architecture

Implicit trust is dead.

In traditional enterprise networks, if a server is behind the corporate firewall, it is trusted. In ORION, there is no firewall. A responder vehicle connects via public 5G, civilian phones connect via open Bluetooth, and satellite modems beam unencrypted RF to space.

## The Principles of VEIL Zero Trust
1.  **Assume Breach:** Every component assumes the network it sits on is hostile and actively monitored.
2.  **Verify Explicitly:** Every single request (HTTP or NATS) must carry cryptographic proof of identity (JWT or mTLS).
3.  **Least Privilege:** An AI agent that analyzes telemetry cannot issue a dispatch order. An operator in Sector A cannot view data for Sector B.
4.  **No Implicit Trust Zones:** Just because a worker microservice is running on the same Docker bridge network as the Postgres database does not mean it is allowed to connect.
