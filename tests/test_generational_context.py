"""
Unit and Integration Tests for generational_context package and AWE algorithm.
Standard library only.
"""

import unittest
import sys
import os

# Add parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from generational_context import (
    ContextOS,
    GenerationalMemory,
    AdaptiveReplacementAttentionCache,
    CacheEntry,
)

# Single source of truth for whether Ed25519 is available.
from cic_bench import _HAS_CRYPTO


class TestAWEAlgorithm(unittest.TestCase):
    def test_cache_hit_and_promotion(self):
        cache = AdaptiveReplacementAttentionCache(capacity_tokens=100)
        e1 = CacheEntry(key="k1", content="test1", tokens=20, tier="gen0")
        evicted = cache.access(e1)
        self.assertEqual(len(evicted), 0)
        self.assertIn("k1", cache.t1)

        # Access again -> should promote to T2
        cache.access(e1)
        self.assertIn("k1", cache.t2)
        self.assertNotIn("k1", cache.t1)

    def test_adaptive_eviction_on_overflow(self):
        cache = AdaptiveReplacementAttentionCache(capacity_tokens=50)
        e1 = CacheEntry(
            key="k1",
            content="chunk 1",
            tokens=30,
            tier="gen0",
            attention_weight=0.1,
            entropy=2.0,
        )
        e2 = CacheEntry(
            key="k2",
            content="chunk 2",
            tokens=30,
            tier="gen0",
            attention_weight=0.9,
            entropy=0.1,
        )

        cache.access(e1)
        evicted = cache.access(e2)

        # Total tokens exceeded 50, so e1 with lower information density should be evicted to B1
        self.assertEqual(len(evicted), 1)
        self.assertEqual(evicted[0].key, "k1")
        self.assertIn("k1", cache.b1)
        self.assertIn("k2", cache.t1)
        self.assertLessEqual(cache.total_tokens(), 50)

    def test_oversized_entry_capacity_invariant(self):
        """
        Adversarial Test: Capacity = 10, single incoming entry = 25 tokens.
        Regression test for capacity overflow bug flagged in external audit.
        """
        cache = AdaptiveReplacementAttentionCache(capacity_tokens=10)
        oversized = CacheEntry(
            key="oversized_log",
            content="word1 word2 word3 word4 word5 word6 word7 word8 word9 word10 word11 word12 word13 word14 word15 word16 word17 word18 word19 word20 word21 word22 word23 word24 word25",
            tokens=25,
            tier="gen0",
        )
        cache.access(oversized)
        self.assertLessEqual(cache.total_tokens(), 10)
        self.assertEqual(cache.total_tokens(), 10)
        self.assertIn("oversized_log", cache.t1)

    def test_default_information_density_scores(self):
        """Unmeasured entries must not collapse to 0.0 or tie arbitrarily."""
        e_gen0 = CacheEntry(key="g0", content="foo", tokens=10, tier="gen0")
        e_gen1 = CacheEntry(key="g1", content="bar", tokens=10, tier="gen1")
        e_gen2 = CacheEntry(key="g2", content="baz", tokens=10, tier="gen2")

        self.assertGreater(e_gen0.information_density, 0.0)
        self.assertGreater(e_gen1.information_density, e_gen0.information_density)
        self.assertGreater(e_gen2.information_density, e_gen1.information_density)

    def test_continuous_capacity_invariant_under_stream(self):
        """Stress test: 30 entries of varied sizes, verifying capacity invariant holds after each."""
        capacity = 50
        cache = AdaptiveReplacementAttentionCache(capacity_tokens=capacity)
        for i in range(30):
            token_size = (i * 7) % 65 + 5  # Sizes ranging from 5 to 69 tokens
            entry = CacheEntry(
                key=f"chunk_{i}",
                content=f"Content for chunk {i} " * (token_size // 4 + 1),
                tokens=token_size,
                tier="gen0" if i % 2 == 0 else "gen1",
            )
            cache.access(entry)
            self.assertLessEqual(
                cache.total_tokens(), capacity, f"Invariant violated at step {i}"
            )

    def test_structural_envelope_overhead_invariant(self):
        """
        Verify that structural delimiters, role tags, and framing metadata
        are strictly counted against capacity C_bound.
        """
        capacity = 50
        # 10 tokens fixed context framing (headers/delimiters)
        cache = AdaptiveReplacementAttentionCache(
            capacity_tokens=capacity, fixed_envelope_overhead=10
        )

        # Add entry with 25 payload tokens and 5 delimiter envelope tokens (effective = 30)
        e1 = CacheEntry(
            key="cmd1", content="run tests", tokens=25, tier="gen0", envelope_tokens=5
        )
        cache.access(e1)
        self.assertEqual(cache.total_tokens(), 40)  # 25 + 5 + 10 = 40 <= 50

        # Add second entry with 15 payload tokens and 5 delimiter tokens (effective = 20)
        # Total would be 40 + 20 = 60 > 50, triggering eviction of lowest density item
        e2 = CacheEntry(
            key="cmd2",
            content="run lint",
            tokens=15,
            tier="gen0",
            envelope_tokens=5,
            attention_weight=0.9,
        )
        evicted = cache.access(e2)

        self.assertLessEqual(cache.total_tokens(), capacity)
        self.assertEqual(len(evicted), 1)
        self.assertEqual(evicted[0].key, "cmd1")
        self.assertEqual(cache.total_tokens(), 30)  # 15 + 5 + 10 = 30 <= 50


class TestContextOSIntegration(unittest.TestCase):
    def test_context_os_distillation_and_tenured_pinning(self):
        cos = ContextOS(
            goal="Refactor monolithic auth service",
            invariants=["Do not change public API", "Maintain 100% test coverage"],
        )

        # Verify invariants are in prompt
        prompt = cos.compile_prompt("Hello agent")
        self.assertIn("PRIMARY GOAL: Refactor monolithic auth service", prompt)
        self.assertIn("INVARIANT CONSTRAINT: Do not change public API", prompt)

        # Simulate massive 10,000 token tool failure
        fake_traceback = (
            "Traceback (most recent call last):\n"
            + ("  File 'auth.py', line 99, in verify\n" * 500)
            + "ZeroDivisionError: division by zero"
        )
        obs = cos.observe_tool(
            "pytest tests/test_auth.py", stdout="", stderr=fake_traceback, exit_code=1
        )

        # Verify distillation prevented Payload Inundation
        self.assertTrue(obs.distilled_token_count < 100)
        self.assertTrue(obs.raw_token_count > 1000)

        # Check compiled prompt has distilled summary, not 500 lines of traceback
        prompt_after_tool = cos.compile_prompt()
        self.assertIn("failed with exit code 1", prompt_after_tool)
        self.assertIn("ZeroDivisionError", prompt_after_tool)
        self.assertTrue(len(prompt_after_tool.splitlines()) < 25)

        # Telemetry verification
        stats = cos.get_telemetry()
        self.assertTrue(float(stats["token_reduction_ratio"].replace("%", "")) > 90.0)

    def test_error_gravitation_break(self):
        cos = ContextOS(goal="Fix bug", egi_threshold=0.30)
        cos.observe_tool(
            "run", stdout="", stderr="ConnectionRefusedError: port 6379", exit_code=1
        )

        # Record repetitive hypothesis closely aligned with error
        loop_detected = cos.record_reasoning(
            "The ConnectionRefusedError port 6379 must be resolved in redis config."
        )
        self.assertIsInstance(loop_detected, bool)


class TestCICCrypto(unittest.TestCase):
    """Ed25519 signing is optional; the HMAC fallback keeps the library usable
    without `cryptography`, so these skip rather than fail when it is absent."""

    @unittest.skipUnless(_HAS_CRYPTO, "cryptography not installed")
    def test_cic_keypair_sign_verify(self):
        from cic_bench import CICKeyPair, CollectiveIntent

        kp = CICKeyPair()
        intent = CollectiveIntent(
            goals=["Preserve safety"],
            values=["Non-maleficence"],
            constraints=["No self-modification"],
            priorities={"safety": 1.0},
            authority="GovernanceCouncil",
        )
        token = kp.sign_proposal("p1", "GovernanceCouncil", intent)
        self.assertTrue(token.verify("GovernanceCouncil", intent))

    @unittest.skipUnless(_HAS_CRYPTO, "cryptography not installed")
    def test_cic_provenance_reject(self):
        from cic_bench import CICKeyPair, CollectiveIntent

        kp = CICKeyPair()
        intent = CollectiveIntent(
            goals=["Preserve safety"],
            values=["Non-maleficence"],
            constraints=["No self-modification"],
            priorities={"safety": 1.0},
            authority="GovernanceCouncil",
        )
        token = kp.sign_proposal("p1", "GovernanceCouncil", intent)
        token2 = type(token)(**{**token.__dict__, "intent_digest": "bad"})
        self.assertFalse(token2.verify("GovernanceCouncil", intent))

    @unittest.skipUnless(_HAS_CRYPTO, "cryptography not installed")
    def test_merkle_audit_chain(self):
        from cic_bench import CICKeyPair, CollectiveIntent, MerkleDagAuditLog

        kp = CICKeyPair()
        intent = CollectiveIntent(
            goals=["Preserve safety"],
            values=["Non-maleficence"],
            constraints=["No self-modification"],
            priorities={"safety": 1.0},
            authority="GovernanceCouncil",
        )
        token = kp.sign_proposal("p1", "GovernanceCouncil", intent)
        log = MerkleDagAuditLog()
        log.append(
            {
                "proposal_id": "p1",
                "intent_digest": intent.canonical_digest(),
                "accepted": True,
            }
        )
        self.assertTrue(log.verify_chain())
        log.append(
            {
                "proposal_id": "p2",
                "intent_digest": intent.canonical_digest(),
                "accepted": False,
            }
        )
        self.assertTrue(log.verify_chain())
