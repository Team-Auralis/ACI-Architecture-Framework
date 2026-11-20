"""
V3 Statistical Aggregator for Neural ERA Benchmark
Reads directly from experiments/v3_raw_execution_traces.jsonl.
Separates real physical measurements from policy enforcement penalties.
Reports active in vivo AWE cache eviction counts, token compression statistics, and GPU attention retention.
"""

from __future__ import annotations

import json
import os
import sys
from collections import defaultdict

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
traces_path = os.path.join(REPO_ROOT, "experiments", "v3_raw_execution_traces.jsonl")

if not os.path.exists(traces_path):
    print(f"Error: {traces_path} does not exist. Run benchmarks/v3_live_neural_era_benchmark.py first.")
    sys.exit(1)

with open(traces_path, "r", encoding="utf-8") as f:
    lines = [json.loads(line) for line in f if line.strip()]

by_seed_cond = defaultdict(list)
for record in lines:
    by_seed_cond[(record["seed"], record["condition"])].append(record)

conditions = [
    "Standard_Google_ERA",
    "Ablation_Gen2_Only",
    "Ablation_Gen0_Only",
    "Full_ACI",
]

seeds = sorted(list(set(r["seed"] for r in lines)))
complete_seeds = [
    s for s in seeds if all(len(by_seed_cond[(s, c)]) == 6 for c in conditions)
]

print(f"Total valid V3 raw records: {len(lines)}")
print(f"Completed seeds: {complete_seeds} ({len(complete_seeds)} seeds)")

summary = {
    "benchmark_version": "v3_live_neural_era_benchmark",
    "model": "GPT-2 (PyTorch CausalLM, GPU CUDA, output_attentions=True)",
    "tokenizer": "tiktoken (cl100k_base)",
    "total_records": len(lines),
    "completed_seeds": complete_seeds,
    "num_seeds": len(complete_seeds),
    "steps_per_seed": 6,
    "conditions": {},
    "statistical_tests": {},
}

for c in conditions:
    seed_final_tokens = []
    seed_mean_tokens = []
    seed_best_rmses = []
    seed_violations = []
    seed_inv_attentions = []
    seed_inv_entropies = []
    seed_awe_evictions = []
    seed_measured_rmses = []

    for s in complete_seeds:
        steps = by_seed_cond[(s, c)]
        toks = [step["prompt_bpe_tokens"] for step in steps]
        seed_final_tokens.append(toks[-1])
        seed_mean_tokens.append(float(np.mean(toks)))

        # Actual measured RMSEs (excluding None)
        valid_rmses = [
            step["actual_measured_rmse"]
            for step in steps
            if step["actual_measured_rmse"] is not None and step["is_invariant_compliant"]
        ]
        if valid_rmses:
            seed_best_rmses.append(float(min(valid_rmses)))
            seed_measured_rmses.extend(valid_rmses)
        else:
            seed_best_rmses.append(0.7280)

        v_count = sum(1 for step in steps if not step["is_invariant_compliant"])
        seed_violations.append(v_count)

        attns = [step["measured_inv_attention"] for step in steps if step["measured_inv_attention"] > 0]
        if attns:
            seed_inv_attentions.append(float(np.mean(attns)))

        entropies = [step["measured_inv_entropy"] for step in steps if step["measured_inv_entropy"] > 0]
        if entropies:
            seed_inv_entropies.append(float(np.mean(entropies)))

        evictions = sum(len(step.get("awe_evicted_keys", [])) for step in steps)
        seed_awe_evictions.append(evictions)

    summary["conditions"][c] = {
        "mean_best_rmse": float(np.mean(seed_best_rmses)),
        "std_best_rmse": float(np.std(seed_best_rmses, ddof=1)) if len(seed_best_rmses) > 1 else 0.0,
        "all_best_rmses": seed_best_rmses,
        "total_violations": int(sum(seed_violations)),
        "violation_rate": float(sum(seed_violations) / (len(complete_seeds) * 6)),
        "seed_violations": seed_violations,
        "mean_final_bpe_tokens": float(np.mean(seed_final_tokens)),
        "std_final_bpe_tokens": float(np.std(seed_final_tokens, ddof=1)),
        "all_final_bpe_tokens": seed_final_tokens,
        "mean_average_bpe_tokens": float(np.mean(seed_mean_tokens)),
        "mean_invariant_attention": float(np.mean(seed_inv_attentions)) if seed_inv_attentions else 0.0,
        "mean_attention_entropy": float(np.mean(seed_inv_entropies)) if seed_inv_entropies else 0.0,
        "total_awe_evictions": int(sum(seed_awe_evictions)),
        "mean_measured_rmse": float(np.mean(seed_measured_rmses)) if seed_measured_rmses else 0.7280,
    }

