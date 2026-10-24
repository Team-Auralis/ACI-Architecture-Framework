# Glossary of Artificial Civilization Intelligence (ACI)

This glossary documents foundational, architectural, and operational terminology established across the ACI Architecture Framework.

---

## Cognitive Context & Agent Memory Architecture

### Payload Inundation
The rapid, non-linear dilution of transformer attention heads caused by dumping high-entropy, syntactically verbose tool execution artifacts (compiler outputs, full-file traces, test runner outputs, JSON dumps) directly into the active prompt window without semantic compression or ephemeral scoping. 
* *See full specification:* [`docs/research/CONTEXT_ARCHITECTURE_TRIFECTA.md`](research/CONTEXT_ARCHITECTURE_TRIFECTA.md)

### Generational Context
A multi-tiered systems architecture for LLM agent memory that stratifies context into distinct lifecycle tiers based on entropy, permanence, and semantic density. Inspired by generational garbage collection (JVM/V8) and virtual memory paging:
* **Generation 0 (Gen-0: Ephemeral)**: High-volume, high-entropy runtime execution artifacts (TTL = 1 turn; evicted immediately after distillation).
* **Generation 1 (Gen-1: Evaporative)**: Working plans, active hypotheses, and uncommitted diffs (paged to disk; updated by state replacement).
* **Generation 2 (Gen-2: Tenured)**: Permanent founding intent vectors, architectural rules, security boundaries, and user goals (permanently pinned; immune to compaction).
* *See full specification:* [`docs/research/CONTEXT_ARCHITECTURE_TRIFECTA.md`](research/CONTEXT_ARCHITECTURE_TRIFECTA.md)

### Error Gravitation
The non-linear cognitive pathology where an erroneous assumption, false diagnostic premise, or catastrophic failure traceback recorded in the context acts as a high-density semantic attractor basin. In subsequent inference turns, the self-attention mechanism assigns disproportionate probability mass to tokens consistent with the error trace, preventing the model from re-evaluating ground truth or exploring orthogonal solution vectors.
* *See full specification:* [`docs/research/CONTEXT_ARCHITECTURE_TRIFECTA.md`](research/CONTEXT_ARCHITECTURE_TRIFECTA.md)

### The Softmax Inundation Bound (The Fool's State)
The analytical bound proving that in autoregressive language agents operating over an unpruned append-only history buffer, the aggregate self-attention allocated to founding system invariants decays asymptotically as $\mathcal{O}(L_u / |\mathcal{S}_{\text{noise}}|)$. Without generational pruning, high-entropy distractor tokens dilute invariant attention, biasing subsequent generations toward symptom-patching loops rather than root-cause resolution (colloquially designated as The Fool's State).
* *See full specification:* [docs/research/FOOLS_THEOREM.md](research/FOOLS_THEOREM.md)
---

## Core ACI Framework Concepts

### ACI (Artificial Civilization Intelligence)
The theoretical and architectural paradigm beyond Artificial General Intelligence (AGI) and Artificial Superintelligence (ASI), governing how multi-agent autonomous systems coordinate, preserve civilizational values, and execute planetary-scale long-horizon tasks under verifiable safety envelopes.

### OCI (Ontological Civilization Intelligence)
The capability of an ACI system to rewrite its own underlying ontological structures, domain models, and meta-governance mechanisms without human intervention, bounded by invariant safety constraints.

### CIC (Civilizational Intent Conservation)
The formal property that an AI-mediated civilization can distinguish intentional, authorized evolution of its values from accidental drift over thousands of decision cycles, and algorithmically correct the latter.
* *See:* [`docs/research/CIVILIZATIONAL_INTENT_CONSERVATION.md`](research/CIVILIZATIONAL_INTENT_CONSERVATION.md)

### AICC (AI-Mediated Cultural Continuity)
The capability to actively preserve, transmit, and reconstruct civilizational knowledge, norms, and institutional memory across agent generations and domain shifts.

### EGE (Epistemic Governance Evolution)
The protocol by which the foundational governance rules of an autonomous civilization update themselves systematically to reflect discovered truths without creating governance ossification or systemic instability.

### OMNIS World Model
The shared, hypergraph-based distributed world model providing a causal, topological source of truth across all cooperating agents.

### NEXUS Agent Fabric
The high-throughput, asynchronous coordination and message fabric facilitating communication, consensus, and action dispatch across heterogeneous agent collectives.

### VEIL Security Framework
The cryptographically gated security and containment layer enforcing authorization envelopes, capability tokens, and invariant boundaries across all agent tool calls.
