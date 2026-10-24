"""
Publication-Grade Vector Plot Generator for CCB-001 Benchmark
Visualizes The Fool's Theorem Phase Transition, Error Gravitation, and Pareto Frontier.
"""

import os
import csv
import matplotlib.pyplot as plt
import matplotlib as mpl

# Publication-grade styling
mpl.rcParams['font.family'] = 'sans-serif'
mpl.rcParams['font.size'] = 11
mpl.rcParams['axes.linewidth'] = 1.2
mpl.rcParams['grid.alpha'] = 0.3
mpl.rcParams['grid.linestyle'] = '--'

OUTPUT_DIR = "E:/ACI-Architecture-Framework/docs/assets"
os.makedirs(OUTPUT_DIR, exist_ok=True)

CSV_PATH = "E:/ACI-Architecture-Framework/ccb_results.csv"


def load_telemetry():
    with open(CSV_PATH, "r", encoding="utf-8") as f:
        reader = list(csv.DictReader(f))
    return reader


def plot_phase_transition(records):
    """Figure 1: Attention on Invariant vs. Context Noise Volume (The Inundation Lemma)"""
    fig, ax = plt.subplots(figsize=(8, 5), dpi=300)

    # Filter for S1_Traceback_Inundation
    s1_recs = [r for r in records if r["scenario_id"] == "S1_Traceback_Inundation"]

    arms = {
        "Arm A: Flat Append-Only": {"color": "#e63946", "style": "o-", "label": "Arm A: Flat Append-Only"},
        "Arm B: Auto-Compaction": {"color": "#f4a261", "style": "s--", "label": "Arm B: Auto-Compaction"},
        "Arm C: Generational Context": {"color": "#2a9d8f", "style": "^-", "label": "Arm C: Generational Context"}
    }

    for arm_name, meta in arms.items():
        arm_data = [r for r in s1_recs if r["arm_name"] == arm_name]
        tokens = [int(r["active_context_tokens"]) for r in arm_data]
        attn = [float(r["attention_on_invariant"]) for r in arm_data]
        ax.plot(tokens, attn, meta["style"], color=meta["color"], label=meta["label"], linewidth=2, markersize=6)

    # Critical Phase Transition Boundary line (N* bound)
    ax.axhline(y=0.05, color="#d62828", linestyle=":", linewidth=1.5, label=r"Critical Invariant Threshold $\theta_{crit} = 0.05$")
    ax.axhspan(0, 0.05, color="#d62828", alpha=0.08, label="The Fool's Basin (Attention Collapse)")

    ax.set_title("Figure 1: The Fool's Phase Transition (Attention Decay vs. Context Volume)", fontsize=12, fontweight='bold', pad=12)
    ax.set_xlabel("Active Context Tokens (KV Cache Ingress)", fontsize=11)
    ax.set_ylabel(r"Attention Probability Mass on Invariants $A_{inv}$", fontsize=11)
    ax.grid(True)
    ax.legend(frameon=True, facecolor="white", edgecolor="#ccc", fontsize=9)
    plt.tight_layout()

    out_path = os.path.join(OUTPUT_DIR, "phase_transition_curve.svg")
    plt.savefig(out_path, format="svg")
    plt.close()
    print(f"Generated: {out_path}")


def plot_error_gravitation(records):
    """Figure 2: Error Gravitation Index (EGI) Trajectories Across Turns"""
    fig, ax = plt.subplots(figsize=(8, 5), dpi=300)

    # Filter for S2_Red_Herring_Attractor
    s2_recs = [r for r in records if r["scenario_id"] == "S2_Red_Herring_Attractor"]

    arms = {
        "Arm A: Flat Append-Only": {"color": "#e63946", "style": "o-", "label": "Arm A: Trapped in Attractor"},
        "Arm B: Auto-Compaction": {"color": "#e76f51", "style": "s--", "label": "Arm B: Trapped in Attractor"},
        "Arm C: Generational Context": {"color": "#2a9d8f", "style": "D-", "label": "Arm C: Anti-Gravitational Flush"}
    }

    for arm_name, meta in arms.items():
        arm_data = [r for r in s2_recs if r["arm_name"] == arm_name]
        turns = [int(r["turn"]) for r in arm_data]
        egi = [float(r["error_gravitation_index"]) for r in arm_data]
        ax.plot(turns, egi, meta["style"], color=meta["color"], label=meta["label"], linewidth=2, markersize=6)

    ax.axhline(y=0.20, color="#8338ec", linestyle=":", linewidth=1.5, label=r"Gravitational Attractor Boundary ($EGI = 0.20$)")
    ax.axhspan(0.20, 0.60, color="#8338ec", alpha=0.06, label="Attractor Basin (Symptom Patching Trap)")

    ax.set_title("Figure 2: Error Gravitation Trajectories in Misleading Error Scenarios", fontsize=12, fontweight='bold', pad=12)
    ax.set_xlabel("Agent Execution Turn (t)", fontsize=11)
    ax.set_ylabel("Error Gravitation Index (EGI)", fontsize=11)
    ax.grid(True)
    ax.legend(frameon=True, facecolor="white", edgecolor="#ccc", fontsize=9)
    plt.tight_layout()

    out_path = os.path.join(OUTPUT_DIR, "error_gravitation_attractor.svg")
    plt.savefig(out_path, format="svg")
    plt.close()
    print(f"Generated: {out_path}")


def plot_pareto_frontier(records):
    """Figure 3: Pareto Frontier (Task Success Rate vs. Compute Cost)"""
    fig, ax = plt.subplots(figsize=(7, 5), dpi=300)

    # Compute aggregate stats by arm
    arms = ["Arm A: Flat Append-Only", "Arm B: Auto-Compaction", "Arm C: Generational Context"]
    colors = ["#e63946", "#f4a261", "#2a9d8f"]
    markers = ["o", "s", "^"]

    for arm, color, marker in zip(arms, colors, markers):
        arm_recs = [r for r in records if r["arm_name"] == arm]
        final_recs = [r for r in arm_recs if r["turn"] == max(x["turn"] for x in arm_recs if x["scenario_id"] == r["scenario_id"])]
        
        cost = sum(float(r["cost_usd"]) for r in final_recs)
        success = (sum(1 for r in final_recs if r["task_succeeded"] == "True") / len(final_recs)) * 100.0

        ax.scatter([cost], [success], color=color, s=200, marker=marker, edgecolors="#111", linewidths=1.5, label=arm, zorder=5)
        ax.annotate(
            f"{arm.split(':')[0]}\n({success:.1f}% @ ${cost:.4f})",
            (cost, success),
            textcoords="offset points",
            xytext=(10, -10 if success > 50 else 10),
            fontweight="bold",
            fontsize=9
        )

    ax.set_title("Figure 3: Empirical Pareto Frontier (Success vs. Compute Cost)", fontsize=12, fontweight='bold', pad=12)
    ax.set_xlabel("Total Compute Cost ($ USD)", fontsize=11)
    ax.set_ylabel("Task Success Rate (%)", fontsize=11)
    ax.set_ylim(-10, 115)
    ax.grid(True)
    ax.legend(loc="lower right", frameon=True, facecolor="white", edgecolor="#ccc")
    plt.tight_layout()

    out_path = os.path.join(OUTPUT_DIR, "pareto_frontier.svg")
    plt.savefig(out_path, format="svg")
    plt.close()
    print(f"Generated: {out_path}")


if __name__ == "__main__":
    records = load_telemetry()
    plot_phase_transition(records)
    plot_error_gravitation(records)
    plot_pareto_frontier(records)
    print("All vector figures plotted successfully.")
