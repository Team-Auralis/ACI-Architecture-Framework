"""
Generational Tree Search (Gen-FUTS)
Extends Google Research ERA's Flat UCB Tree Search (FUTS) with 3-tier Generational Context:
- Gen-2: Tenured Invariants (Scientific laws, mathematical constraints, safety contracts)
- Gen-1: Evaporative Working Hypotheses (AWE-governed active algorithmic ideas)
- Gen-0: Ephemeral Execution Distillation (Atomic execution signatures instead of raw log floods)
"""

from __future__ import annotations

import dataclasses
import math
import re
from typing import Any, Callable, Dict, List, Optional, Protocol, Tuple

from .awe import CacheEntry
from .memory import GenerationalMemory


@dataclasses.dataclass(frozen=True)
class Problem:
    """Problem definition with scientific objective and formal constraints."""
    description: str
    invariants: Dict[str, str] = dataclasses.field(default_factory=dict)
    metric_name: str = "score"
    maximize: bool = True


@dataclasses.dataclass(frozen=True)
class Solution:
    """Candidate program and active scientific hypotheses."""
    program: str
    hypotheses: List[str] = dataclasses.field(default_factory=list)
    metadata: Dict[str, Any] = dataclasses.field(default_factory=dict)


@dataclasses.dataclass
class ExecutionResult:
    """Raw sandboxed execution feedback."""
    score: float
    status: str = "SUCCESS"  # SUCCESS, EXCEPTION, TIMEOUT, INVARIANT_VIOLATION
    stdout: str = ""
    stderr: str = ""
    metrics: Dict[str, float] = dataclasses.field(default_factory=dict)


@dataclasses.dataclass(frozen=True)
class DistilledExecutionSignature:
    """
    Gen-0 Ephemeral Distillation of raw execution logs.
    Captures exact scientific signal while discarding unbounded noise tokens.
    """
    status: str
    score: float
    metric_delta: float
    root_cause_signature: Optional[str] = None
    summary: str = ""
    raw_tokens: int = 0
    distilled_tokens: int = 0


@dataclasses.dataclass
class GenerationalNode:
    """Node in the Generational Tree Search."""
    index: int
    parent_index: Optional[int]
    solution: Solution
    score: float
    num_visits: int = 0
    rank_score: float = 0.5
    puct: float = 0.5
    execution_signature: Optional[DistilledExecutionSignature] = None
    memory: Optional[GenerationalMemory] = None


class GenerateFn(Protocol):
    """Generates an improved candidate solution using generational context."""
    def __call__(
        self,
        problem: Problem,
        parent_node: GenerationalNode,
        context_prompt: str,
    ) -> Solution:
        ...


class ExecuteFn(Protocol):
    """Executes a candidate program in a sandbox and returns ExecutionResult."""
    def __call__(self, problem: Problem, solution: Solution) -> ExecutionResult:
        ...


def distill_execution_result(
    result: ExecutionResult,
    parent_score: float,
    maximize: bool = True,
) -> DistilledExecutionSignature:
    """
    Distills raw stdout/stderr into an atomic execution signature (Gen-0).
    Replaces 500-2000 token tracebacks with a <50 token signature tuple.
    """
    raw_text = f"{result.stdout}\n{result.stderr}".strip()
    raw_tokens = len(re.findall(r"\w+", raw_text)) or 1

    metric_delta = (
        (result.score - parent_score) if maximize else (parent_score - result.score)
    )

    root_cause = None
    if result.status != "SUCCESS":
        # Extract exception signature
        exc_match = re.search(
            r"([A-Za-z0-9_]+(?:Error|Exception|Warning|Fault)):?\s*([^\n\r]+)?",
            result.stderr or result.stdout,
        )
        if exc_match:
            exc_type = exc_match.group(1)
            exc_msg = (exc_match.group(2) or "").strip()[:80]
            root_cause = f"{exc_type}: {exc_msg}"
        elif "Timeout" in result.status:
            root_cause = "ExecutionTimeout: exceeded wall-clock budget"
        elif "INVARIANT" in result.status:
            root_cause = "InvariantViolation: violated physical or computational bound"
        else:
            root_cause = "UnknownExecutionAnomaly"

    summary_parts = [f"Status={result.status}", f"Score={result.score:.5f}"]
    if metric_delta != 0.0:
        summary_parts.append(f"Delta={metric_delta:+.5f}")
    if root_cause:
        summary_parts.append(f"RootCause=[{root_cause}]")

    summary = " | ".join(summary_parts)
    distilled_tokens = len(re.findall(r"\w+", summary))

    return DistilledExecutionSignature(
        status=result.status,
        score=result.score,
        metric_delta=metric_delta,
        root_cause_signature=root_cause,
        summary=summary,
        raw_tokens=raw_tokens,
        distilled_tokens=distilled_tokens,
    )


