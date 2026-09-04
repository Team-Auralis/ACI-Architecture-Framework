# Security Testing Protocols

Standard penetration testing is insufficient for ORION. 

## Automated Adversarial Checks
1.  **Policy Fuzzing:** OPA Rego policies are constantly fuzzed. Automated scripts generate millions of malformed JWTs and edge-case permission requests to ensure the system strictly defaults to `DENY`.
2.  **Prompt Injection Suite:** The SENTIENCE AI agents are subjected to thousands of known prompt-injection strings embedded in simulated civilian SOS payloads to verify that the agent's output does not bypass Bounded Autonomy.
3.  **Dependency Auditing:** Every container image is scanned for CVEs before deployment. If a critical vulnerability is found in a base image, the deployment is blocked via GitOps hooks.
