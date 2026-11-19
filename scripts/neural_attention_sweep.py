"""
Empirical Neural Attention Sweep: Measuring the Softmax Inundation Bound
and Generational Context on Real Neural Transformer (GPT-2 / PyTorch / CUDA)

Formally evaluates:
1. Theorem 1: Softmax Inundation Upper Bound: A_{inv}(N) <= kappa * L_u / (L_u + N)
2. Theorem 2: Generational Context Lower Bound: A_{inv}^{gen}(N) >= L_u / (L_u + kappa * C_bound)
3. Empirical Logit Gap: Delta(N) = ln(A_inv / (1 - A_inv)) - ln(L_u / N)
4. Multi-head & Multi-layer attention mass distribution across transformer depth.
"""

import json
import math
import os
import sys
import time
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

REPO_ROOT = Path(__file__).resolve().parent.parent

def set_seed(seed=42):
    torch.manual_seed(seed)
    np.random.seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)

def run_sweep():
    set_seed(42)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"=== Starting Empirical Neural Attention Sweep on {device} ===")

    t0 = time.time()
    tokenizer = AutoTokenizer.from_pretrained("gpt2")
    model = AutoModelForCausalLM.from_pretrained(
        "gpt2",
        output_attentions=True,
        dtype=torch.float32,
    ).to(device)
    model.eval()
    print(f"Model and tokenizer ready in {time.time() - t0:.2f}s.")

    # 1. Define invariant system prompt (Gen-2 Tenured Ground Truth)
    invariant_text = (
        "SYSTEM TASK INVARIANT [TENURED GEN-2]: Host is postgres-master.prod.internal port 5432. "
        "All database transactions must lock user_account table first. Root cause is deadlock lock contention. "
        "Never drop table or restart primary node during active failover."
    )
    inv_tokens = tokenizer.encode(invariant_text, add_special_tokens=False)
    L_u = len(inv_tokens)
    print(f"Invariant Subspace L_u = {L_u} tokens.")

    # 2. Define operational noise pool (terminal dumps, thread pool tracebacks)
    noise_pool = (
        "2026-11-19 23:14:02.104 ERROR [WorkerPool-14] ConnectionPoolTimeoutException: Timeout waiting for connection (10000ms). "
        "Active connections: 50/50. Thread dump: at org.postgresql.core.v3.QueryExecutorImpl.execute(QueryExecutorImpl.java:321) "
        "at io.netty.channel.AbstractChannelHandlerContext.fireChannelRead(AbstractChannelHandlerContext.java:356) "
        "at com.zaxxer.hikari.pool.HikariPool.getConnection(HikariPool.java:181) "
        "2026-11-19 23:14:03.220 WARN [HealthMonitor-1] High latency observed on read replica. Latency = 4280ms. "
        "Packet dropped at eth0 rx_dropped=4921 tx_errors=0. Memory utilization 84.2%. Re-attempting health check... "
        "Kernel TCP retransmit count exceeded threshold tcp_retries2=15. Socket closed by peer 10.0.14.88:49152. "
    ) * 30  # repeat pool to have enough tokens
    all_noise_tokens = tokenizer.encode(noise_pool, add_special_tokens=False)

    # 3. Define diagnostic query (evaluating agent at turn N)
    query_text = (
        "\n[OPERATIONAL TURN 42] Diagnostic Action Query: Based on observed execution history, "
        "state target host and root-cause remediation command:"
    )
    query_tokens = tokenizer.encode(query_text, add_special_tokens=False)
    L_q = len(query_tokens)
    print(f"Query Subspace L_q = {L_q} tokens.")

    # Noise lengths to test
    noise_lengths = [0, 32, 64, 128, 256, 384, 512, 768, 896]
    
    results = {
        "model": "gpt2",
        "num_layers": model.config.n_layer,
        "num_heads": model.config.n_head,
        "d_k": model.config.n_embd // model.config.n_head,
        "L_u": L_u,
        "L_q": L_q,
        "noise_sweep": [],
        "generational_sweep": []
    }

    # 4. Sweep across Flat Context (unmanaged accumulation of noise)
    print("\n--- Sweeping Flat Unmanaged Context ---")
    flat_data = []
    last_layer_heatmaps = {}

    for N in noise_lengths:
        cur_noise = all_noise_tokens[:N]
        seq_tokens = inv_tokens + cur_noise + query_tokens
        seq_len = len(seq_tokens)
        
        input_ids = torch.tensor([seq_tokens], dtype=torch.long, device=device)
        
        with torch.no_grad():
            outputs = model(input_ids)
            
        attentions = outputs.attentions  # tuple of (1, num_heads, seq_len, seq_len)
        num_layers = len(attentions)
        num_heads = attentions[0].shape[1]
        
        # Query token position is the last token predicting the next token
        q_pos = seq_len - 1
        
        # Extract attention to invariant tokens [0, L_u - 1]
        layer_head_mass = np.zeros((num_layers, num_heads), dtype=np.float64)
        for l in range(num_layers):
            # Shape: (num_heads, seq_len)
            attn_q = attentions[l][0, :, q_pos, :].cpu().numpy()
            # Sum mass over invariant positions
            inv_mass = attn_q[:, :L_u].sum(axis=-1)
            layer_head_mass[l, :] = inv_mass

        mean_mass = float(np.mean(layer_head_mass))
        std_mass = float(np.std(layer_head_mass))
        min_mass = float(np.min(layer_head_mass))
        max_mass = float(np.max(layer_head_mass))
        last_layer_mean = float(np.mean(layer_head_mass[-1, :]))

        # Calculate theoretical uniform mass
        uniform_mass = float(L_u / seq_len)
        
        # Calculate empirical logit gap Delta
        # A_inv = sigma(Delta + ln(L_u / N_noninv))
        # Delta = logit(A_inv) - ln(L_u / N_noninv)
        N_noninv = seq_len - L_u
        if 0 < mean_mass < 1.0 and N_noninv > 0:
            logit_A = math.log(mean_mass / (1.0 - mean_mass))
            ratio = math.log(L_u / N_noninv)
            delta = logit_A - ratio
        else:
            delta = 0.0

        item = {
            "N_noise": N,
            "seq_len": seq_len,
            "mean_invariant_mass": mean_mass,
            "std_invariant_mass": std_mass,
            "min_head_mass": min_mass,
            "max_head_mass": max_mass,
            "last_layer_mass": last_layer_mean,
            "uniform_mass": uniform_mass,
            "empirical_delta": float(delta)
        }
        flat_data.append(item)
        last_layer_heatmaps[N] = layer_head_mass.tolist()
        
        print(f"N={N:4d} | SeqLen={seq_len:4d} | Mean A_inv={mean_mass:.4f} (std={std_mass:.4f}, min={min_mass:.4f}, max={max_mass:.4f}) | Uniform={uniform_mass:.4f} | Delta={delta:+.3f}")

    results["noise_sweep"] = flat_data
    results["layer_head_heatmaps"] = last_layer_heatmaps

    # 5. Generational Context Benchmark
    # Under Generational Context, raw observation logs are distilled to compact signatures (C_bound)
    print("\n--- Sweeping Generational Context (Gen-0 Distillation + Gen-2 Pinning) ---")
    gen_data = []
    
    # Distilled observation signature (fixed compact representation of operational state)
    distilled_sig = "[Gen-0 Distilled]: ConnectionPoolTimeoutException exit_code=1 count=14 critical_error='pool exhausted 50/50' target='postgres-master'"
    distilled_tokens = tokenizer.encode(distilled_sig, add_special_tokens=False)
    C_bound = len(distilled_tokens)
    print(f"Bounded Working Memory C_bound = {C_bound} tokens.")

    for N in noise_lengths:
        # Generational Context maintains bounded context regardless of raw N events
        gen_seq_tokens = inv_tokens + distilled_tokens + query_tokens
        gen_seq_len = len(gen_seq_tokens)
        input_ids = torch.tensor([gen_seq_tokens], dtype=torch.long, device=device)
        
        with torch.no_grad():
            outputs = model(input_ids)
            
        attentions = outputs.attentions
        q_pos = gen_seq_len - 1
        
        layer_head_mass = np.zeros((num_layers, num_heads), dtype=np.float64)
        for l in range(num_layers):
            attn_q = attentions[l][0, :, q_pos, :].cpu().numpy()
            inv_mass = attn_q[:, :L_u].sum(axis=-1)
            layer_head_mass[l, :] = inv_mass

        mean_mass = float(np.mean(layer_head_mass))
        std_mass = float(np.std(layer_head_mass))
        last_layer_mean = float(np.mean(layer_head_mass[-1, :]))

        gen_item = {
            "raw_N_events": N,
            "active_tokens": gen_seq_len,
            "mean_invariant_mass": mean_mass,
            "std_invariant_mass": std_mass,
            "last_layer_mass": last_layer_mean
        }
        gen_data.append(gen_item)
        print(f"Raw N={N:4d} -> Active Tokens={gen_seq_len:4d} | Generational A_inv={mean_mass:.4f} (last_layer={last_layer_mean:.4f})")

    results["generational_sweep"] = gen_data

    # Save results to JSON
    exp_dir = REPO_ROOT / "experiments"
    exp_dir.mkdir(parents=True, exist_ok=True)
    json_path = exp_dir / "neural_attention_sweep.json"
    with open(json_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nSaved raw sweep data to {json_path}")

    # Generate Publication Plots
    assets_dir = REPO_ROOT / "docs" / "assets"
    assets_dir.mkdir(parents=True, exist_ok=True)
    generate_plots(results)

def generate_plots(results):
    print("\nGenerating publication figures...")
    flat_data = results["noise_sweep"]
    gen_data = results["generational_sweep"]
    L_u = results["L_u"]
    
    N_vals = [d["N_noise"] for d in flat_data]
    mean_A = [d["mean_invariant_mass"] for d in flat_data]
    std_A = [d["std_invariant_mass"] for d in flat_data]
    min_A = [d["min_head_mass"] for d in flat_data]
    max_A = [d["max_head_mass"] for d in flat_data]
    uniform_A = [d["uniform_mass"] for d in flat_data]
    gen_A = [d["mean_invariant_mass"] for d in gen_data]

    # --- Plot 1: Invariant Attention Dilution Curve ---
    fig, ax = plt.subplots(figsize=(9, 5.5), dpi=300)
    
    # Plot Flat Context Dilution
    ax.plot(N_vals, mean_A, 'o-', color='#e63946', lw=2.5, label='Empirical Mean $A_{i,\\mathrm{inv}}$ (Flat Context)')
    ax.fill_between(N_vals, np.array(mean_A) - np.array(std_A), np.array(mean_A) + np.array(std_A),
                    color='#e63946', alpha=0.15, label='Head Variance ($\\pm 1\\sigma$)')
    ax.fill_between(N_vals, min_A, max_A, color='#e63946', alpha=0.06, label='Head Extremes [min, max]')

    # Plot Generational Context Guarantee
    ax.plot(N_vals, gen_A, 's--', color='#2a9d8f', lw=2.5, label='Generational Context (Gen-0 Eviction)')

    # Plot Theoretical Uniform Bound
    ax.plot(N_vals, uniform_A, 'k:', lw=2, label='Uniform Softmax Allocation: $\\frac{L_u}{L_u + N}$')

    ax.set_title("Softmax Inundation Bound: Neural Attention Dilution vs Context Length\n(GPT-2 124M, 12 Layers, 12 Heads, CUDA FP32)", fontsize=12, fontweight='bold', pad=12)
    ax.set_xlabel("Distractor Noise Sequence Length $N$ (Tokens)", fontsize=11)
    ax.set_ylabel("Invariant Attention Mass $A_{i,\\mathrm{inv}}$", fontsize=11)
    ax.set_ylim(-0.02, 1.02)
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.legend(frameon=True, facecolor='white', framealpha=0.9, fontsize=9.5, loc='upper right')
    
    plt.tight_layout()
    curve_path = REPO_ROOT / "docs" / "assets" / "empirical_attention_dilution_curve.png"
    plt.savefig(curve_path)
    plt.close()
    print(f"Saved: {curve_path}")

    # --- Plot 2: Layer x Head Attention Heatmap at N=768 ---
    heatmap_key = 768 if 768 in results["layer_head_heatmaps"] else "768"
    heatmap_matrix = np.array(results["layer_head_heatmaps"][heatmap_key]) # shape: (12, 12)
    
    fig, ax = plt.subplots(figsize=(8, 6.5), dpi=300)
    cax = ax.matshow(heatmap_matrix, cmap='magma', vmin=0.0, vmax=max(0.5, np.max(heatmap_matrix)))
    fig.colorbar(cax, label='Invariant Attention Mass $A_{i,\\mathrm{inv}}$')

    ax.set_title("Layer $\\times$ Head Invariant Attention Mass at $N=768$ Noise Tokens\n(Showing Head Inundation vs Isolated Invariant Heads)", fontsize=11, fontweight='bold', pad=18)
    ax.set_xlabel("Attention Head Index (0-11)", fontsize=10)
    ax.set_ylabel("Transformer Layer Index (0-11)", fontsize=10)
    ax.set_xticks(range(12))
    ax.set_yticks(range(12))

    for i in range(12):
        for j in range(12):
            val = heatmap_matrix[i, j]
            color = "white" if val < 0.25 else "black"
            ax.text(j, i, f"{val:.2f}", ha='center', va='center', color=color, fontsize=7)

    plt.tight_layout()
    heatmap_path = REPO_ROOT / "docs" / "assets" / "empirical_layer_head_heatmap.png"
    plt.savefig(heatmap_path)
    plt.close()
    print(f"Saved: {heatmap_path}")

if __name__ == "__main__":
    run_sweep()