std_data = summary["conditions"]["Standard_Google_ERA"]
aci_data = summary["conditions"]["Full_ACI"]

# 1. Paired Student's t-test on prompt tokens across seeds
t_stat_tok, p_val_tok = stats.ttest_rel(
    std_data["all_final_bpe_tokens"], aci_data["all_final_bpe_tokens"]
)
wilcoxon_tok = stats.wilcoxon(
    std_data["all_final_bpe_tokens"], aci_data["all_final_bpe_tokens"]
)

token_reduct = (
    (std_data["mean_final_bpe_tokens"] - aci_data["mean_final_bpe_tokens"])
    / std_data["mean_final_bpe_tokens"]
) * 100.0

# 2. Welch's t-test on best RMSE
t_stat_rmse, p_val_rmse = stats.ttest_ind(
    aci_data["all_best_rmses"], std_data["all_best_rmses"], equal_var=False
)
paired_t_rmse, paired_p_rmse = stats.ttest_rel(
    std_data["all_best_rmses"], aci_data["all_best_rmses"]
)

# 3. Fisher's exact test on violations
total_steps = len(complete_seeds) * 6
table = [
    [aci_data["total_violations"], total_steps - aci_data["total_violations"]],
    [std_data["total_violations"], total_steps - std_data["total_violations"]],
]
odds, p_val_fisher = stats.fisher_exact(table)

summary["statistical_tests"] = {
    "token_reduction_percentage": float(token_reduct),
    "token_paired_t_statistic": float(t_stat_tok),
    "token_paired_p_value": float(p_val_tok),
    "token_wilcoxon_statistic": float(wilcoxon_tok.statistic),
    "token_wilcoxon_p_value": float(wilcoxon_tok.pvalue),
    "token_statistically_significant": bool(p_val_tok < 0.001),
    "rmse_welch_t_statistic": float(t_stat_rmse) if not np.isnan(t_stat_rmse) else 0.0,
    "rmse_welch_p_value": float(p_val_rmse) if not np.isnan(p_val_rmse) else 1.0,
    "rmse_paired_t_statistic": float(paired_t_rmse) if not np.isnan(paired_t_rmse) else 0.0,
    "rmse_paired_p_value": float(paired_p_rmse) if not np.isnan(paired_p_rmse) else 1.0,
    "fisher_exact_odds_ratio": float(odds) if not np.isinf(odds) else 999.0,
    "fisher_exact_p_value_violations": float(p_val_fisher),
    "total_in_vivo_awe_evictions": aci_data["total_awe_evictions"],
}

out_json_path = os.path.join(REPO_ROOT, "experiments", "v3_neural_era_results.json")
with open(out_json_path, "w", encoding="utf-8") as f:
    json.dump(summary, f, indent=2)

print("\n" + "=" * 80)
print("V3 STATISTICAL RESULTS:")
print(f"Token Reduction: {token_reduct:.2f}% (Paired t = {t_stat_tok:.3f}, p = {p_val_tok:.2e})")
print(f"AWE Evictions Triggered in Vivo: {aci_data['total_awe_evictions']}")
print(f"Best RMSE: Standard={std_data['mean_best_rmse']:.4f} vs ACI={aci_data['mean_best_rmse']:.4f}")
print(f"Live Invariant Attention: Standard={std_data['mean_invariant_attention']:.4f} vs ACI={aci_data['mean_invariant_attention']:.4f}")
print(f"Exported JSON to: {out_json_path}")
print("=" * 80)

