# Authentication (AuthN)

Proving *who* you are.

## 1. Machine-to-Machine (mTLS)
All internal traffic between the FastAPI Gateway, the NATS broker, and the PostgreSQL database is secured via Mutual TLS. 
*   Standard TLS (like HTTPS) only proves the server to the client.
*   mTLS forces the client to present a valid certificate to the server as well. 
*   If a rogue script tries to connect to Postgres, it fails the mTLS handshake instantly because it lacks a valid SPIRE-issued certificate.

## 2. User-to-Machine (JWT & Hardware Tokens)
When an operator logs into the Next.js Dashboard:
1.  They authenticate against Keycloak.
2.  Command-level operators are mandated to use FIDO2 hardware keys (e.g., YubiKey) to prevent phishing.
3.  Keycloak issues a short-lived JWT.
4.  Every API request attaches this JWT in the `Authorization: Bearer` header.
