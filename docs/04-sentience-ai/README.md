# 05 AI Orchestration Layer (SENTIENCE)

## 1. Purpose
SENTIENCE defines the artificial intelligence, autonomous agents, and machine learning components of ORION. It acts as the cognitive layer that processes the massive influx of data to assist human operators in making split-second emergency decisions.

## 2. Scope
Included: AI agents, federated learning, decision-support algorithms, LLM integrations, and AI safety mechanisms.
Excluded: Autonomous physical control systems (e.g., weapons, self-driving vehicle control).

## 3. Major Components
*   **The Agent Pool:** Specialized AI workers subscribing to the NATS event mesh.
*   **Decision Support Engine:** The UI layer providing actionable intelligence to human operators.
*   **Federated Learning Aggregator:** The engine syncing edge-trained models.

## 4. Architecture
AI components in ORION operate strictly as **Asynchronous Workers**. They subscribe to NATS events, process data, and publish "Proposals" back to the mesh. They do not have synchronous control over the core API.

## 5. Responsibilities
To reduce the cognitive load on human operators by triaging data, predicting cascading failures, and drafting response plans.

## 6. Relationships with other ORION parts
SENTIENCE relies heavily on **OMNIS** (Data Fabric) for telemetry. Its physical execution power is strictly contained by **VEIL** (Security & Zero Trust), which enforces the "Bounded Autonomy" principle.

## 7. Future Roadmap
Swarm Intelligence, where edge nodes negotiate routing and resource allocation dynamically using localized, lightweight AI models.

## 8. Trade-offs
To guarantee safety, we trade "fully autonomous speed" for "human-in-the-loop safety." An AI might detect a fire in 1 millisecond, but it must wait for human approval to dispatch a drone.

## 9. Risks
AI Hallucinations, Prompt Injection attacks, and Data Poisoning from compromised edge nodes.

## 10. Research Questions
How to maintain high-quality LLM reasoning capabilities on edge hardware with constrained VRAM and thermal limits?

## 11. Security Considerations
AI models are treated as **Untrusted External Actors**. Their outputs are never executed blindly; they are mathematically or logically verified by an independent deterministic engine (OPA).

## 12. Current Status
**Phase 0:** Agent architecture and Bounded Autonomy principles are documented.
