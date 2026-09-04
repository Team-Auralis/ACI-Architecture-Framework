# ACI System Architecture

## Target Architecture

```text
                    ARTIFICIAL CIVILIZATION INTELLIGENCE
                                │
                                ▼
                         AURA INTELLIGENCE
                                │
              ┌─────────────────┼─────────────────┐
              │                 │                 │
              ▼                 ▼                 ▼
           MEMORY          WORLD MODEL       REASONING
              │                 │                 │
              └─────────────────┼─────────────────┘
                                ▼
                         NEXUS AGENT FABRIC
                                │
          ┌─────────────┬───────┼───────┬─────────────┐
          ▼             ▼       ▼       ▼             ▼
       Science      Engineering Medicine Economics Infrastructure
          │             │       │       │             │
          └─────────────┴───────┼───────┴─────────────┘
                                ▼
                         FORGE SCIENCE ENGINE
                                │
                                ▼
                         ASCEND PLANNER
                                │
                                ▼
                         SIMULATION LAYER
                                │
                                ▼
                         GOVERNANCE LAYER
                                │
                                ▼
                       HUMAN / AUTHORIZED AGENT
                                │
                                ▼
                         REAL-WORLD ACTION
                                │
                                ▼
                         OBSERVATION / TELEMETRY
                                │
                                ▼
                         WORLD MODEL UPDATE
                                │
                                └───────────────► CONTINUOUS LOOP
```

## Legacy to ACI Mapping
Existing ORION components map into the new architecture as follows:
- **TITAN CLOUD** -> OMNIS Backend / Data Lake
- **MIRROR TWIN** -> SIMULATION LAYER
- **PHOENIX EDGE** -> OBSERVATION / TELEMETRY Edge nodes
- **ATLAS GEO** -> OMNIS Spatial Engine
- **SENTIENCE** -> Legacy term, deprecated in favor of AURA
- **AEGIS COMMS** -> NEXUS Communication Bus
- **SHIELD IDENTITY** -> GOVERNANCE LAYER (Authentication)
- **FORGE CYBER** -> FORGE SCIENCE ENGINE (Generalized)
- **CHRONOS AUDIT** -> MEMORY / INSTITUTIONAL KNOWLEDGE
- **ASCEND** -> ASCEND PLANNER
