# ACI Architecture Framework

[![GitHub Pages](https://img.shields.io/badge/docs-GitHub%20Pages-blue?logo=github)](https://team-auralis.github.io/ACI-Architecture-Framework/)
[![License](https://img.shields.io/badge/license-CC%20BY--NC--ND%204.0-lightgrey)](LICENSE)
[![Version](https://img.shields.io/badge/version-v1.0--ACI--Alpha-indigo)](https://github.com/Team-Auralis/ACI-Architecture-Framework/releases)

The official specification, benchmark, and research ledger for **Artificial Civilization Intelligence (ACI)** — a post-AGI architectural paradigm for planetary-scale governance, authored by **Raja Dharma Tej Maddala** under **Team Auralis**.

**Documentation site:** [https://team-auralis.github.io/ACI-Architecture-Framework/](https://team-auralis.github.io/ACI-Architecture-Framework/)

---

## What is ACI?

Artificial Civilization Intelligence is not a smarter chatbot or an AGI with more compute. It is a new class of intelligence designed to:

- Maintain causal world models of real-world infrastructure under sensor noise and deception
- Coordinate thousands of heterogeneous sub-agents without central bottlenecks
- Run multi-decade scientific programs and self-validate their hypotheses
- Detect and survive adversarial manipulation, including attacks on its own architecture
- Recursively redesign its own components within sandboxed environments, then deploy validated upgrades into the live system

Where AGI targets human-level reasoning and ASI targets maximal individual cognition, **ACI targets civilizational-scale institutional function**: the capacity to run, maintain, and improve entire societies under adversarial, resource-constrained, and catastrophically uncertain conditions.

---

## Empirical Results (v1.0-ACI-Alpha)

| Metric | Value |
|---|---|
| ACI-008 Integrated Benchmark Score | **90 / 100** |
| Phase B Replication Mean (n=1,000) | **90.45 +/- 2.19** |
| Phase B 95% Confidence Interval | **[86.16, 94.74]** |
| Phase B Threshold Rate (>= 70/100) | **100%** |
| Accumulated Empirical Advantage (AEA) | **22.9%** |
| Phase C Blind Test Score | 68 / 100 (F-007 identified) |
| Phase D Adversarial Score | 15 / 100 (F-001, F-006 identified) |

All experiments were run under the ORION-defined ACI-001 evaluation framework. Results represent performance of the ORION reference implementation, not a claim about ACI as a general class of systems.

---

## Architecture

```
Real World Infrastructure
        |  (Telemetry)
        v
OMNIS: Causal World Model
        |
        v
NEXUS: Agent Fabric  <-->  AURA: Reasoning Core (Dispute Resolution)
        |
        v
ASCEND: Decadal Planner
        |  (Scientific Validation)
        v
FORGE: Science Engine
        |  (Action)
        v
Real World Infrastructure

--- Recursive Self-Improvement Loop (Sandboxed) ---
GENESIS: Architecture Synthesis
        |  (Proposes New OS)
        v
CRUCIBLE: Sandbox
        |  (Hot-Swaps Code)
        v
CHIRON: Integration
        |  (Upgrades)
        v
NEXUS
```

---

## Repository Structure

```
docs/
  index.md                        Homepage
  ACI_DEFINITION.md               Formal definition of ACI
  ACI_VS_AGI_VS_ASI.md            Comparison table
  ACI_VS_OCI_MASTER_GUIDE.md      ACI vs Organic Civilization Intelligence
  ACI_EMPIRICAL_METHODOLOGY.md    Experimental design principles
  BEYOND_ASI_THE_ACI_PARADIGM.md  Why ACI is a distinct paradigm
  ACI_ORIGIN_AND_PROVENANCE.md    History and authorship record
  architecture/                   Technical subsystem specifications
  research/                       Benchmark protocols and results
  00-core-vision/                 Core vision documents
  01-nexus-architecture/          NEXUS agent fabric
  02-haven-civilian-platform/     HAVEN civilian platform
  03-aegis-communications/        AEGIS communications layer
  04-sentience-ai/                SENTIENCE AI subsystem
  05-veil-security/               VEIL security layer
  06-phoenix-resilience/          PHOENIX resilience framework
  07-mirror-digital-twin/         MIRROR digital twin
  08-atlas-infrastructure/        ATLAS infrastructure
  09-omnis-data/                  OMNIS data layer
  10-forge-research/              FORGE research engine
  11-ascend-expansion/            ASCEND expansion planner
  governance/                     Governance framework
  roadmap/                        Development roadmap
```

---

## Benchmark Summary (ACI-001)

The ACI-001 Benchmark scores systems across 10 dimensions (10 points each, max 100):

1. Causal Persistence — Does the world model persist under perturbation?
2. Cross-Domain Transfer — Does causal knowledge generalise to new domains?
3. Causal Generalization — Does the system infer novel causal structures?
4. Causal Discovery — Can the system discover hidden causal variables?
5. Open-World Robustness — Does performance hold on unseen real-world structures?
6. Multi-Agent Coordination — Can sub-agents coordinate without central bottlenecks?
7. Ablation Stability — Does performance degrade gracefully when components are removed?
8. Adversarial Robustness — Does the system resist active deception and injection attacks?
9. Recursive Self-Improvement — Can the system propose and validate architectural upgrades?
10. Integrated Performance — Does the full system exceed the sum of its parts?

---

## Failure Corpus

Identified failure modes catalogued during the experiment series:

| ID | Name | Identified In |
|---|---|---|
| F-001 | False Transfer | Phase D Adversarial |
| F-002 | Causal Collapse Under Noise | ACI-001 |
| F-003 | Agent Deadlock | ACI-006 |
| F-004 | Planner Horizon Overflow | ACI-005 |
| F-005 | Science Engine Hallucination | ACI-007 Ablation |
| F-006 | Simulation Model Error | Phase D Adversarial |
| F-007 | Knowledge Retrieval Failure | Phase C Blind Test |
| F-008 | Recursive Loop Instability | ACI-007 Ablation |

---

## Getting Started

```bash
# Clone the repository
git clone https://github.com/Team-Auralis/ACI-Architecture-Framework.git

# Install MkDocs Material
pip install mkdocs-material

# Serve locally
mkdocs serve

# Build static site
mkdocs build
```

---

## Contributing

This repository is maintained by **Raja Dharma Tej Maddala** and **Team Auralis**. The ACI paradigm is an active research programme. Contributions, critiques, and replications are welcome via GitHub Issues and Pull Requests.

---

## Legal Notice

Copyright (c) 2026 **Raja Dharma Tej Maddala**. Published under **Team Auralis**.

The ACI Architecture Framework, including all specifications, benchmark protocols, experiment results, subsystem designs, and the ACI paradigm itself, is the original intellectual work of Raja Dharma Tej Maddala. All rights reserved except as explicitly licensed.

This repository is published under the **Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0)** license unless otherwise stated in individual files.
