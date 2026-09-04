# Open Policy Agent (OPA)

The brain of the VEIL security layer.

## Why OPA?
If we hardcode authorization into the Python API (`if user.role == "admin"`), the security rules become scattered across 50 different microservices in 3 different programming languages.

OPA centralizes this. It runs as a high-performance sidecar next to every API and NATS Worker.

## Rego (The Policy Language)
Policies are written in Rego, a declarative language.
This allows security engineers to write rules like:
*   "Allow dispatch IF role is Operator AND incident is in their assigned sector."
*   "Deny ALL actions if the user's AI-flag is set to True, UNLESS the action is /v1/propose."

When the rules change, we update the Rego files. We do not need to recompile or redeploy the Python API. The policy firewall is completely deterministic.
