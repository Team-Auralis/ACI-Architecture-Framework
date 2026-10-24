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

    @property
    def information_density(self) -> float:
        """
        Information Density Score (IDS):
        IDS = AttentionWeight / (Entropy + 1e-6)
        High attention with low entropy = high density (keep in cache).
        Low attention with high entropy = low density / pure noise (evict first).
        """
        return (self.attention_weight * 100.0) / (self.entropy + 1e-4)


class AdaptiveReplacementAttentionCache:
    """
    AWE (Attention-Weighted Eviction) Cache Engine.
    Adapts Megiddo & Modha's Adaptive Replacement Cache (ARC) to Transformer
    Context Buffers by dynamically balancing between:
      T1: Recent tool outputs and working notes (Recency)
      T2: High-attention architectural rules and verified state (Frequency / Saliency)
    With ghost registries B1 and B2 for dynamic boundary parameter p.
    """
    def __init__(self, capacity_tokens: int = 4000):
        self.c = capacity_tokens  # Target max token capacity
        self.p = 0.0  # Adaptation parameter: target size of T1 in tokens

        # Active Caches
        self.t1: Dict[str, CacheEntry] = {}  # Recency cache
        self.t2: Dict[str, CacheEntry] = {}  # Frequency / High-Attention cache

        # Ghost Registries (Store keys and token counts, not payloads)
        self.b1: Dict[str, int] = {}  # History of evicted from T1
        self.b2: Dict[str, int] = {}  # History of evicted from T2

    def total_tokens(self) -> int:
        return sum(e.tokens for e in self.t1.values()) + sum(e.tokens for e in self.t2.values())

    def _t1_tokens(self) -> int:
        return sum(e.tokens for e in self.t1.values())

    def _t2_tokens(self) -> int:
        return sum(e.tokens for e in self.t2.values())

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
        """
        evicted = []
        key = entry.key

        # Case 1: Hit in T1 or T2 -> Promote to T2 (Frequent/Tenured)
        if key in self.t1:
            hit = self.t1.pop(key)
            hit.access_count += 1
            hit.tier = 'gen1'
            self.t2[key] = hit
            return evicted

        if key in self.t2:
            self.t2[key].access_count += 1
            return evicted

        # Case 2: Hit in B1 (Recently evicted from T1) -> Increase p (favor recency)
        if key in self.b1:
            delta = 1.0 if len(self.b1) >= len(self.b2) else len(self.b2) / max(len(self.b1), 1)
            self.p = min(float(self.c), self.p + (delta * entry.tokens))
            del self.b1[key]
            evicted.extend(self._replace(entry))
            self.t2[key] = entry
            return evicted

        # Case 3: Hit in B2 (Recently evicted from T2) -> Decrease p (favor frequency/saliency)
        if key in self.b2:
            delta = 1.0 if len(self.b2) >= len(self.b1) else len(self.b1) / max(len(self.b2), 1)
            self.p = max(0.0, self.p - (delta * entry.tokens))
            del self.b2[key]
            evicted.extend(self._replace(entry))
            self.t2[key] = entry
            return evicted

        # Case 4: Complete Cache Miss
        evicted.extend(self._replace(entry))
        self.t1[key] = entry
        return evicted

    def _replace(self, incoming: CacheEntry) -> List[CacheEntry]:
        """Evicts entries with lowest Information Density Score (IDS) until capacity fits."""
        evicted = []
        while (self.total_tokens() + incoming.tokens) > self.c:
            t1_size = self._t1_tokens()
            # If T1 is larger than target boundary p, evict lowest IDS from T1
            if t1_size > 0 and (t1_size > self.p or (incoming.key in self.b2 and t1_size >= self.p)):
                victim_key = min(self.t1.keys(), key=lambda k: self.t1[k].information_density)
                victim = self.t1.pop(victim_key)
                self.b1[victim_key] = victim.tokens
                evicted.append(victim)
            else:
                if not self.t2:
                    if self.t1:
                        victim_key = min(self.t1.keys(), key=lambda k: self.t1[k].information_density)
                        victim = self.t1.pop(victim_key)
                        self.b1[victim_key] = victim.tokens
                        evicted.append(victim)
                    break
                victim_key = min(self.t2.keys(), key=lambda k: self.t2[k].information_density)
                victim = self.t2.pop(victim_key)
                self.b2[victim_key] = victim.tokens
                evicted.append(victim)
        return evicted

    def get_active_entries(self) -> List[CacheEntry]:
        """Returns all entries currently in active attention memory."""
        return list(self.t1.values()) + list(self.t2.values())
