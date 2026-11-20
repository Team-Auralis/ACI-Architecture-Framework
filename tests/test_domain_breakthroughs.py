"""
Unit and Integration Tests for the 15 Real-World Breakthrough Domain Specifications.
Validates invariant creation, domain regex distillation, and tree search integration.
Standard library only.
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from generational_context.domain_invariants import (
    BREAKTHROUGH_CATALOG,
    create_breakthrough_problem,
    distill_domain_execution,
)
from generational_context.tree_search import GenerationalTreeSearch, Solution, ExecutionResult


class TestDomainBreakthroughs(unittest.TestCase):
    def test_catalog_completeness(self):
        """Assert exactly 15 breakthrough specifications exist with valid fields."""
        self.assertEqual(len(BREAKTHROUGH_CATALOG), 15)
        for i in range(1, 16):
            bt_id = f"BT-{i:02d}"
            self.assertIn(bt_id, BREAKTHROUGH_CATALOG)
            spec = BREAKTHROUGH_CATALOG[bt_id]
            self.assertEqual(spec.domain_id, bt_id)
            self.assertTrue(len(spec.name) > 0)
            self.assertTrue(len(spec.sector) > 0)
            self.assertTrue(len(spec.real_world_stake) > 0)
            self.assertGreaterEqual(len(spec.invariants), 2)
            self.assertTrue(len(spec.metric_name) > 0)
            self.assertGreaterEqual(len(spec.distillation_regexes), 1)

    def test_domain_distillation_biopharma(self):
        """Test BT-01: Lipinski / Valence log distillation."""
        spec = BREAKTHROUGH_CATALOG["BT-01"]
        raw_log = """
        [AutoDock Vina] Iteration 42 starting molecular dynamics docking sweep.
        Rigid receptor grid: 40 x 40 x 40 points centered at active pocket (12.4, -4.2, 38.1).
        Conformation sampling: Monte Carlo simulated annealing across 2,500,000 steps.
        Checking bond torsions for dihedral flexibility...
        ValenceViolation: Carbon atom C14 has 5 covalent bonds in pyrrole ring.
        Warning: Atomic overlap in van der Waals radii detected at residue ASP-189.
        Refining binding energy matrix:
        Mode 1 | Affinity: -8.4 kcal/mol | RMSD l.b.: 1.42 | RMSD u.b.: 2.89
        Mode 2 | Affinity: -7.9 kcal/mol | RMSD l.b.: 2.10 | RMSD u.b.: 3.45
        VinaAffinity: -8.4 kcal/mol
        Docking simulation terminated with non-physical stereocenter configuration.
        """
        sig = distill_domain_execution(
            spec=spec,
            raw_output=raw_log,
            score=-8.4,
            parent_score=-7.2,
            status="SUCCESS",
        )
        self.assertEqual(sig.status, "INVARIANT_VIOLATION")
        self.assertIn("ValenceViolation", sig.root_cause_signature)
        self.assertLess(sig.distilled_tokens, sig.raw_tokens)

    def test_domain_distillation_fusion_tokamak(self):
        """Test BT-02: DivB / Grad-Shafranov MHD distillation."""
        spec = BREAKTHROUGH_CATALOG["BT-02"]
        raw_log = """
        [NIMROD MHD Solver] Mesh refinement step 12
        DivBError: 4.82e-06 exceeded machine precision threshold.
        BetaPoloidal: 1.42
        """
        sig = distill_domain_execution(
            spec=spec,
            raw_output=raw_log,
            score=0.35,
            parent_score=0.82,
            status="SUCCESS",
        )
        self.assertEqual(sig.status, "ANOMALY")
        self.assertIn("DivBError", sig.root_cause_signature)

    def test_domain_tree_search_initialization(self):
        """Test initializing GenerationalTreeSearch on a domain breakthrough problem."""
        spec = BREAKTHROUGH_CATALOG["BT-03"]  # Power Grid
        problem = create_breakthrough_problem(spec)
        searcher = GenerationalTreeSearch(problem=problem, max_context_tokens=2500)

        root = searcher.initialize_root(
            initial_solution=Solution(
                program="def dispatch_grid(scada): return {'generator_mw': 500}",
                hypotheses=["Initial N-1 contingency baseline"],
            ),
            initial_score=450.0,
            initial_result=ExecutionResult(score=450.0, status="SUCCESS", stdout="Nominal grid state"),
        )

        prompt = searcher.assemble_context_prompt(root)
        self.assertIn("BT-03", prompt)
        self.assertIn("frequency_nadir", prompt)
        self.assertIn("transformer_mva_thermal", prompt)
        self.assertIn("Initial N-1 contingency baseline", prompt)


if __name__ == "__main__":
    unittest.main()
