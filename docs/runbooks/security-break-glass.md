# Security and Break-Glass Runbook

## Purpose

Respond to identity, policy, secret, PII, and emergency override issues without bypassing the human-in-the-loop safety model.

## OPA Failure

Symptoms:

- API returns `503` with policy firewall unavailable.
- Redis key `circuit_open:OPA` is set.
- Dispatch approval or dashboard access fails despite valid operator auth.

Actions:

1. Treat OPA outage as SEV-1.
2. Do not disable authorization in code.
3. Confirm Redis circuit state and OPA health.
4. Restart or roll back OPA policy only through change control.
5. Use break-glass only for a documented emergency action that cannot wait.

## Keycloak Failure

Symptoms:

- JWT validation fails.
- JWKS fetch errors appear.
- Redis key `circuit_open:KEYCLOAK` is set and stale JWKS is used.

Actions:

1. Check Keycloak health and JWKS endpoint.
2. Confirm `JWT_ISSUER`, `JWT_AUDIENCE`, and `KEYCLOAK_JWKS_URL`.
3. If auth is degraded during a pilot, consider pilot suspension.
4. Do not create ad hoc local auth bypasses.

## Break-Glass

Endpoint: `POST /v1/auth/break-glass`

Rules:

- Requires authenticated user and a detailed reason of at least 20 characters.
- Issues a short-lived override token.
- Writes `BREAK_GLASS_ACTIVATED` to CHRONOS.
- Must be reviewed after incident closure.

Use break-glass only when delay would create greater public-safety risk than the temporary policy bypass. It is not a workaround for routine OPA or Keycloak maintenance.

## PII Leakage

If unmasked email, phone number, SSN, medical note, or other sensitive civilian data is found in persisted incident messages:

1. Declare SEV-0.
2. Suspend pilot if active.
3. Preserve evidence and identify affected incident IDs.
4. Stop further export or analytics on affected data.
5. Verify `apps/api/security.py` masking behavior.
6. Patch, test, and redeploy.
7. Follow partner-agency notification and retention rules.

## Secret Exposure

If a secret appears in code, logs, dashboard, CHRONOS, or docs:

1. Revoke or rotate the secret.
2. Identify every system that used it.
3. Scrub non-audit copies when allowed.
4. Keep audit evidence immutable.
5. Open a follow-up to move the secret class into the production secret manager if it is not already there.

