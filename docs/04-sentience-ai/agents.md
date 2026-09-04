# Autonomous Agents

AI in ORION is not a single, massive monolithic brain. It is a pool of highly specialized, decoupled agents operating as NATS Workers.

## The Agent Types

1.  **Triage Agent (LLM/NLP):** Subscribes to incoming civilian SOS text. Extracts severity, medical requirements, and structural damage info, converting unstructured text to structured JSON.
2.  **Routing Agent (Graph/Heuristic ML):** Analyzes the current health of the NATS event mesh and terrestrial infrastructure to predict network bottlenecks and suggest optimal data routing paths.
3.  **Anomaly Agent (Time-Series ML):** Ingests raw telemetry from OMNIS (e.g., bridge stress sensors, power grid loads) and flags deviations from the baseline.

## Agent Architecture
Every agent is a stateless microservice.
*   It subscribes to a specific NATS subject (e.g., `telemetry.raw.*`).
*   It processes the payload.
*   It publishes its conclusion to a new subject (e.g., `telemetry.anomaly.detected`).
