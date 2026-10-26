"""
Attention-Weighted Eviction (AWE) Algorithm
Adaptive Replacement Cache (ARC) for LLM Attention Memory
"""

import math
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple, Set


@dataclass
class CacheEntry:
    key: str
    content: str
    tokens: int
    tier: str  # 'gen0', 'gen1', 'gen2'
    attention_weight: float = 0.0
    entropy: float = 0.0
    access_count: int = 1
    envelope_tokens: int = 0  # Structural delimiters, role tags, and framing metadata

    @property
    def effective_tokens(self) -> int:
        """Total token footprint including content payload and structural formatting/envelope tokens."""
        return self.tokens + self.envelope_tokens

    @property
    def information_density(self) -> float:
        """
        Information Density Score (IDS):
        IDS = (AttentionWeight * 100.0) / (Entropy + 1e-4)
        If unmeasured (both weight and entropy are 0.0), provides a neutral
        tier-based initialization prior so new entries are not tied at 0.0.
        """
        if self.attention_weight == 0.0 and self.entropy == 0.0:
            tier_priors = {"gen2": 50.0, "gen1": 20.0, "gen0": 5.0}
            return tier_priors.get(self.tier, 10.0)
        return (self.attention_weight * 100.0) / (self.entropy + 1e-4)


