# ACI System Architecture

## Target Architecture

```mermaid
graph TD
    %% Styling
    classDef ai fill:#2d1b4e,stroke:#9d72ff,stroke-width:2px,color:#fff
    classDef memory fill:#113247,stroke:#2b8abb,stroke-width:2px,color:#fff
    classDef agents fill:#1a4138,stroke:#3bb38d,stroke-width:2px,color:#fff
    classDef physical fill:#4a2b10,stroke:#d98436,stroke-width:2px,color:#fff
    classDef gov fill:#4a1515,stroke:#d93d3d,stroke-width:2px,color:#fff

    sublayer1[("🧠 AURA Intelligence Core")]:::ai
    
    subgraph CognitiveLayer [Cognitive & Memory Layer]
        mem[(Institutional Memory)]:::memory
        world((OMNIS World Model)):::memory
        reason[Reasoning Engine]:::memory
    end
    
    sublayer1 --> CognitiveLayer

    subgraph NEXUS [NEXUS Agent Fabric]
        direction LR
        sci[🧬 Science Agents]:::agents
        eng[⚙️ Engineering Agents]:::agents
        med[🏥 Medical Agents]:::agents
        econ[📈 Economics Agents]:::agents
        infra[🏗️ Infrastructure Agents]:::agents
    end
    
    CognitiveLayer --> NEXUS
    
    forge{{FORGE Science Engine}}:::ai
    ascend>ASCEND Long-Horizon Planner]:::ai
    sim((Mirror Digital Twin Simulation)):::memory
    
    NEXUS --> forge
    forge --> ascend
    ascend --> sim
    
    veil{VEIL Security & Governance}:::gov
    sim --> veil
    
    human([Human / Authorized Operators]):::agents
    veil --> human
    
    action[⚡ Real-World Action / Execution]:::physical
    human --> action
    
    telemetry[/📡 Observation & Edge Telemetry/]:::physical
    action --> telemetry
    
    telemetry -. "Continuous Learning Loop" .-> world
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
