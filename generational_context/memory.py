"""
Generational Memory Architecture
3-Tier Context Lifecycle: Gen-0 Ephemeral, Gen-1 Evaporative, Gen-2 Tenured
"""

from dataclasses import dataclass, field
import hashlib
import math
import re
from typing import List, Dict, Optional, Tuple, Any

from .awe import AdaptiveReplacementAttentionCache, CacheEntry


def hash_embed(text: str, dim: int = 128) -> List[float]:
    """Subword n-gram embedding projection (FastText style, standard library)."""
    words = re.findall(r'[a-zA-Z0-9_\.]+', text.lower())
    if not words:
        return [0.0] * dim

    vec = [0.0] * dim
    for w in words:
        tokens = [w]
        if len(w) >= 3:
            tokens.extend(w[i:i+3] for i in range(len(w) - 2))

        for t in tokens:
            h = int(hashlib.sha256(t.encode('utf-8')).hexdigest()[:8], 16)
            idx = h % dim
            sign = 1.0 if ((h >> 16) & 1) else -1.0
            vec[idx] += sign

    mag = math.sqrt(sum(v * v for v in vec)) or 1e-12
    return [v / mag for v in vec]


def cosine_sim(v1: List[float], v2: List[float]) -> float:
    dot = sum(a * b for a, b in zip(v1, v2))
    n1 = math.sqrt(sum(a * a for a in v1)) or 1e-12
    n2 = math.sqrt(sum(b * b for b in v2)) or 1e-12
    return dot / (n1 * n2)


@dataclass
class DistilledObservation:
    command: str
    exit_code: int
    summary: str
    critical_lines: List[str]
    raw_token_count: int
    distilled_token_count: int