class AdaptiveReplacementAttentionCache:
    """
    AWE (Attention-Weighted Eviction) Cache Engine.
    Adapts Megiddo & Modha's Adaptive Replacement Cache (ARC) to Transformer
    Context Buffers by dynamically balancing between:
      T1: Recent tool outputs and working notes (Recency)
      T2: High-attention architectural rules and verified state (Frequency / Saliency)
    With ghost registries B1 and B2 for dynamic boundary parameter p.

    Guarantees strict post-condition: total_tokens() <= capacity_tokens,
    encompassing payload tokens, framing delimiters, and metadata headers.
    """

    def __init__(self, capacity_tokens: int = 4000, fixed_envelope_overhead: int = 0):
        if capacity_tokens <= 0:
            raise ValueError(f"capacity_tokens must be positive, got {capacity_tokens}")
        self.c = capacity_tokens  # Target max token capacity
        self.fixed_envelope_overhead = (
            fixed_envelope_overhead  # Delimiters, headers, metadata
        )
        self.p = 0.0  # Adaptation parameter: target size of T1 in tokens

        # Active Caches
        self.t1: Dict[str, CacheEntry] = {}  # Recency cache
        self.t2: Dict[str, CacheEntry] = {}  # Frequency / High-Attention cache

        # Ghost Registries (Store keys and token counts, not payloads)
        self.b1: Dict[str, int] = {}  # History of evicted from T1
        self.b2: Dict[str, int] = {}  # History of evicted from T2

        # Indexes for faster lookups
        self._key_to_tier: Dict[str, str] = {}  # key -> 't1' or 't2'
        self._by_key: Dict[str, CacheEntry] = {}  # key -> entry (active)

    def total_tokens(self) -> int:
        base = sum(e.effective_tokens for e in self.t1.values()) + sum(
            e.effective_tokens for e in self.t2.values()
        )
        return base + (self.fixed_envelope_overhead if (self.t1 or self.t2) else 0)

    def _t1_tokens(self) -> int:
        return sum(e.effective_tokens for e in self.t1.values())

    def _t2_tokens(self) -> int:
        return sum(e.effective_tokens for e in self.t2.values())

    def _sync_indexes(self):
        self._key_to_tier = {}
        self._by_key = {}
        for k, v in self.t1.items():
            self._key_to_tier[k] = "t1"
            self._by_key[k] = v
        for k, v in self.t2.items():
            self._key_to_tier[k] = "t2"
            self._by_key[k] = v

    def get_entry(self, key: str) -> Optional[CacheEntry]:
        if key in self.t1:
            return self.t1[key]
        if key in self.t2:
            return self.t2[key]
        return None

    def evict_by_key(self, key: str) -> Optional[CacheEntry]:
        if key in self.t1:
            entry = self.t1.pop(key)
            self.b1[key] = entry.effective_tokens
            self._sync_indexes()
            return entry
        if key in self.t2:
            entry = self.t2.pop(key)
            self.b2[key] = entry.effective_tokens
            self._sync_indexes()
            return entry
        return None

    def record_attention(self, key: str, attention_weight: float, entropy: float):
        """Update empirical attention weights calculated from transformer forward pass."""
        if key in self.t1:
            self.t1[key].attention_weight = attention_weight
            self.t1[key].entropy = entropy
        elif key in self.t2:
            self.t2[key].attention_weight = attention_weight
            self.t2[key].entropy = entropy

    def access(self, entry: CacheEntry) -> List[CacheEntry]:
        """
        Accesses an entry. If cache overflows, runs adaptive eviction
        and returns list of evicted entries.
        Guarantees: total_tokens() <= self.c after execution.
        """
        evicted = []
        key = entry.key

        # Guard against single entry exceeding total cache capacity
        if entry.effective_tokens > self.c:
            target_payload_tokens = max(0, self.c - entry.envelope_tokens)
            words = entry.content.split()
            if len(words) > target_payload_tokens:
                entry.content = " ".join(words[:target_payload_tokens]) + " [TRUNCATED]"
            entry.tokens = target_payload_tokens

        # Case 1: Hit in T1 or T2 -> Promote to T2 (Frequent/Tenured)
        if key in self.t1:
            hit = self.t1.pop(key)
            hit.access_count += 1
            hit.tier = "gen1"
            hit.content = entry.content
            hit.tokens = entry.tokens
            hit.envelope_tokens = entry.envelope_tokens
            evicted.extend(self._replace(hit))
            self.t2[key] = hit
            self._prune_ghost_registries()
            self._sync_indexes()
            assert self.total_tokens() <= self.c, (
                f"Invariant violated: {self.total_tokens()} > {self.c}"
            )
            return evicted

        if key in self.t2:
            self.t2[key].access_count += 1
            old_eff = self.t2[key].effective_tokens
            new_eff = entry.effective_tokens
            diff = new_eff - old_eff
            self.t2[key].content = entry.content
            self.t2[key].tokens = entry.tokens
            self.t2[key].envelope_tokens = entry.envelope_tokens
            if diff > 0:
                # Evict others first; do not evict the entry we just updated
                evicted.extend(
                    self._replace_other_than(key, incoming_eff=entry.effective_tokens)
                )
            self._prune_ghost_registries()
            self._sync_indexes()
            assert self.total_tokens() <= self.c, (
                f"Invariant violated: {self.total_tokens()} > {self.c}"
            )
            return evicted

        # Ghost list token calculations for consistent ratio
        b1_tokens = sum(self.b1.values())
        b2_tokens = sum(self.b2.values())

        # Case 2: Hit in B1 (Recently evicted from T1) -> Increase p (favor recency)
        if key in self.b1:
            delta = (
                1.0
                if b1_tokens >= b2_tokens
                else float(b2_tokens) / max(float(b1_tokens), 1.0)
            )
            self.p = min(float(self.c), self.p + (delta * entry.effective_tokens))
            del self.b1[key]
            evicted.extend(self._replace(entry))
            self.t2[key] = entry
            self._prune_ghost_registries()
            self._sync_indexes()
            assert self.total_tokens() <= self.c, (
                f"Invariant violated: {self.total_tokens()} > {self.c}"
            )
            return evicted

        # Case 3: Hit in B2 (Recently evicted from T2) -> Decrease p (favor frequency/saliency)
        if key in self.b2:
            delta = (
                1.0
                if b2_tokens >= b1_tokens
                else float(b1_tokens) / max(float(b2_tokens), 1.0)
            )
            self.p = max(0.0, self.p - (delta * entry.effective_tokens))
            del self.b2[key]
            evicted.extend(self._replace(entry))
            self.t2[key] = entry
            self._prune_ghost_registries()
            self._sync_indexes()
            assert self.total_tokens() <= self.c, (
                f"Invariant violated: {self.total_tokens()} > {self.c}"
            )
            return evicted

        # Case 4: Complete Cache Miss -> Insert into T1 (Recency)
        evicted.extend(self._replace(entry))
        self.t1[key] = entry
        self._prune_ghost_registries()
        self._sync_indexes()
        assert self.total_tokens() <= self.c, (
            f"Invariant violated: {self.total_tokens()} > {self.c}"
        )
        return evicted

    def _replace_other_than(
        self, exclude_key: str, incoming_eff: int
    ) -> List[CacheEntry]:
        """Evicts entries with lowest Information Density Score (IDS) until
        (current_total + incoming_eff) fits, never evicting exclude_key."""
        evicted = []
        while (self.total_tokens() + incoming_eff) > self.c and (self.t1 or self.t2):
            t1_size = self._t1_tokens()
            # Prefer T1 eviction based on p if possible
            if t1_size > 0 and (
                t1_size > self.p or (exclude_key in self.b2 and t1_size >= self.p)
            ):
                candidates = [k for k in self.t1.keys() if k != exclude_key]
                if candidates:
                    # Use index on IDS - compute min efficiently
                    victim_key = min(
                        candidates, key=lambda k: self.t1[k].information_density
                    )
                    victim = self.t1.pop(victim_key)
                    self.b1[victim_key] = victim.effective_tokens
                    evicted.append(victim)
                    continue
            if self.t2:
                candidates = [k for k in self.t2.keys() if k != exclude_key]
                if candidates:
                    victim_key = min(
                        candidates, key=lambda k: self.t2[k].information_density
                    )
                    victim = self.t2.pop(victim_key)
                    self.b2[victim_key] = victim.effective_tokens
                    evicted.append(victim)
                    continue
            if self.t1:
                candidates = [k for k in self.t1.keys() if k != exclude_key]
                if candidates:
                    victim_key = min(
                        candidates, key=lambda k: self.t1[k].information_density
                    )
                    victim = self.t1.pop(victim_key)
                    self.b1[victim_key] = victim.effective_tokens
                    evicted.append(victim)
                    continue
            break
        self._sync_indexes()
        return evicted

    def _replace(self, incoming: CacheEntry) -> List[CacheEntry]:
        """Evicts entries with lowest Information Density Score (IDS) until incoming fits."""
        evicted = []
        while (self.total_tokens() + incoming.effective_tokens) > self.c and (
            self.t1 or self.t2
        ):
            t1_size = self._t1_tokens()
            # If T1 is larger than target boundary p, evict lowest IDS from T1
            if t1_size > 0 and (
                t1_size > self.p or (incoming.key in self.b2 and t1_size >= self.p)
            ):
                victim_key = min(
                    self.t1.keys(), key=lambda k: self.t1[k].information_density
                )
                victim = self.t1.pop(victim_key)
                self.b1[victim_key] = victim.effective_tokens
                evicted.append(victim)
            elif self.t2:
                victim_key = min(
                    self.t2.keys(), key=lambda k: self.t2[k].information_density
                )
                victim = self.t2.pop(victim_key)
                self.b2[victim_key] = victim.effective_tokens
                evicted.append(victim)
            elif self.t1:
                victim_key = min(
                    self.t1.keys(), key=lambda k: self.t1[k].information_density
                )
                victim = self.t1.pop(victim_key)
                self.b1[victim_key] = victim.effective_tokens
                evicted.append(victim)
            else:
                break
        self._sync_indexes()
        return evicted

    def _prune_ghost_registries(self):
        """Bounds ghost registries to prevent unbounded memory growth."""
        while sum(self.b1.values()) > self.c and self.b1:
            first_key = next(iter(self.b1))
            del self.b1[first_key]
        while sum(self.b2.values()) > self.c and self.b2:
            first_key = next(iter(self.b2))
            del self.b2[first_key]
        self._sync_indexes()

    def get_active_entries(self) -> List[CacheEntry]:
        """Returns all entries currently in active attention memory."""
        self._sync_indexes()
        return list(self.t1.values()) + list(self.t2.values())
