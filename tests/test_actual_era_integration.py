"""
Unit and Integration Tests for Direct Google Research ERA Integration.
Directly tests benchmarks.google_era.futs.search() paired with GenerationalERAGenerator.
Standard library only.
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from generational_context.google_era import futs
from generational_context.era_adapter import StandardERAGenerator, GenerationalERAGenerator


class TestActualGoogleERAIntegration(unittest.TestCase):
    def test_direct_google_futs_execution_with_generational_adapter(self):
        """Tests Google's actual futs.search() running with ACI's GenerationalERAGenerator."""
        problem = futs.Problem("Optimize regression score on housing data.")
        initial_solution = futs.Solution(
            "def train_and_predict(train, test): return [0.5] * len(test)"
        )
        initial_score = -0.8500  # -RMSE

        # Mock mutation engine
        def mock_mutator(prompt: str) -> str:
            self.assertIn("MANDATORY PROBLEM INVARIANTS", prompt)
            self.assertIn("no_xgboost", prompt)
            return "def train_and_predict(train, test): return [0.45] * len(test)"

        gen_adapter = GenerationalERAGenerator(
            mutation_engine=mock_mutator,
            invariants={"no_xgboost": "DO NOT use xgboost or external boosting."},
            max_context_tokens=1200,
        )

        def mock_executor(prob: futs.Problem, sol: futs.Solution) -> float:
            self.assertIsInstance(sol, futs.Solution)
            return -0.7200  # Improved -RMSE

        # CALL GOOGLE RESEARCH'S EXACT futs.search() FUNCTION DIRECTLY
        best_sol, best_score = futs.search(
            problem=problem,
            initial_solution=initial_solution,
            initial_score=initial_score,
            generate_fn=gen_adapter,
            execute_fn=mock_executor,
            num_iterations=5,
            c_puct=1.0,
        )

        self.assertIsInstance(best_sol, futs.Solution)
        self.assertEqual(best_score, -0.7200)
        self.assertEqual(len(gen_adapter.total_tokens_emitted), 5)
        # Verify that prompt tokens are bounded
        for tok in gen_adapter.total_tokens_emitted:
            self.assertLess(tok, 500)

    def test_google_futs_standard_vs_generational_interface_parity(self):
        """Verifies exact interface parity between standard and generational ERA generators."""
        problem = futs.Problem("Fit scientific polynomial curve.")
        init_sol = futs.Solution("def fit(): return 1.0")
        init_score = 0.50

        std_gen = StandardERAGenerator(mutation_engine=lambda p: "def fit(): return 1.1")
        gen_gen = GenerationalERAGenerator(
            mutation_engine=lambda p: "def fit(): return 1.2",
            invariants={"positive": "Output must be > 0."},
        )

        # Both conform to futs.Generate Protocol
        sol1 = std_gen(problem, init_sol, init_score)
        sol2 = gen_gen(problem, init_sol, init_score)

        self.assertIsInstance(sol1, futs.Solution)
        self.assertIsInstance(sol2, futs.Solution)


if __name__ == "__main__":
    unittest.main()
