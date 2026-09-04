# Civilian Privacy & Zero-Knowledge

During emergencies, vast amounts of sensitive data (medical status, exact location) are generated. HAVEN adheres to strict privacy laws to prevent surveillance or data exploitation.

## 1. End-to-End Encryption in the Mesh
When an offline SOS is bounced between civilian phones (store-and-carry), the intermediate relay phones **cannot read** the payload. The payload is encrypted with the public key of the regional ORION dispatch server. Relays only see routing headers.

## 2. Location Obfuscation
Unless an active SOS is triggered, civilian devices do not broadcast their exact GPS coordinates. Background mesh routing relies entirely on relative proximity (BLE signal strength) rather than absolute coordinates.

## 3. Ephemeral State
Once an incident is resolved and the audit log is archived, PII (Personally Identifiable Information) associated with the civilian's identity token is scrubbed from the active PostgreSQL state to minimize the blast radius of any future data breach.
