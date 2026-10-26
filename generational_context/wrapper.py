"""
Universal ContextOS Wrapper
Drop-In Middleware for Agent Execution Runtimes
"""

from typing import List, Dict, Optional, Any, Callable
from .memory import GenerationalMemory, DistilledObservation


class ContextOS:
    """
    Drop-In Middleware for LLM Agent Execution Runtimes.
    Prevents The Fool's Theorem and eliminates Payload Inundation in 2 lines of code.

    Usage:
        cos = ContextOS(
            goal="Refactor authentication layer",
            invariants=["Preserve standard library compliance", "Do not modify DB schema"]
        )

        # Inside agent execution loop:
        cos.observe_tool(cmd, stdout, stderr, exit_code)
        active_prompt = cos.compile_prompt(current_user_message)
    """

    def __init__(
        self,
        goal: str,
        invariants: Optional[List[str]] = None,
        max_working_tokens: int = 4000,
        egi_threshold: float = 0.35,
    ):
        self.memory = GenerationalMemory(
            max_working_tokens=max_working_tokens, egi_threshold=egi_threshold
        )
        # Pin Root Objective and Invariants as Gen-2 Tenured
        self.memory.pin_invariant("root_objective", f"PRIMARY GOAL: {goal}")
        if invariants:
            for idx, inv in enumerate(invariants):
                self.memory.pin_invariant(f"inv_{idx}", f"INVARIANT CONSTRAINT: {inv}")

    def observe_tool(
        self, command: str, stdout: str, stderr: str = "", exit_code: int = 0
    ) -> DistilledObservation:
        """Intercepts tool execution and runs Gen-0 distillation."""
        return self.memory.record_tool_result(command, stdout, stderr, exit_code)

    def record_reasoning(self, hypothesis: str) -> bool:
        """
        Records the model's hypothesis and checks for Error Gravitation.
        Returns True if an attractor loop was detected and flushed.
        """
        egi = self.memory.check_error_gravitation(hypothesis)
        if egi > self.memory.egi_threshold:
            self.memory.break_attractor_loop()
            if hasattr(self.memory, "advance_turn"):
                self.memory.advance_turn(1)
            elif hasattr(self.memory, "_turn_counter"):
                self.memory._turn_counter += 1
            return True
        self.memory.record_hypothesis(hypothesis)
        # Advance turn counter for Gen-0 TTL (best-effort)
        if hasattr(self.memory, "advance_turn"):
            self.memory.advance_turn(1)
        elif hasattr(self.memory, "_turn_counter"):
            self.memory._turn_counter += 1
        return False

    def compile_prompt(self, user_prompt: str = "") -> str:
        """Generates the active prompt context without raw noise."""
        compiled_context = self.memory.compile_active_context()
        if user_prompt:
            return f"{compiled_context}\n\n=== USER INPUT ===\n{user_prompt}"
        return compiled_context

    def get_telemetry(self) -> Dict[str, Any]:
        """Returns token savings and efficiency stats."""
        raw_ingested = self.memory.total_raw_tokens_ingested
        active_tokens = self.memory.total_active_tokens_emitted
        savings_pct = (
            round((1.0 - (active_tokens / max(raw_ingested, 1))) * 100.0, 1)
            if raw_ingested > 0
            else 0.0
        )
        return {
            "total_raw_tokens_intercepted": raw_ingested,
            "current_active_context_tokens": active_tokens,
            "token_reduction_ratio": f"{savings_pct}%",
            "tenured_invariants_count": len(self.memory.gen2_invariants),
            "cached_working_entries": len(self.memory.cache.get_active_entries()),
        }