# Generate 4-panel publication-grade figure
fig, axes = plt.subplots(1, 4, figsize=(22, 5.2))
colors = ["#e74c3c", "#f39c12", "#3498db", "#2ecc71"]
short_labels = ["Standard ERA", "Gen-2 Only", "Gen-0 Only", "Full ACI"]

# Panel 1: Context Footprint
toks = [summary["conditions"][c]["mean_final_bpe_tokens"] for c in conditions]
errs = [summary["conditions"][c]["std_final_bpe_tokens"] for c in conditions]
bars1 = axes[0].bar(short_labels, toks, yerr=errs, color=colors, capsize=5, edgecolor="black", alpha=0.88, width=0.55)
axes[0].set_ylabel("Final Prompt BPE Tokens", fontsize=11, fontweight="bold")
axes[0].set_title(f"A. Context Footprint (-{token_reduct:.1f}%, p={p_val_tok:.1e})", fontsize=12, fontweight="bold")
axes[0].grid(axis="y", linestyle="--", alpha=0.4)
for b in bars1:
    h = b.get_height()
    axes[0].annotate(f"{int(h)}", xy=(b.get_x() + b.get_width() / 2, h), xytext=(0, 4),
                     textcoords="offset points", ha="center", va="bottom", fontweight="bold")

# Panel 2: Live Invariant Attention
attns = [summary["conditions"][c]["mean_invariant_attention"] for c in conditions]
bars2 = axes[1].bar(short_labels, attns, color=colors, edgecolor="black", alpha=0.88, width=0.55)
axes[1].set_ylabel("Attention Mass (alpha_inv)", fontsize=11, fontweight="bold")
axes[1].set_title("B. Live Invariant Attention (GPU)", fontsize=12, fontweight="bold")
axes[1].grid(axis="y", linestyle="--", alpha=0.4)
for b in bars2:
    h = b.get_height()
    axes[1].annotate(f"{h:.3f}", xy=(b.get_x() + b.get_width() / 2, h), xytext=(0, 3),
                     textcoords="offset points", ha="center", va="bottom", fontweight="bold")

# Panel 3: In Vivo AWE Evictions
evicts = [summary["conditions"][c]["total_awe_evictions"] for c in conditions]
bars3 = axes[2].bar(short_labels, evicts, color=colors, edgecolor="black", alpha=0.88, width=0.55)
axes[2].set_ylabel("AWE Evictions Triggered (N=48 steps)", fontsize=11, fontweight="bold")
axes[2].set_title(f"C. Active AWE Evictions ({aci_data['total_awe_evictions']} total)", fontsize=12, fontweight="bold")
axes[2].grid(axis="y", linestyle="--", alpha=0.4)
for b in bars3:
    h = b.get_height()
    axes[2].annotate(f"{int(h)}", xy=(b.get_x() + b.get_width() / 2, h), xytext=(0, 3),
                     textcoords="offset points", ha="center", va="bottom", fontweight="bold")

# Panel 4: Best Measured RMSE
rmses = [summary["conditions"][c]["mean_best_rmse"] for c in conditions]
bars4 = axes[3].bar(short_labels, rmses, color=colors, edgecolor="black", alpha=0.88, width=0.55)
axes[3].set_ylabel("Best Validation RMSE", fontsize=11, fontweight="bold")
axes[3].set_ylim(0.60, 0.70)
axes[3].set_title(f"D. Search Convergence (p={p_val_rmse:.3f})", fontsize=12, fontweight="bold")
axes[3].grid(axis="y", linestyle="--", alpha=0.4)
for b in bars4:
    h = b.get_height()
    axes[3].annotate(f"{h:.4f}", xy=(b.get_x() + b.get_width() / 2, h), xytext=(0, 3),
                     textcoords="offset points", ha="center", va="bottom", fontweight="bold")

plt.tight_layout()
fig_path = os.path.join(REPO_ROOT, "docs", "assets", "v3_ablation_matrix.png")
os.makedirs(os.path.dirname(fig_path), exist_ok=True)
plt.savefig(fig_path, dpi=300)
plt.close()
print(f"Saved figure to: {fig_path}")
