# Human-in-the-Loop (HITL)

HITL is not a feature in ORION; it is an architectural mandate.

## UX Principles for AI
1.  **Confidence Scoring:** Every AI proposal must include a confidence score (e.g., 92% confidence). The UI will flag low-confidence proposals with warning colors, forcing the human to scrutinize them closer.
2.  **Explainability:** An operator must be able to click "Why?" on any AI proposal. The system must surface the exact telemetry, SOS signals, or documents that led to the conclusion.
3.  **Override by Default:** The human operator always has the final physical "button." The system cannot bypass the human UI for critical physical actions.
4.  **Auditability:** When a human approves an AI proposal, the database logs both the AI's proposal ID and the Human's Identity Token. If an error occurs, the exact chain of reasoning and approval is permanently recorded in PostgreSQL.
