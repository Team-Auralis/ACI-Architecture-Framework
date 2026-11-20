"""
Generational Context: Tiered Attention Lifecycle & The Fool's Theorem Prevention Engine
"""

from .awe import AdaptiveReplacementAttentionCache, CacheEntry
from .memory import DistilledObservation, GenerationalMemory
from .wrapper import ContextOS
from .tree_search import (
    Problem,
    Solution,
    ExecutionResult,
    DistilledExecutionSignature,
    GenerationalNode,
    GenerationalTreeSearch,
    compute_rank_scores,
    compute_pucts,
    backpropagate_visit,
    distill_execution_result,
)
from .domain_invariants import (
    BREAKTHROUGH_CATALOG,
    DomainBreakthroughSpec,
    create_breakthrough_problem,
    distill_domain_execution,
)
from .era_adapter import (
    StandardERAGenerator,
    GenerationalERAGenerator,
)

__version__ = "0.4.0"
__all__ = [
    "AdaptiveReplacementAttentionCache",
    "CacheEntry",
    "ContextOS",
    "DistilledObservation",
    "GenerationalMemory",
    "Problem",
    "Solution",
    "ExecutionResult",
    "DistilledExecutionSignature",
    "GenerationalNode",
    "GenerationalTreeSearch",
    "compute_rank_scores",
    "compute_pucts",
    "backpropagate_visit",
    "distill_execution_result",
    "BREAKTHROUGH_CATALOG",
    "DomainBreakthroughSpec",
    "create_breakthrough_problem",
    "distill_domain_execution",
    "StandardERAGenerator",
    "GenerationalERAGenerator",
]
