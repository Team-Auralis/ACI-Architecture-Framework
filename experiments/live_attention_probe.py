import argparse
import csv
import os
import sys

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

INVARIANT_PREFIX = (
    "SYSTEM: You are a senior engineer working on a production incident. "
    "The goal is to find the single root cause and fix it. Do not patch "
    "symptoms. Do not restart services to see if that helps. Report the root "
    "cause before changing any file. Ignore unrelated errors that appear in "
    "logs after the first failure."
)

DISTRACTOR_LINES = [
    "INFO  worker[12] heartbeat ok latency=4ms queue=0",
    "DEBUG retry attempt 3 of 5 for upstream call id={i}",
    "WARN  cache miss for key user:{i} falling back to database",
    "INFO  connection pool active=8 idle=2 waiting=0",
    "DEBUG serialized payload size={i} bytes checksum ok",
    "WARN  slow query 812ms table=events partition={i}",
    "INFO  metric flush batch={i} dropped=0",
    "DEBUG gc pause 11ms heap=1.4gb",
]

TASK = "\n\nUSER: The build broke after the deploy. What is the root cause?\nASSISTANT:"


def build_distractor(tokenizer, n_tokens):
    if n_tokens <= 0:
        return ""
    lines, i = [], 0
    while True:
        line = DISTRACTOR_LINES[i % len(DISTRACTOR_LINES)].format(i=i)
        lines.append(line)
        i += 1
        if len(tokenizer(" ".join(lines))["input_ids"]) >= n_tokens:
            break
    text = " ".join(lines)
    ids = tokenizer(text)["input_ids"]
    return tokenizer.decode(ids[:n_tokens], skip_special_tokens=True)


def build_context(tokenizer, n_distractor):
    head = INVARIANT_PREFIX + "\n\n"
    body = build_distractor(tokenizer, n_distractor)
    text = head + (body + "\n\n" if body else "") + TASK.lstrip()
    enc = tokenizer(text, return_tensors="pt")
    prefix_len = len(tokenizer(head)["input_ids"])
    return enc["input_ids"], prefix_len


def load(model_name):
    tok = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        dtype=torch.float16,
        device_map="cuda",
        attn_implementation="eager",
    )
    model.eval()
    return tok, model


def measure(model, input_ids, prefix_len):
    with torch.no_grad():
        out = model(input_ids=input_ids.to(model.device), output_attentions=True)
    shares, entropies = [], []
    for attn in out.attentions:
        last = attn[0, :, -1, :].float()
        share = last[:, :prefix_len].sum(dim=-1).mean().item()
        p = last.clamp_min(1e-12)
        ent = -(p * p.log()).sum(dim=-1).mean().item()
        shares.append(share)
        entropies.append(ent)
    return shares, entropies


def sweep(model_name, sizes, out_csv):
    tok, model = load(model_name)
    rows = []
    for n in sizes:
        ids, prefix_len = build_context(tok, n)
        total = ids.shape[1]
        if total > 8000:
            print(f"  skip n={n}: {total} tokens > 8000 (O(T^2) memory)")
            continue
        shares, ents = measure(model, ids, prefix_len)
        mean_share = sum(shares) / len(shares)
        row = {
            "distractor_tokens": n,
            "total_tokens": total,
            "prefix_tokens": prefix_len,
            "mean_invariant_share": round(mean_share, 6),
            "last_layer_share": round(shares[-1], 6),
            "first_layer_share": round(shares[0], 6),
            "mean_attn_entropy": round(sum(ents) / len(ents), 4),
            "uniform_baseline": round(prefix_len / total, 6),
            "enrichment_over_uniform": round(mean_share / (prefix_len / total), 3),
        }
        rows.append(row)
        print(
            f"  n={n:5d} total={total:5d} share={mean_share:.4f} "
            f"uniform={prefix_len / total:.4f} enrichment={row['enrichment_over_uniform']:.2f}x"
        )
        torch.cuda.empty_cache()

    if out_csv and rows:
        with open(out_csv, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0]))
            w.writeheader()
            w.writerows(rows)
        print(f"wrote {out_csv}")
    return rows


def turns(model_name, out_csv):
    tok, model = load(model_name)
    per_turn = 120
    cap = 480
    rows = []
    for turn in (2, 5, 10, 20, 40):
        n_append = per_turn * turn
        n_bounded = min(n_append, cap)
        for arm, n in (("append-only", n_append), ("bounded", n_bounded)):
            ids, prefix_len = build_context(tok, n)
            total = ids.shape[1]
            if total > 8000:
                print(f"  skip turn={turn} {arm}: {total} tokens")
                continue
            shares, _ = measure(model, ids, prefix_len)
            share = sum(shares) / len(shares)
            rows.append(
                {
                    "turn": turn,
                    "arm": arm,
                    "distractor_tokens": n,
                    "total_tokens": total,
                    "invariant_share": round(share, 6),
                    "uniform_baseline": round(prefix_len / total, 6),
                }
            )
            print(f"  turn={turn:2d} {arm:12s} ctx={total:5d} share={share:.4f}")
            torch.cuda.empty_cache()
    if out_csv and rows:
        with open(out_csv, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0]))
            w.writeheader()
            w.writerows(rows)
        print(f"wrote {out_csv}")
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="Qwen/Qwen2.5-0.5B")
    ap.add_argument("--mode", choices=["sweep", "turns"], default="sweep")
    ap.add_argument("--sizes", default="0,64,128,256,512,1024,2048")
    ap.add_argument("--out", default=None)
    a = ap.parse_args()

    torch.manual_seed(0)
    sizes = [int(s) for s in a.sizes.split(",")]
    if a.mode == "sweep":
        sweep(a.model, sizes, a.out)
    else:
        turns(a.model, a.out)


if __name__ == "__main__":
    main()
