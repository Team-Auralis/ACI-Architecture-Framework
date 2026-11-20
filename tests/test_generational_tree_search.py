"""
Unit and Integration Tests for Generational Tree Search (Gen-FUTS).
Tests bounded-context tree search, rank scoring, PUCT, and Gen-0 execution distillation.
Standard library only.
"""

import os
import sys
import unittest

# Add parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from generational_context.tree_search import (
    Problem,
    Solution,
    ExecutionResult,
    GenerationalNode,
    GenerationalTreeSearch,
    compute_rank_scores,
    compute_pucts,
    backpropagate_visit,
    distill_execution_result,
)


class TestGenerationalTreeSearch(unittest.TestCase):
    def test_rank_scores_single_and_multi(self):
        n0 = GenerationalNode(index=0, parent_index=None, solution=Solution("code0"), score=10.0)
        compute_rank_scores([n0])
        self.assertEqual(n0.rank_score, 0.5)

        n1 = GenerationalNode(index=1, parent_index=0, solution=Solution("code1"), score=30.0)
        n2 = GenerationalNode(index=2, parent_index=0, solution=Solution("code2"), score=20.0)
        compute_rank_scores([n0, n1, n2])
        self.assertEqual(n0.rank_score, 0.0)
        self.assertEqual(n2.rank_score, 0.5)
        self.assertEqual(n1.rank_score, 1.0)

    def test_puct_computation_and_backpropagation(self):
        n0 = GenerationalNode(index=0, parent_index=None, solution=Solution("code0"), score=10.0)
        n1 = GenerationalNode(index=1, parent_index=0, solution=Solution("code1"), score=20.0)
        nodes = [n0, n1]

        backpropagate_visit(nodes, n1)
        self.assertEqual(n1.num_visits, 1)
        self.assertEqual(n0.num_visits, 1)

        compute_rank_scores(nodes)
        compute_pucts(nodes, c_puct=1.0)
        self.assertGreater(n1.puct, 0.0)
        self.assertGreater(n0.puct, 0.0)

    def test_distill_execution_result(self):
        raw_traceback = """Traceback (most recent call last):
  File "solver.py", line 42, in integrate
    res = matrix_multiply(a, b)
  File "kernel.py", line 12, in matrix_multiply
    raise ValueError("DimensionMismatch: matrix A (100x64) and B (32x64) incompatible")
ValueError: DimensionMismatch: matrix A (100x64) and B (32x64) incompatible
"""
        exec_res = ExecutionResult(
            score=-999.0,
            status="EXCEPTION",
            stderr=raw_traceback,
        )

        sig = distill_execution_result(exec_res, parent_score=50.0, maximize=True)
        self.assertEqual(sig.status, "EXCEPTION")
        self.assertIn("ValueError", sig.root_cause_signature)
        self.assertIn("DimensionMismatch", sig.root_cause_signature)
        self.assertLess(sig.distilled_tokens, sig.raw_tokens)
        self.assertIn("RootCause", sig.summary)

    def test_generational_tree_search_loop(self):
        problem = Problem(
            description="Optimize scientific ODE kernel",
            invariants={
                "energy_conservation": "Total system energy must not drift > 1e-4.",
                "forbidden_imports": "Do not import scipy.integrate or external solvers.",
            },
            metric_name="numerical_accuracy",
            maximize=True,
        )

        searcher = GenerationalTreeSearch(
            problem=problem,
            c_puct=1.0,
            max_context_tokens=2000,
        )

        root = searcher.initialize_root(
            initial_solution=Solution(
                program="def solve(): return 1.0",
                hypotheses=["Initial Euler baseline"],
            ),
            initial_score=0.40,
        )

        self.assertEqual(len(searcher.nodes), 1)

        # Verify context prompt assembly has invariants pinned
        prompt = searcher.assemble_context_prompt(root)
        self.assertIn("energy_conservation", prompt)
        self.assertIn("forbidden_imports", prompt)
        self.assertIn("Initial Euler baseline", prompt)

        # Mock generator and executor
        def mock_generate(prob, parent, prompt_str):
            new_idx = len(searcher.nodes)
            return Solution(
                program=f"def solve_v{new_idx}(): return {new_idx} * 0.1",
                hypotheses=[f"Hypothesis {new_idx}: higher order integration step"],
            )

        def mock_execute(prob, sol):
            idx = len(searcher.nodes)
            return ExecutionResult(
                score=0.40 + (idx * 0.05),
                status="SUCCESS",
                stdout=f"Kernel benchmark iteration {idx} passed.",
            )

        # Run 5 iterations of tree search
        for _ in range(5):
            searcher.step(mock_generate, mock_execute)

        self.assertEqual(len(searcher.nodes), 6)
        best_sol, best_score = searcher.get_best_solution()
        self.assertGreater(best_score, 0.40)
        self.assertEqual(searcher.telemetry["nodes_expanded"], 5)
        self.assertGreater(searcher.telemetry["distilled_tokens_emitted"], 0)


if __name__ == "__main__":
    unittest.main()
