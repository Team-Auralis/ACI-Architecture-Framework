# FORGE: The Scientific Discovery & Hypothesis Engine

> **Authored by Shaurya Sanyal (Mr Fool) — Team Auralis, 2026**  
> *Definitive Engineering & Epistemic Specification for Autonomous Scientific Discovery.*

---

## 1. Executive Summary

True civilizational intelligence cannot merely extrapolate patterns from historical datasets. When novel crises emerge (e.g., unexpected pathogens, materials degradation under space radiation, or unprecedented climate feedback loops), the system must be capable of generating **novel scientific knowledge**.

**FORGE** is the **automated scientific hypothesis and causal discovery engine** of the ACI architecture. It operates an automated Popperian falsification loop: formulating causal hypotheses, designing discriminative experiments, validating them in the MIRROR digital twin simulation, and updating the global OMNIS causal world model with cryptographic provenance.

---

## 2. The 11-Stage Scientific Discovery Loop

```mermaid
flowchart TD
    OBS["1. OBSERVE<br/>(Telemetry & Anomaly Ingestion)"]
    Q["2. QUESTION<br/>(Identify Unexplained Variance)"]
    HYP["3. HYPOTHESIZE<br/>(Generate Causal Graph Hypotheses)"]
    SIM["4. SIMULATE<br/>(MIRROR Digital Twin Prototyping)"]
    EXP["5. EXPERIMENT DESIGN<br/>(Optimal Bayesian Interventions)"]
    HUMAN{"6. VEIL / HUMAN GATE<br/>(Physical Safety Approval)"}
    ACT["7. EXECUTE EXPERIMENT<br/>(Lab Robotics / Edge Actuation)"]
    RES["8. COLLECT RESULTS<br/>(Empirical Measurement)"]
    FAL["9. FALSIFY / VERIFY<br/>(Popperian Residual Elimination)"]
    UP["10. UPDATE OMNIS<br/>(Ratify Novel Causal Edges)"]
    NEXT["11. NEXT FRONTIER<br/>(Formulate Successor Hypotheses)"]

    OBS --> Q --> HYP --> SIM --> EXP --> HUMAN --> ACT --> RES --> FAL
    FAL -->|Hypothesis Rejected| HYP
    FAL -->|Hypothesis Verified| UP --> NEXT --> Q
```

---

## 3. Algorithmic Foundation: Active Causal Discovery

FORGE combines observational constraint search with continuous interventional optimization to discover true causal DAGs:

### 3.1 Constraint-Based Discovery (PC / FCI)
- Tests conditional independence relations $X \perp\!\!\!\perp Y \mid \mathbf{Z}$ across telemetry streams using kernel-based conditional independence tests.
- Reconstructs the **Markov Equivalence Class** (CPDAG) of the underlying physical system.

### 3.2 Continuous Optimization (NOTEARS / DCDI)
To resolve directionality among observationally equivalent graphs, FORGE solves a continuous constrained optimization problem:

$$\min_{W \in \mathbb{R}^{d \times d}} \mathcal{L}(W) \quad \text{subject to} \quad h(W) = \text{tr}\left(e^{W \odot W}\right) - d = 0$$

Where $h(W) = 0$ is the exact algebraic characterization of acyclicity (DAG constraint), enabling efficient gradient-based discovery of complex planetary-scale networks.

---

## 4. Bayesian Experimental Design & Discriminative Testing

When multiple competing hypotheses explain the observed data ($H_1, H_2, \dots, H_k$), FORGE does not guess. It computes the **Expected Information Gain (EIG)** to design an experiment $\xi^*$ that maximizes mutual information between the outcome $Y$ and the true hypothesis $H$:

$$\xi^* = \arg\max_{\xi} \mathbb{E}_{Y \mid \xi} \left[ D_{\text{KL}}\Big(P(H \mid Y, \xi) \parallel P(H)\Big) \right]$$

### 4.1 The Role of the MIRROR Digital Twin
- Before any physical experiment or real-world intervention is dispatched, it is run across $10^4$ stochastic rollouts inside the **MIRROR** simulation environment.
- If an experiment has non-zero probability of exceeding safety boundaries (e.g., thermal runaway, chemical contamination), it is rejected immediately by VEIL.

---

## 5. Epistemic Provenance & Integrity Standards

In accordance with the ACI Research Integrity Protocol:
1. **Zero Hallucination Tolerance**: Every proposed causal relationship $A \to B$ in OMNIS must link to an immutable Merkle cryptographic proof containing:
   - The originating observational sensor log;
   - The mathematical test statistic ($\text{p-value} < 10^{-6}$ or Bayes Factor $\ge 100$);
   - The digital signature of the human/laboratory executor that verified the experiment.
2. **Anti-Dogmatism Check**: Periodically re-tests historical causal axioms against recent observational residuals to prevent **Institutional Epistemic Lock-in**.

---

## 6. Empirical Program Synthesis & Tree Search: Generational FUTS (`Gen-FUTS`)

In empirical scientific software synthesis—from discovering numerical ODE integrators to modeling single-cell genomics and atmospheric dynamics—FORGE leverages **Generational Flat UCB Tree Search (`Gen-FUTS`)**, an evolution of Google DeepMind & Google Research's ERA architecture ([arXiv:2509.06503](https://arxiv.org/abs/2509.06503), Aygün et al., 2025).

Standard Flat UCB Tree Search suffers from **Softmax Inundation** and **Error Gravitation** as search depth increases, because execution stdout/stderr and tracebacks accumulate along branch lineages, diluting attention to fundamental physical conservation laws.

FORGE overcomes this by enforcing a 3-tier bounded context lifecycle:
1. **Gen-2 Tenured Invariants:** Physical conservation laws, energy drift bounds, interface contracts, and objective metrics are permanently pinned at the top of the prompt with zero eviction risk ($A_{i, \text{inv}} \ge 0.38$).
2. **Gen-1 Evaporative Working Hypotheses:** Lineage hypotheses are paged through the Adaptive Replacement Attention Cache (AWE); stagnant exploration branches evaporate.
3. **Gen-0 Ephemeral Execution Distillation:** Raw sandbox stderr and compiler outputs (500–2000 tokens) are intercepted and distilled into atomic $\mathcal{O}(1)$ execution signatures `(Status, Score, Delta, RootCause)` (<50 tokens).

In rigorous empirical benchmarks, `Gen-FUTS` achieved a **78.6% reduction in context window footprint**, reduced invariant violations from **12.0% to 4.0%**, and achieved a convergence score of **0.9950 vs. 0.8959** on chaotic Hamiltonian symplectic kernel synthesis.

> **Full Empirical Research Specification:** For the complete mathematical proof, benchmark telemetry, and reproducibility suite, see [Bounded-Context Tree Search: Integrating Google Research ERA with Generational Context](../research/ERA_GENERATIONAL_TREE_SEARCH.md).
