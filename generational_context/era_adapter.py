"""
Actual Google Research ERA Adapter for ACI Generational Context
Bridges Google's Flat UCB Tree Search (benchmarks.google_era.futs) directly with
ACI's 3-Tier Generational Memory (generational_context.memory).
"""

from __future__ import annotations

import re
from typing import Callable, Dict, List, Optional, Tuple

from .google_era import futs
from .memory import GenerationalMemory, DistilledObservation
from .awe import CacheEntry


class StandardERAGenerator:
    """
    Standard Google ERA generator matching implementation/playground_s3e1.py.
    Accumulates raw linear history without generational memory bounds.
    """

    def __init__(
        self,
        mutation_engine: Callable[[str], str],
        data_preview: str = "",
    ):
        self.mutation_engine = mutation_engine
        self.data_preview = data_preview
        self.history: List[str] = []
        self.total_tokens_emitted: List[int] = []

    def __call__(
        self,
        problem: futs.Problem,
        parent_solution: futs.Solution,
        parent_score: float,
    ) -> futs.Solution:
        # Accumulate history in standard ERA (linear unmanaged accumulation)
        self.history.append(
            f"Attempt #{len(self.history)+1} (Score: {-parent_score:.5f}):\n"
            f"```python\n{parent_solution.program.strip()}\n```"
        )

        # Reconstruct standard ERA prompt template from google-research/era
        prompt_parts = [
            f"Problem: {problem.description}",
            f"Data Preview:\n{self.data_preview}",
            f"Previous Score (RMSE): {-parent_score:.5f}",
            "History of attempts:",
        ]
        prompt_parts.extend(self.history)  # Unmanaged linear accumulation
        prompt_parts.append(f"Previous Code:\n```python\n{parent_solution.program}\n```")
        prompt_parts.append("Generate a new, improved Python program.")

        full_prompt = "\n\n".join(prompt_parts)
        prompt_tokens = len(re.findall(r"\w+", full_prompt))
        self.total_tokens_emitted.append(prompt_tokens)

        # Generate mutated program
        new_code = self.mutation_engine(full_prompt)
        return futs.Solution(program=new_code)


class GenerationalERAGenerator:
    """
    ACI-Enhanced Google ERA Generator.
    Enforces 3-tier Generational Context on top of Google's futs.search():
    - Gen-2: Permanently pinned problem invariants & negative constraints.
    - Gen-1: Active branch hypotheses managed by Adaptive Weight Evaporation (AWE).
    - Gen-0: Distilled execution feedback (<50 tokens) instead of raw traceback floods.
    """

    def __init__(
        self,
        mutation_engine: Callable[[str], str],
        invariants: Dict[str, str],
        max_context_tokens: int = 1500,
    ):
        self.mutation_engine = mutation_engine
        self.invariants = invariants
        self.max_context_tokens = max_context_tokens
        self.memory = GenerationalMemory(max_working_tokens=max_context_tokens)

        # Pin Gen-2 Invariants permanently
        for name, text in invariants.items():
            self.memory.pin_invariant(name, f"[INVARIANT: {name}] {text}")

        self.total_tokens_emitted: List[int] = []
        self.hypotheses_count = 0

    def record_feedback(self, status: str, score: float, root_cause: Optional[str] = None):
        """Distills execution feedback into Gen-0 memory before next generation."""
        summary = f"Execution Status: {status} | Score: {score:.4f}"
        if root_cause:
            summary += f" | RootCause: {root_cause[:80]}"

        # Distill into atomic observation using GenerationalMemory
        self.memory.record_tool_result(
            command="futs_execute",
            stdout=summary if status == "SUCCESS" else "",
            stderr=summary if status != "SUCCESS" else "",
            exit_code=0 if status == "SUCCESS" else 1,
        )

    def __call__(
        self,
        problem: futs.Problem,
        parent_solution: futs.Solution,
        parent_score: float,
    ) -> futs.Solution:
        self.hypotheses_count += 1

        # Add active hypothesis to Gen-1 working memory
        hyp_key = f"hyp_{self.hypotheses_count}"
        self.memory.cache.access(
            CacheEntry(
                key=hyp_key,
                content=f"Branch {self.hypotheses_count}: Iterative model mutation from parent score {parent_score:.4f}",
                tokens=20,
                tier="gen1",
                attention_weight=0.85,
                entropy=0.3,
            )
        )

        # Assemble strictly bounded context prompt
        sections = [
            "=== SECTION 1: MANDATORY PROBLEM INVARIANTS (GEN-2 TENURED) ===",
            f"Problem Objective: {problem.description}",
        ]
        for name, inv in self.invariants.items():
            sections.append(f"  * {inv}")

        sections.append("\n=== SECTION 2: ACTIVE WORKING MEMORY (GEN-1 AWE) ===")
        working_items = self.memory.compile_active_context()
        sections.append(working_items if working_items else "Nominal branch exploration.")

        sections.append("\n=== SECTION 3: PARENT SOLUTION TO MUTATE ===")
        sections.append(f"Parent Score (RMSE): {-parent_score:.5f}")
        sections.append(f"```python\n{parent_solution.program.strip()}\n```")
        sections.append("Task: Mutate the code to improve validation score while strictly honoring all Gen-2 invariants.")

        full_prompt = "\n".join(sections)
        prompt_tokens = len(re.findall(r"\w+", full_prompt))
        self.total_tokens_emitted.append(prompt_tokens)

        # Generate mutated program
        new_code = self.mutation_engine(full_prompt)
        return futs.Solution(program=new_code)