class GenerationalMemory:
    """
    Core memory controller enforcing Generational Context and preventing
    The Fool's Theorem by active eviction of Gen-0 and pinning of Gen-2.
    """
    def __init__(self, max_working_tokens: int = 4000, egi_threshold: float = 0.35):
        self.max_working_tokens = max_working_tokens
        self.egi_threshold = egi_threshold

        # Gen-2: Tenured Invariants (Permanently Pinned, Never Evicted)
        self.gen2_invariants: Dict[str, CacheEntry] = {}

        # AWE Cache for Gen-0 and Gen-1
        self.cache = AdaptiveReplacementAttentionCache(capacity_tokens=max_working_tokens)

        # Failure Traceback Memory for Error Gravitation Monitoring
        self.failed_tracebacks: List[str] = []
        self.diagnostic_hypotheses: List[str] = []

        # Accounting Telemetry
        self.total_raw_tokens_ingested = 0
        self.total_active_tokens_emitted = 0

    def pin_invariant(self, key: str, instruction: str):
        """Pins a Gen-2 Tenured Invariant. Protected from all eviction and compaction."""
        tokens = len(re.findall(r'\w+', instruction))
        entry = CacheEntry(
            key=key,
            content=instruction,
            tokens=tokens,
            tier='gen2',
            attention_weight=1.0,
            entropy=0.1
        )
        self.gen2_invariants[key] = entry

    def record_tool_result(
        self,
        command: str,
        stdout: str,
        stderr: str,
        exit_code: int
    ) -> DistilledObservation:
        """
        Receives raw tool execution. Mitigates Payload Inundation by extracting
        a 3-line distilled essence and evicting the raw terminal output.
        """
        raw_text = f"{stdout}\n{stderr}".strip()
        raw_tokens = len(re.findall(r'\w+', raw_text)) + len(re.findall(r'\w+', command))
        self.total_raw_tokens_ingested += raw_tokens

        # Distillation filter
        critical_lines = []
        if exit_code == 0:
            summary = f"Command `{command}` succeeded."
            lines = [l for l in stdout.strip().splitlines() if l.strip()][-2:]
            critical_lines = lines
        else:
            summary = f"Command `{command}` failed with exit code {exit_code}."
            err_lines = stderr.splitlines() or stdout.splitlines()
            signatures = [l for l in err_lines if re.search(r'(Error|Exception|FAILED|fatal):', l, re.IGNORECASE)]
            critical_lines = signatures[-3:] if signatures else err_lines[-2:]

        distilled_text = f"[{summary}]\n" + "\n".join(f"  > {l}" for l in critical_lines)
        distilled_tokens = len(re.findall(r'\w+', distilled_text))

        key = f"tool_{hashlib.sha256(command.encode('utf-8')).hexdigest()[:8]}"
        entry = CacheEntry(
            key=key,
            content=distilled_text,
            tokens=distilled_tokens,
            tier='gen0',
            attention_weight=0.5,
            entropy=1.2
        )

        # Pass through AWE Cache
        self.cache.access(entry)

        if exit_code != 0:
            self.failed_tracebacks.append(distilled_text)

        return DistilledObservation(
            command=command,
            exit_code=exit_code,
            summary=summary,
            critical_lines=critical_lines,
            raw_token_count=raw_tokens,
            distilled_token_count=distilled_tokens
        )

    def record_hypothesis(self, thought: str):
        """Records diagnostic reasoning step and checks Error Gravitation."""
        tokens = len(re.findall(r'\w+', thought))
        self.diagnostic_hypotheses.append(thought)
        key = f"hyp_{len(self.diagnostic_hypotheses)}"
        entry = CacheEntry(
            key=key,
            content=f"[Hypothesis]: {thought}",
            tokens=tokens,
            tier='gen1',
            attention_weight=0.7,
            entropy=0.8
        )
        self.cache.access(entry)

    def check_error_gravitation(self, candidate_thought: str) -> float:
        """Computes Error Gravitation Index (EGI) against past failed traces."""
        if not self.failed_tracebacks:
            return 0.0

        q_vec = hash_embed(candidate_thought)
        scores = []
        for tb in self.failed_tracebacks:
            tb_vec = hash_embed(tb)
            sim = cosine_sim(q_vec, tb_vec)
            scores.append(max(0.0, sim))

        return max(scores) if scores else 0.0

    def break_attractor_loop(self):
        """Anti-Gravitational Flush: Clears stale hypotheses from Gen-1."""
        self.diagnostic_hypotheses.clear()
        self.failed_tracebacks.clear()
        # Purge diagnostic keys from cache
        for k in list(self.cache.t1.keys()):
            if k.startswith("hyp_"):
                del self.cache.t1[k]
        for k in list(self.cache.t2.keys()):
            if k.startswith("hyp_"):
                del self.cache.t2[k]

    def compile_active_context(self) -> str:
        """
        Compiles the active prompt context conforming to Generational Context:
        [Gen-2 Tenured Invariants] + [Gen-1 Working State] + [Gen-0 Distilled Signals]
        """
        sections = []

        # 1. Gen-2 Tenured Invariants
        if self.gen2_invariants:
            sec_tenured = "=== TENURED INVARIANTS (GEN-2: PINNED) ===\n" + "\n".join(
                f"- {e.content}" for e in self.gen2_invariants.values()
            )
            sections.append(sec_tenured)

        # 2. Gen-1 and Gen-0 from AWE Cache
        active_entries = self.cache.get_active_entries()
        gen1_entries = [e for e in active_entries if e.tier == 'gen1']
        gen0_entries = [e for e in active_entries if e.tier == 'gen0']

        if gen1_entries:
            sec_gen1 = "=== ACTIVE WORKING HYPOTHESES (GEN-1) ===\n" + "\n".join(
                f"{e.content}" for e in gen1_entries[-3:]
            )
            sections.append(sec_gen1)

        if gen0_entries:
            sec_gen0 = "=== RECENT TOOL ESSENCE (GEN-0: DISTILLED) ===\n" + "\n".join(
                f"{e.content}" for e in gen0_entries[-2:]
            )
            sections.append(sec_gen0)

        compiled = "\n\n".join(sections)
        self.total_active_tokens_emitted = len(re.findall(r'\w+', compiled))
        return compiled
