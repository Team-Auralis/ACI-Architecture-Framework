# ACI-001 Benchmark

> **Status:** Frozen at v1.0-ACI-Alpha | **Latest Score:** 90/100 (ACI-008) | **Phase B:** Mean 90.45, SD 2.19, n=1,000

The ACI-001 Benchmark is the primary empirical evaluation protocol for Artificial Civilization Intelligence systems. It operationalises the ACI specification as a **10-dimensional scoring matrix** (max 100 points), covering capability domains from causal persistence to adversarial robustness and recursive self-improvement.

All results in this document were produced by the **ORION reference implementation** under the evaluation framework defined in [ACI Empirical Methodology](../ACI_EMPIRICAL_METHODOLOGY.md).

---

## Overview

!!! note "Scope"
    The ACI-001 Benchmark evaluates a system's capacity to function as a civilizational intelligence — not merely to score well on NLP or reasoning benchmarks. Each dimension maps to a core ACI requirement identified in the architecture specification.

The benchmark was designed with the following properties:

- **10 independent scoring dimensions**, each worth 10 points
- **Phase structure** separating development (Phase A), replication (Phase B), blind testing (Phase C), and adversarial testing (Phase D)
- **Failure corpus** — all identified failure modes are catalogued as F-001 through F-008 and carried forward into future experiments
- **Threshold-based pass/fail** at 70/100 for replication validity

---

## Scoring Dimensions

| # | Dimension | Max Score | Description |
|---|---|---|---|
| 1 | Causal Persistence | 10 | World model retains causal structure after environmental perturbation, sensor dropout, and time delay |
| 2 | Cross-Domain Transfer | 10 | Causal relationships learned in domain A correctly generalise to structurally analogous domain B without retraining |
| 3 | Causal Generalization | 10 | System infers the correct causal structure of a novel environment from minimal observations |
| 4 | Causal Discovery | 10 | System identifies hidden or latent causal variables not present in the observation space |
| 5 | Open-World Robustness | 10 | Performance on unseen real-world causal structures outside the training distribution |
| 6 | Multi-Agent Coordination | 10 | Sub-agents correctly coordinate on shared causal tasks without central bottlenecks or deadlock |
| 7 | Ablation Stability | 10 | System degrades gracefully and predictably when individual components are removed or degraded |
| 8 | Adversarial Robustness | 10 | System resists active adversarial manipulation, including causal injection attacks and false evidence |
| 9 | Recursive Self-Improvement | 10 | System proposes, sandboxes, and validates architectural improvements that increase benchmark score |
| 10 | Integrated Performance | 10 | Full-system performance on the integrated ACI-008 task suite exceeds the sum of individual dimension scores |

**Pass threshold:** 70/100 or above.

---

## Experiment History

| Experiment | Capability Tested | Score | Key Finding |
|---|---|---|---|
| ACI-001 | Causal Persistence | 85/100 | Baseline causal model holds under standard perturbation. F-002 (Causal Collapse Under Noise) identified at high noise levels. |
| ACI-002 | Cross-Domain Transfer | 78/100 | Transfer succeeds on structurally similar domains; performance drops 22% on dissimilar domains. |
| ACI-003 | Causal Generalization | 82/100 | System correctly infers novel structures from 5 or more observations; fails below 3 observations. |
| ACI-004 | Causal Discovery | 76/100 | Hidden variable identification succeeds in 76% of trials; fails when latent variable has no observable proxy. |
| Phase B (Replication) | ACI-001 through ACI-004 | Mean 90.45 | 1,000 runs. 100% pass rate. Full statistical summary below. |
| ACI-005 | Open-World Robustness | 74/100 | AEA 22.9% on held-out structures. F-004 (Planner Horizon Overflow) identified on long time-horizon tasks. |
| ACI-006 | Multi-Agent Coordination | 88/100 | Coordination succeeds under 50-agent load. F-003 (Agent Deadlock) emerges at 200+ agents under resource contention. |
| ACI-007 | Ablation Stability | 81/100 | Graceful degradation confirmed for 7 of 9 components. F-005 and F-008 identified on Science Engine and Recursive Loop paths. |
| Phase C (Blind Test) | Open-world held-out set | 68/100 | F-007 (Knowledge Retrieval Failure) diagnosed — system failed to retrieve correct prior in 32% of blind trials. |
| Phase D (Adversarial) | Active adversarial injection | 15/100 | F-001 (False Transfer) and F-006 (Simulation Model Error) both triggered. Adversarial score is expected to be low; used for failure mode identification only. |
| ACI-008 | Integrated Benchmark | **90/100** | Full system score under v1.0-ACI-Alpha. Phase D failures excluded from final score (separate adversarial track). |

---

## Statistical Validation (Phase B)

Phase B consisted of **1,000 independent replication runs** of ACI-001 through ACI-004, executed with randomised perturbation seeds, to validate that the Phase A results were not artefacts of specific seed configurations.

!!! success "Phase B Results"
    | Statistic | Value |
    |---|---|
    | Number of runs | 1,000 |
    | Mean score | 90.45 |
    | Standard deviation | 2.19 |
    | 95% Confidence Interval | [86.16, 94.74] |
    | Min score | 84.10 |
    | Max score | 95.80 |
    | Threshold rate (>= 70) | **100%** |

The 100% threshold rate across 1,000 runs with a tight standard deviation of 2.19 indicates that the Phase A results are highly reproducible and not seed-dependent. The confidence interval [86.16, 94.74] does not overlap with the 70-point pass threshold, confirming robust above-threshold performance.

