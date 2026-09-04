# Cloud Architecture

The Global Core of ORION.

## Multi-Region, Active-Active
The ORION Cloud is the ultimate aggregator. It receives telemetry and events from all global edge nodes.
To survive the loss of a major data center, the cloud architecture is strictly active-active across at least three geographic regions.

## Cloud Agnosticism
ORION avoids proprietary hyperscaler services (e.g., AWS SQS, GCP Pub/Sub) in its core critical path. 
Because ORION relies on open-source, containerized primitives (NATS, PostgreSQL, OPA), the entire global core can be lifted and shifted to a different cloud provider—or even an on-premise government data center—with minimal architectural refactoring.
