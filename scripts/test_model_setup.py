import sys
import time
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

print(f"Python version: {sys.version}")
print(f"PyTorch version: {torch.__version__}")
print(f"CUDA available: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"CUDA device name: {torch.cuda.get_device_name(0)}")
    print(f"CUDA device capability: {torch.cuda.get_device_capability(0)}")
    device = "cuda"
else:
    device = "cpu"

print(f"Target device: {device}")
t0 = time.time()
print("Loading tokenizer 'gpt2'...")
tokenizer = AutoTokenizer.from_pretrained("gpt2")
print(f"Tokenizer loaded in {time.time() - t0:.2f}s, vocab size: {len(tokenizer)}")

t1 = time.time()
print("Loading model 'gpt2' with output_attentions=True...")
model = AutoModelForCausalLM.from_pretrained(
    "gpt2",
    output_attentions=True,
    torch_dtype=torch.float32,
).to(device)
print(f"Model loaded in {time.time() - t1:.2f}s! Param count: {sum(p.numel() for p in model.parameters()):,}")

# Test forward pass with attention extraction
dummy_text = "SYSTEM: Root cause is database deadlock. ACTION: Query active locks."
inputs = tokenizer(dummy_text, return_tensors="pt").to(device)
with torch.no_grad():
    outputs = model(**inputs)

attentions = outputs.attentions
print(f"Forward pass success! Layers count: {len(attentions)}")
print(f"Layer 0 attention shape: {attentions[0].shape} (batch, heads, seq, seq)")
print("ALL PREFLIGHT CHECKS PASSED FOR NEURAL BENCHMARK!")
