# Encryption Standards

## Data in Transit
*   100% of network traffic is encrypted via TLS 1.3.
*   Civilian mesh payloads (BLE/Wi-Fi Direct) are encrypted with the public key of the regional ORION gateway before they ever leave the civilian's phone. Relay nodes cannot decrypt them.

## Data at Rest
*   PostgreSQL databases utilize AES-256 transparent data encryption (TDE) at the block storage level.
*   **Edge Security Enclaves:** Responder vehicles carry physical servers. If a vehicle is overrun or captured, the physical server is at risk. ORION edge nodes mandate hardware roots of trust (TPM 2.0). If the server case is opened or the boot sequence is tampered with, the TPM refuses to release the decryption keys, bricking the local database.
