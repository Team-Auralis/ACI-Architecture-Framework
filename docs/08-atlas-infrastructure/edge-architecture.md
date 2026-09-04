# Edge Architecture

The Tactical Edge is where ORION wins or loses.

## The Responder Vehicle Node
A standard ORION tactical edge node is a ruggedized 2U server mounted in an emergency vehicle. It contains:
*   **Compute:** x86 architecture with dedicated AI accelerators (e.g., NVIDIA T4/L4 GPUs) for local inference.
*   **Storage:** NVMe SSDs with TPM 2.0 hardware encryption.
*   **Power:** Integrated UPS with multi-day battery survival independent of the vehicle's engine.

## The Software Payload
Even while disconnected from the cloud, this box runs:
1.  A local NATS Leaf Node.
2.  A local PostgreSQL database.
3.  The FastAPI Gateway.
4.  The OPA Policy Engine.
5.  A local SPIRE server for credential issuance.

It is a complete, miniaturized ORION deployment, capable of coordinating a 50-mile local mesh autonomously.
