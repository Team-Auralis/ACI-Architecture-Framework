# AEGIS Hardware Gateway Runbook

## Purpose

Operate and troubleshoot LoRaWAN and direct-radio hardware ingress without allowing hardware traffic to bypass ORION safety controls.

## Normal Behavior

AEGIS accepts:

- The Things Stack-compatible LoRaWAN uplink webhooks.
- Direct-radio packets signed with HMAC-SHA256 over `DEVICE_ID:SEQUENCE:PAYLOAD_HEX`.

The gateway emits only `incident.created` events. It cannot dispatch assets. AI triage, recommendation creation, OPA checks, and human approval remain mandatory downstream.

## Required Configuration

- `NATS_URL` points to the authenticated NATS/JetStream route.
- `AEGIS_DEVICE_SECRETS_JSON` maps direct-radio device IDs to secrets.
- NATS Leaf Node or equivalent transport is mutually authenticated.
- Device secrets are never printed in logs.

## Packet Validation Failures

| Error class | Operator response |
|---|---|
| Invalid payload length | Check firmware version and payload encoder. |
| Unsupported message type | Quarantine device or update protocol compatibility plan. |
| Coordinates out of range | Treat as device fault or spoofing attempt. |
| Battery outside range | Check firmware and sensor calibration. |
| Unregistered radio device | Reject and investigate device inventory. |
| Invalid signature | Treat as possible spoofing or stale secret. |

## Replay and Duplicate Handling

AEGIS event and correlation IDs are derived from packet fingerprints. Broker retries should be dropped by Redis worker deduplication.

If duplicates appear in the dashboard:

1. Check whether packet payload and sequence are identical.
2. Check Redis `processed:{event_id}` behavior.
3. Check NATS redelivery and worker acknowledgements.
4. Check `worker_duplicates_dropped_total`.
5. If uncontrolled replay is confirmed during pilot, suspend pilot and declare SEV-0 or SEV-1 depending on dispatch impact.

## Hardware Ingress Failure

1. Confirm NATS connectivity from the gateway.
2. Confirm LoRaWAN network-server webhook authentication.
3. Confirm direct-radio device ID exists in `AEGIS_DEVICE_SECRETS_JSON`.
4. Confirm the packet decodes to protocol v1: type `0x01`, float32 latitude, float32 longitude, battery percentage.
5. Confirm the emitted event uses subject `incident.created`.
6. Confirm worker and dashboard receive the event.

## Safety Boundary

Do not patch AEGIS to call dispatch endpoints. The only allowed hardware output in Phase 1.5 is normalized incident ingestion.

