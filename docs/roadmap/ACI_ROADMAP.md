# ACI Roadmap

## PHASE 1: Existing ORION infrastructure
- **Objective**: Stabilize current Emergency Response capabilities.
- **Required Components**: Keycloak, OPA, TITAN, PHOENIX.
- **Dependencies**: None.
- **Tests**: Core integration tests.
- **Measurable Criteria**: System runs stably.
- **Resource**: Solo developer.

## PHASE 2: AURA intelligence core
- **Objective**: Implement multimodal local reasoning.
- **Required Components**: AURA Orchestration, AURA Memory.
- **Dependencies**: Phase 1.
- **Measurable Criteria**: Passes baseline reasoning eval.
- **Resource**: Solo developer + Local GPU.

## PHASE 3: OMNIS world model
- **Objective**: Graph-based entity representation.
- **Required Components**: Graph DB, Causal schemas.
- **Dependencies**: Phase 2.
- **Measurable Criteria**: Can represent drought causal chain.
- **Resource**: Solo developer.

## PHASE 4: NEXUS multi-agent fabric
- **Objective**: Multi-agent coordination.
- **Required Components**: Agent Registry, Dispute Resolution.
- **Dependencies**: Phase 3.
- **Measurable Criteria**: 3 agents solve a cross-domain problem.
- **Resource**: Solo developer.

## PHASE 5: FORGE scientific engine
- **Objective**: Automated hypothesis testing.
- **Required Components**: Simulation sandboxes.
- **Dependencies**: Phase 4.
- **Measurable Criteria**: Generates and tests 1 valid hypothesis.
- **Resource**: Solo developer.

## PHASE 6: ASCEND long-horizon planning
- **Objective**: Multi-year planning.
- **Required Components**: Objective solver, Error tracking.
- **Dependencies**: Phase 4.
- **Measurable Criteria**: Generates 10-year plan, adapts to 1 simulated disruption.
- **Resource**: Solo developer.

## PHASE 7: Civilization simulation
- **Objective**: Synthetic civilization (10M population).
- **Required Components**: MIRROR extension.
- **Dependencies**: Phase 3, Phase 6.
- **Measurable Criteria**: Runs 20 simulated years stably.
- **Resource**: Team / Cloud Compute.

## PHASE 8: Controlled real-world interfaces
- **Objective**: Safe physical actuation.
- **Required Components**: VEIL Governance, IoT bindings.
- **Dependencies**: Phase 1, Phase 7.
- **Measurable Criteria**: Passes strict security audit for actuation.
- **Resource**: Team.

## PHASE 9: ACI benchmark
- **Objective**: Formal testing against ACI-001.
- **Required Components**: Evaluation harness.
- **Dependencies**: Phase 7.
- **Measurable Criteria**: Validated score > 50/100.
- **Resource**: Solo developer / Team.

## PHASE 10: Independent evaluation
- **Objective**: Third-party verification.
- **Required Components**: Documentation, reproducible environment.
- **Dependencies**: Phase 9.
- **Measurable Criteria**: External confirmation of ACI claims.
- **Resource**: External Auditors.
