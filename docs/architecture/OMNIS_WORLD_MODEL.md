# OMNIS World Model

OMNIS is the Civilization World Model. Its purpose is to maintain a structured, continuously updateable representation of civilization and its environment. 

It is NOT just a giant database. It represents:

- People, Organizations, Institutions, Cities
- Infrastructure, Energy, Water, Food, Transportation, Healthcare
- Economics, Technology, Science, Environment, Resources
- Communications, Space Infrastructure, Emergencies

## Architectural Support
OMNIS supports:
- **Entities**: Nodes in the civilization graph.
- **Relationships**: Edges connecting entities.
- **Temporal State**: Historical, current, and projected future states.
- **Uncertainty**: Confidence scores for data points.
- **Provenance**: Lineage of every data point (which agent/sensor provided it).
- **Causal Relationships**: Understanding that A affects B.
- **Events & Observations**: Telemetry and real-world occurrences.
- **Predictions & Dependencies**: Cascading effects.

### Example Causal Chain
`DROUGHT → WATER AVAILABILITY → AGRICULTURE → FOOD SUPPLY → PRICES → MIGRATION → ENERGY DEMAND → INFRASTRUCTURE LOAD`
