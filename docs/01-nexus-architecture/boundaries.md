# Architectural Boundaries

Strict decoupling is required to prevent systemic failure.

## 1. The Policy Boundary
The FastAPI application **must not** contain `if user.role == "admin"` logic. It must blindly pass the user identity and requested action to OPA. OPA holds all the rules. If OPA rules change, the API code does not.

## 2. The State Boundary
Workers and AI agents **must not** connect directly to the PostgreSQL database. If an AI agent wants to update an incident status, it must hit the FastAPI endpoint (subjecting it to OPA authorization) OR publish a specific NATS event that a trusted, privileged worker consumes.

## 3. The Transport Boundary
Workers **must not** care whether an event originated from a cellular phone in Tokyo or a LoRaWAN sensor in a forest. The Gateway normalizes all incoming traffic into a standard ORION Event JSON format before publishing to NATS.
