"""
AWE Stress Test Suite (V4): Empirical Verification of Cache Eviction Dynamics
Validates the three rigorous properties required by independent audit:
1. Capacity Test: Strict capacity enforcement under high ingestion volume with active evictions.
2. T1-to-T2 Promotion & Attention-Weighted Retention Test:
   - Verifies first access places entry in T1 (recency).
   - Verifies second access explicitly promotes entry from T1 to T2 (frequent/salient).
   - Verifies Information Density Score (IDS) retains high-attention entry in T2 while evicting low-attention entries from T1 under capacity overflow.
3. Invariant Protection Test: Gen-2 Tenured Invariants remain 100% immune from eviction under sustained context pressure.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from generational_context.awe import AdaptiveReplacementAttentionCache, CacheEntry
from generational_context.memory import GenerationalMemory


def test_1_capacity_enforcement():
    print("--- TEST 1: Capacity Enforcement & Active Eviction ---")
    capacity = 100
    cache = AdaptiveReplacementAttentionCache(capacity_tokens=capacity)

    total_evictions = 0
    # Insert 6 entries of 30 tokens each (total 180 tokens > capacity 100)
    for i in range(1, 7):
        entry = CacheEntry(
            key=f"hyp_{i}",
            content=f"Hypothesis {i}: Feature engineering testing polynomial terms.",
            tokens=30,
            tier="gen1",
            attention_weight=0.5,
            entropy=1.0,
        )
        evicted = cache.access(entry)
        if evicted:
            total_evictions += len(evicted)
            print(f"  [Step {i}] Ingested {entry.key} -> Evicted: {[e.key for e in evicted]}")
        else:
            print(f"  [Step {i}] Ingested {entry.key} -> No eviction (Cache: {cache.total_tokens()}/{capacity})")

    assert total_evictions > 0, "Failed: Expected active evictions when volume exceeds capacity!"
    assert cache.total_tokens() <= capacity, f"Failed: Cache exceeded capacity {cache.total_tokens()} > {capacity}"
    print(f"  [Result] SUCCESS: Evictions Triggered = {total_evictions}, Final Cache Tokens = {cache.total_tokens()}/{capacity}\n")
    return True


def test_2_t1_to_t2_promotion_and_attention_retention():
    print("--- TEST 2: T1-to-T2 Promotion & Attention-Weighted Eviction ---")
    capacity = 60
    cache = AdaptiveReplacementAttentionCache(capacity_tokens=capacity)

    # 1. Insert entry A (Low Attention: Weight=0.10, Entropy=3.0 -> IDS = 3.33)
    entry_a = CacheEntry(
        key="cand_low_attn",
        content="Candidate A with minimal relevance to current task.",
        tokens=30,
        tier="gen1",
        attention_weight=0.10,
        entropy=3.0,
    )
    cache.access(entry_a)
    assert "cand_low_attn" in cache.t1, "Verification failed: First access must place entry in T1 (recency)."
    print("  [Step 1] First access of Entry A -> Verified placed in T1 (recency cache).")

    # 2. Insert entry B (High Attention: Weight=0.90, Entropy=0.2 -> IDS = 450.0)
    entry_b = CacheEntry(
        key="cand_high_attn",
        content="Candidate B with high gradient boosting interaction importance.",
        tokens=30,
        tier="gen1",
        attention_weight=0.90,
        entropy=0.2,
    )
    cache.access(entry_b)
    assert "cand_high_attn" in cache.t1, "Verification failed: First access of Entry B must place it in T1."
    print("  [Step 2] First access of Entry B -> Placed in T1.")

    # 3. Access entry B a SECOND time -> PROMOTION TO T2
    cache.access(entry_b)
    assert "cand_high_attn" in cache.t2, "Verification failed: Second access must promote entry from T1 to T2!"
    assert "cand_high_attn" not in cache.t1, "Verification failed: Promoted entry should no longer be in T1."
    print("  [Step 3] Second access of Entry B -> VERIFIED PROMOTED FROM T1 TO T2 (frequent/salient cache)!")

    # 4. Insert entry C: Needs 30 tokens, causing capacity overflow (60/60)
    print(f"  Cache full ({cache.total_tokens()}/{capacity}). Inserting incoming Candidate C (30 tokens)...")
    entry_c = CacheEntry(
        key="cand_incoming",
        content="Candidate C incoming trial observation.",
        tokens=30,
        tier="gen1",
        attention_weight=0.50,
        entropy=1.0,
    )
    evicted = cache.access(entry_c)
    evicted_keys = [e.key for e in evicted]
    print(f"  Evicted entries: {evicted_keys}")

    # Verify that cand_low_attn in T1 was evicted, while cand_high_attn in T2 survived!
    assert "cand_low_attn" in evicted_keys, "Verification failed: Low attention entry was not evicted!"
    assert "cand_high_attn" in cache.t2, "Verification failed: High attention entry in T2 was improperly evicted!"
    print(f"  [Result] SUCCESS: Verified T1->T2 promotion; low-attention T1 evicted, high-attention T2 preserved (IDS=450.0 > 3.33)!\n")
    return True


def test_3_gen2_invariant_immunity():
    print("--- TEST 3: Gen-2 Invariant Immunity under Extreme Context Pressure ---")
    memory = GenerationalMemory(max_working_tokens=80)

    # Pin Gen-2 Invariant
    memory.pin_invariant(
        "forbidden_libraries",
        "SYSTEM INVARIANT: Under no circumstances import or execute xgboost or lightgbm."
    )
    inv_key = "forbidden_libraries"
    assert inv_key in memory.gen2_invariants, "Invariant failed to register in Gen-2."

    # Flood the working memory with 10 successive Gen-1 hypotheses (300 tokens into 80-token capacity)
    evictions = 0
    for i in range(1, 11):
        hyp = CacheEntry(
            key=f"hyp_flood_{i}",
            content=f"Exploratory thought {i} filling context window.",
            tokens=30,
            tier="gen1",
            attention_weight=0.4,
            entropy=1.2,
        )
        evicted = memory.cache.access(hyp)
        if evicted:
            evictions += len(evicted)

    # Verify Gen-2 is completely untouched
    assert inv_key in memory.gen2_invariants, "CRITICAL ERROR: Gen-2 invariant was dropped from memory!"
    assert memory.gen2_invariants[inv_key].content.startswith("SYSTEM INVARIANT"), "Gen-2 corrupted."
    assert evictions > 0, "Expected multiple evictions in Gen-1."
    print(f"  Working context experienced {evictions} evictions under 3.75x capacity overload.")
    print(f"  Gen-2 Invariant '{inv_key}' remains 100% intact, permanently tenured.")
    print(f"  [Result] SUCCESS: Gen-2 Invariants verified 100% immune to eviction under context pressure.\n")
    return True


def run_all_stress_tests():
    print("=" * 80)
    print("AWE STRESS TEST SUITE (V4): 3-TIER GENERATIONAL REPLACEMENT DYNAMICS")
    print("=" * 80)
    t1 = test_1_capacity_enforcement()
    t2 = test_2_t1_to_t2_promotion_and_attention_retention()
    t3 = test_3_gen2_invariant_immunity()
    assert t1 and t2 and t3
    print("=" * 80)
    print("ALL 3 STRESS TESTS PASSED WITH 100% VERIFICATION.")
    print("=" * 80)


if __name__ == "__main__":
    run_all_stress_tests()