def compute_rank_scores(nodes: List[GenerationalNode]) -> None:
    """Computes normalized empirical rank scores Q(n) in [0, 1]."""
    if len(nodes) == 1:
        nodes[0].rank_score = 0.5
        return
    sorted_nodes = sorted(nodes, key=lambda n: n.score)
    denom = len(sorted_nodes) - 1
    for rank, node in enumerate(sorted_nodes):
        node.rank_score = rank / denom


def compute_pucts(nodes: List[GenerationalNode], c_puct: float = 1.0) -> None:
    """Computes PUCT scores using polynomial upper confidence bounds."""
    if not nodes:
        return
    prior = 1.0 / len(nodes)
    total_visits = sum(n.num_visits for n in nodes)
    sqrt_total = math.sqrt(total_visits)
    for node in nodes:
        node.puct = node.rank_score + c_puct * prior * sqrt_total / (1 + node.num_visits)


def backpropagate_visit(nodes: List[GenerationalNode], node: GenerationalNode) -> None:
    """Recursively updates visit counts up to root."""
    node.num_visits += 1
    if node.parent_index is not None and 0 <= node.parent_index < len(nodes):
        backpropagate_visit(nodes, nodes[node.parent_index])


class GenerationalTreeSearch:
    """
    Flat UCB Tree Search with 3-tier Generational Context Management.
    Prevents Softmax Inundation and Error Gravitation during empirical program synthesis.
    """

    def __init__(
        self,
        problem: Problem,
        c_puct: float = 1.0,
        max_context_tokens: int = 3500,
        gen0_ttl_turns: int = 1,
    ):
        self.problem = problem
        self.c_puct = c_puct
        self.max_context_tokens = max_context_tokens
        self.gen0_ttl_turns = gen0_ttl_turns

        self.nodes: List[GenerationalNode] = []
        self.telemetry = {
            "iterations": 0,
            "raw_log_tokens_generated": 0,
            "distilled_tokens_emitted": 0,
            "invariant_violations_prevented": 0,
            "nodes_expanded": 0,
            "best_score_progression": [],
        }

    def _init_node_memory(
        self, parent_node: Optional[GenerationalNode] = None
    ) -> GenerationalMemory:
        """Initializes generational memory inheriting invariants and active branch state."""
        mem = GenerationalMemory(
            max_working_tokens=self.max_context_tokens,
            gen0_ttl_turns=self.gen0_ttl_turns,
        )

        # Pin Problem Invariants into Gen-2 (Never Evicted)
        mem.pin_invariant("problem_desc", self.problem.description)
        for name, inv_text in self.problem.invariants.items():
            mem.pin_invariant(f"invariant_{name}", f"[INVARIANT: {name}] {inv_text}")

        # If parent exists, inherit active Gen-1 hypotheses from branch lineage
        if parent_node and parent_node.memory:
            # Transfer working memory items from parent that haven't evaporated
            for key, entry in parent_node.memory.cache.t1.items():
                if entry.tier == "gen1":
                    mem.cache.access(
                        CacheEntry(
                            key=key,
                            content=entry.content,
                            tokens=entry.tokens,
                            tier="gen1",
                            attention_weight=entry.attention_weight * 0.95,  # slight lineage evaporation
                            entropy=entry.entropy,
                        )
                    )
            for key, entry in parent_node.memory.cache.t2.items():
                if entry.tier == "gen1":
                    mem.cache.access(
                        CacheEntry(
                            key=key,
                            content=entry.content,
                            tokens=entry.tokens,
                            tier="gen1",
                            attention_weight=entry.attention_weight * 0.95,
                            entropy=entry.entropy,
                        )
                    )

        return mem

    def assemble_context_prompt(self, node: GenerationalNode) -> str:
        """
        Assembles bounded context prompt:
        Tier 2: Invariants (Pinned at top)
        Tier 1: Active Branch Hypotheses
        Tier 0: Distilled Execution Feedback from parent
        """
        sections = []

        # Tier 2: Problem & Invariants
        sections.append("=== SECTION 1: PROBLEM SPECIFICATION & TENURED INVARIANTS (GEN-2) ===")
        sections.append(f"Problem: {self.problem.description}")
        sections.append(f"Optimization Objective: {self.problem.metric_name} (Maximize={self.problem.maximize})")
        if self.problem.invariants:
            sections.append("MANDATORY SCIENTIFIC & COMPUTATIONAL INVARIANTS:")
            for name, text in self.problem.invariants.items():
                sections.append(f"  * [{name}]: {text}")

        # Tier 1: Working Hypotheses along the lineage
        if node.solution.hypotheses:
            sections.append("\n=== SECTION 2: ACTIVE SCIENTIFIC HYPOTHESES (GEN-1) ===")
            for idx, h in enumerate(node.solution.hypotheses, 1):
                sections.append(f"  {idx}. {h}")

        # Tier 0: Distilled Parent Performance & Execution Signature
        sections.append("\n=== SECTION 3: LINEAGE EXECUTION SIGNATURE (GEN-0 DISTILLED) ===")
        sections.append(f"Parent Node Index: {node.index} (Visits={node.num_visits}, RankScore={node.rank_score:.4f})")
        sections.append(f"Parent Score: {node.score:.5f}")
        if node.execution_signature:
            sections.append(f"Parent Execution Feedback: {node.execution_signature.summary}")
            if node.execution_signature.root_cause_signature:
                sections.append(f"Root Cause to Address: {node.execution_signature.root_cause_signature}")

        # Parent Program Code
        sections.append("\n=== SECTION 4: CANDIDATE CODE TO REFINE ===")
        sections.append("```python\n" + node.solution.program.strip() + "\n```")

        sections.append("\nTask: Synthesize an improved Python program adhering strictly to all Gen-2 invariants.")
        return "\n".join(sections)

    def initialize_root(
        self,
        initial_solution: Solution,
        initial_score: float,
        initial_result: Optional[ExecutionResult] = None,
    ) -> GenerationalNode:
        """Initializes root node of the search tree."""
        mem = self._init_node_memory()
        sig = None
        if initial_result:
            sig = distill_execution_result(
                initial_result,
                parent_score=initial_score,
                maximize=self.problem.maximize,
            )
            self.telemetry["raw_log_tokens_generated"] += sig.raw_tokens
            self.telemetry["distilled_tokens_emitted"] += sig.distilled_tokens

        root = GenerationalNode(
            index=0,
            parent_index=None,
            solution=initial_solution,
            score=initial_score,
            execution_signature=sig,
            memory=mem,
        )
        self.nodes.append(root)
        self.telemetry["best_score_progression"].append(initial_score)
        return root

    def step(
        self,
        generate_fn: GenerateFn,
        execute_fn: ExecuteFn,
    ) -> GenerationalNode:
        """Performs one iteration of Generational Flat UCB Tree Search."""
        if not self.nodes:
            raise ValueError("Tree not initialized. Call initialize_root first.")

        # 1. Compute Rank Scores & PUCTs
        compute_rank_scores(self.nodes)
        compute_pucts(self.nodes, self.c_puct)

        # 2. Select Node with largest PUCT
        best_parent = max(self.nodes, key=lambda n: n.puct)

        # 3. Assemble bounded generational prompt
        prompt = self.assemble_context_prompt(best_parent)

        # 4. Generate candidate child solution
        child_solution = generate_fn(self.problem, best_parent, prompt)

        # 5. Execute candidate program in sandbox
        exec_result = execute_fn(self.problem, child_solution)

        # 6. Distill raw execution logs (Gen-0 Ephemeral Distillation)
        distilled_sig = distill_execution_result(
            exec_result,
            parent_score=best_parent.score,
            maximize=self.problem.maximize,
        )

        self.telemetry["raw_log_tokens_generated"] += distilled_sig.raw_tokens
        self.telemetry["distilled_tokens_emitted"] += distilled_sig.distilled_tokens

        # 7. Create child node with inherited & bounded memory
        child_mem = self._init_node_memory(parent_node=best_parent)

        # Ingest new hypotheses into Gen-1 working memory
        for h in child_solution.hypotheses:
            h_tokens = len(re.findall(r"\w+", h))
            child_mem.cache.access(
                CacheEntry(
                    key=f"hyp_{len(self.nodes)}_{h[:15]}",
                    content=h,
                    tokens=h_tokens,
                    tier="gen1",
                    attention_weight=0.8,
                    entropy=0.5,
                )
            )

        child_node = GenerationalNode(
            index=len(self.nodes),
            parent_index=best_parent.index,
            solution=child_solution,
            score=exec_result.score,
            execution_signature=distilled_sig,
            memory=child_mem,
        )
        self.nodes.append(child_node)

        # 8. Backpropagate visits
        backpropagate_visit(self.nodes, child_node)

        # Update telemetry
        self.telemetry["iterations"] += 1
        self.telemetry["nodes_expanded"] += 1
        current_best = (
            max(n.score for n in self.nodes)
            if self.problem.maximize
            else min(n.score for n in self.nodes)
        )
        self.telemetry["best_score_progression"].append(current_best)

        return child_node

    def get_best_solution(self) -> Tuple[Solution, float]:
        """Returns the optimal solution found across the tree search."""
        if not self.nodes:
            raise ValueError("No nodes in search tree.")
        best_node = (
            max(self.nodes, key=lambda n: n.score)
            if self.problem.maximize
            else min(self.nodes, key=lambda n: n.score)
        )
        return best_node.solution, best_node.score