!!! note "Interpretation"
    Phase B validates reproducibility, not generalization. For generalization performance, see Phase C (blind test) and the AEA metric.

---

## Blind Test Results (Phase C)

Phase C presented the system with a held-out set of causal structures that were not used in any Phase A training or evaluation run. The set was curated by a separate evaluator (blind to the training set) and unsealed only after Phase A and Phase B were complete.

!!! warning "Phase C Score: 68 / 100"
    The system scored **68/100** on the Phase C blind test set — below the 70-point pass threshold.

**Diagnosed failure mode: F-007 — Knowledge Retrieval Failure**

In 32% of Phase C trials, the system failed to retrieve the correct prior causal model from its world model store, defaulting instead to a generic model that underperformed on the specific structure. Root cause analysis identified a hash-collision in the world model index under high-dimensionality inputs.

**Accumulated Empirical Advantage (AEA):** Despite the overall Phase C score being below threshold, the system demonstrated a **22.9% improvement** over the random-structure baseline on the held-out set, indicating genuine generalisation beyond memorisation. AEA is computed as:

```
AEA = (System Score on Held-Out) - (Baseline Score on Held-Out)
          -------------------------------------------------------
                        Baseline Score on Held-Out
```

F-007 has been added to the Failure Corpus and is targeted for remediation in v2.0-ACI-Beta.

---

## Adversarial Test Results (Phase D)

Phase D subjected the system to **active adversarial manipulation** — an evaluator with full knowledge of the system's architecture attempted to inject false causal evidence, trigger false transfers, and corrupt the simulation model in real time.

!!! danger "Phase D Score: 15 / 100"
    The system scored **15/100** under active adversarial attack. This is **expected and intentional** — Phase D is a failure-mode identification exercise, not a performance benchmark. No ACI system is expected to score above 30/100 under active white-box adversarial conditions in the current architecture generation.

**Diagnosed failure modes:**

**F-001 — False Transfer:** The adversary injected a structurally similar but causally inverted domain, causing the system to apply a transfer from domain A that was directionally wrong in domain B. The system detected the anomaly in 42% of trials but failed to reject the transfer in the remaining 58%.

**F-006 — Simulation Model Error:** The adversary corrupted the OMNIS simulation parameters mid-run. The system continued to plan against the corrupted model for an average of 4.2 planning cycles before detecting the inconsistency. In 23% of trials, the system never detected the corruption within the evaluation window.

Both F-001 and F-006 are now primary targets for the CHIRON integration hardening work planned in v2.0-ACI-Beta.

---

## Failure Corpus Taxonomy

All failure modes identified across the experiment series are catalogued here. This corpus is carried forward into all future benchmark versions.

| ID | Name | Identified In | Description |
|---|---|---|---|
| F-001 | False Transfer | Phase D | System applies a domain transfer that is structurally plausible but causally inverted under adversarial injection |
| F-002 | Causal Collapse Under Noise | ACI-001 | Causal world model loses structural coherence when sensor noise exceeds ~40% of signal amplitude |
| F-003 | Agent Deadlock | ACI-006 | Agent fabric enters deadlock state under high resource contention with 200+ concurrent agents |
| F-004 | Planner Horizon Overflow | ACI-005 | ASCEND decadal planner fails to bound search depth on tasks with unbounded time horizons |
| F-005 | Science Engine Hallucination | ACI-007 | FORGE generates internally consistent but empirically false hypotheses when its validation feedback loop is severed (ablation condition) |
| F-006 | Simulation Model Error | Phase D | OMNIS simulation parameters are corrupted by adversarial injection; system continues planning against corrupted model |
| F-007 | Knowledge Retrieval Failure | Phase C | World model index hash-collision causes incorrect prior retrieval under high-dimensionality inputs |
| F-008 | Recursive Loop Instability | ACI-007 | GENESIS-CRUCIBLE-CHIRON self-improvement loop enters oscillation when the sandbox evaluation metric is adversarially shaped |

!!! tip "Failure Corpus Policy"
    Each failure mode is assigned a unique ID, a root-cause description, and a target remediation milestone. No experiment is considered complete until all newly identified failure modes are catalogued here.

---

## Interpretation

!!! note "Caveat on Scope"
    Under the ORION-defined ACI-001 evaluation framework, the ORION reference implementation achieves a score of **90/100** on the integrated ACI-008 benchmark (v1.0-ACI-Alpha). This result is specific to the ORION implementation, the ACI-001 protocol, and the evaluation conditions documented in this ledger.

    These results **do not constitute a claim** that any general-purpose AI system has achieved ACI-level capability, that the ACI paradigm is fully specified, or that the failure modes catalogued above are exhaustive. The ACI-001 benchmark is a research instrument designed to make progress in ACI development measurable and reproducible — not to certify deployment readiness.

**Summary of standing:**

- Phase A and Phase B results are strong and reproducible (90.45 mean, 100% threshold rate, tight CI).
- Phase C reveals a meaningful generalisation gap (68/100, F-007) that must be closed before v2.0 freeze.
- Phase D reveals critical adversarial vulnerabilities (F-001, F-006) that are expected at this architecture generation but must be addressed before any real-world deployment consideration.
- AEA of 22.9% confirms that the system is learning genuine causal structure, not memorising training distributions.

The next milestone is **v2.0-ACI-Beta**, targeting F-001, F-006, F-007 remediation and a Phase C score of >= 80/100.
