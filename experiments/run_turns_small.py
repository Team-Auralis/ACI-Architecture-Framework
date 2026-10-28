import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from live_attention_probe import build_context, measure

tok = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-0.5B")
model = AutoModelForCausalLM.from_pretrained(
    "Qwen/Qwen2.5-0.5B",
    dtype=torch.float16,
    device_map="cuda",
    attn_implementation="eager",
)
model.eval()

per_turn = 60
cap = 240
for turn in (2, 5, 10, 20):
    n_append = per_turn * turn
    n_bounded = min(n_append, cap)
    for arm, n in (("append-only", n_append), ("bounded", n_bounded)):
        ids, prefix_len = build_context(tok, n)
        total = ids.shape[1]
        if total > 3800:
            print(f"  skip turn={turn} {arm} ctx={total}")
            torch.cuda.empty_cache()
            continue
        shares, _ = measure(model, ids, prefix_len)
        share = sum(shares) / len(shares)
        print(
            f"  turn={turn:2d} {arm:12s} ctx={total:5d} share={share:.4f} uniform={prefix_len / total:.4f}"
        )
        torch.cuda.empty_cache()
