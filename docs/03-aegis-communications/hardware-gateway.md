# AEGIS Hardware Gateway

P1.5-014 normalizes two physical ingress paths into the existing `incident.created` event contract: a The Things Stack-compatible LoRaWAN uplink webhook and a signed direct-radio packet. LoRaWAN traffic relies on network-server authentication; direct radio additionally requires a per-device HMAC-SHA256 over `DEVICE_ID:SEQUENCE:PAYLOAD_HEX`, with secrets supplied in `AEGIS_DEVICE_SECRETS_JSON`.

Protocol v1 contains SOS type `0x01`, big-endian float32 latitude/longitude, and battery percentage. Invalid lengths, message types, device IDs, coordinates, battery values, signatures, and unregistered devices are rejected before the mesh.

The gateway only emits `incident.created`; it cannot dispatch assets. Existing worker triage, recommendations, and operator approval remain mandatory. Packet fingerprints form deterministic event/correlation IDs so Redis worker deduplication drops broker retries. Deploy behind a mutually authenticated NATS Leaf Node with durable JetStream routing, and never log device secrets.
