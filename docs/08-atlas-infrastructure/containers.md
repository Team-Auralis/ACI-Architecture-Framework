# Containerization

Everything in ORION is a container.

## Immutable Infrastructure
No software is installed directly on the host OS of an edge node or cloud server. There are no `apt-get install` scripts running in production.

*   Every service (API, Worker, AI Agent) is packaged as an OCI-compliant container image.
*   Images are built deterministically in CI/CD pipelines.
*   Images are cryptographically signed before being pushed to the registry. Edge nodes use OPA to verify the signature before spinning up a container, preventing supply-chain attacks.
