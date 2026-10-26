# Launch Kit

Copy-paste posts for the platforms that don't require me to have your account.
I can't post these — every one ties the submission to your identity.

## Read this first

**1. The licence is resolved.** The code is Apache-2.0, so people can actually
run, fork and ship it — that was the blocker standing in front of everything
else. One caveat survives: the prose and the paper are CC BY-NC-ND 4.0, which
forbids commercial reuse and derivative versions. Quoting is fine; reusing the
diagrams is not. Know the answer before you get asked.

**2. Do not call Theorem 1 a new theorem.** It is Cauchy–Schwarz plus the
definition of softmax. A mathematician will say so in the first comment and
everything else in the thread becomes collateral. The paper already scopes this
in §8 — let the posts match it. The honest, interesting claim is: *softmax
normalisation gives a horizon-independent bound if you bound the volume of the
non-invariant context, and here is a controller that maintains that bound.*

**3. What actually makes this shareable** is the second table row, not the
vision. Lead with a number and a command that reproduces it.

## Order

| # | Where | Why |
|---|---|---|
| 1 | r/LocalLLaMA | No real karma gate. Will actually run the code and argue with you. |
| 2 | Show HN | Needs account history first — new accounts get auto-flagged regardless of content. |
| 3 | X thread | Lowest ceiling, but it's where the link gets picked up and reposted. |

Do not post all three the same hour. One thread with real replies is worth more
than three ignored ones.

---

## 1. r/LocalLLaMA

**Title**

```
I bounded the active context so my agent stops forgetting its goal at turn 40
```

**Body**

```
Long-horizon agents drift. The usual diagnosis is "the model is dumb". The
boring mechanism is that every tool response gets appended to history, so by
turn 40 the system prompt is a rounding error in the softmax denominator and the
model spends its attention on whatever was said most recently.

Wrote up the mechanism and built the controller for it: tier the context by how
invariant each item is (system + standing goal / current plan / tool output),
put a hard cap on the volume of the non-invariant tiers, and evict with ARC-style
scoring using attention weight over entropy instead of recency alone.

Deterministic simulation, 3 scenarios, 40 turns, no API calls:

| arm                  | active tokens | invariant attn share | CSR    |
|----------------------|---------------|----------------------|--------|
| append-only history  | 5,099         | 0.0425               | 0.0059 |
| sliding window       | 3,340         | 0.0553               | 0.0077 |
| this                 | 129           | 0.0757               | 0.2000 |

What this is not: no live-model evaluation yet. The attention share is computed
from synthetic key vectors under a stated uniform-bounded-projection assumption,
and the derived bound is vacuous at realistic norms — §8 of the paper says so in
plain text. The simulation exercises the controller, it is not evidence that a
frontier model gets smarter.

Stdlib only, `python ccb_bench.py` reproduces that table in about a second.

[repo link]

Genuinely interested in where this falls apart — the eviction policy is the part
I trust least.
```

---

## 2. Show HN

**URL field:** the repository link
**Text field:**

```
I've been running long agent tasks and the failure is always the same shape: the
agent stops working on the task and starts patching whatever error it saw last.
The mechanism is unglamorous — tool output accumulates, the softmax denominator
grows, and the system prompt's share of attention goes to zero.

This is a small Python package that tiers context by invariance and caps the
volume of the mutable tiers, so the standing goal keeps competing regardless of
turn count. Eviction is ARC-style, scored by attention weight over entropy.

The supplied simulation goes 5,099 -> 129 active tokens with the invariant
attention share up from 0.0425 to 0.0757 and the cognitive signal ratio up 33.9x.
No API keys, stdlib only.

I want to be precise about the theory, because it's easy to oversell: the bound
is elementary. It's Cauchy-Schwarz applied to the softmax, and it's vacuous under
realistic projection norms — the paper's limitations section says this outright.
The contribution I'd defend is the controller that maintains the volume bound as
a post-condition, plus the eviction fix (a naive promote-if-larger implementation
picks the entry it just promoted as its own victim).

No live-model numbers yet. That's the obvious next thing and I haven't done it.
```

---

## 3. X / Twitter thread

```
1/
Long agent runs fail the same way every time: the model stops working on the task
and starts patching the last error it saw.

It isn't a reasoning failure. It's arithmetic.

2/
Every tool response gets appended. The softmax denominator grows. By turn 40 the
system prompt's share of attention is ~4%.

The model optimises for what's recent because that's literally what the
normalisation says to do.

3/
So: tier the context by invariance.

- system + standing goal: never evicted
- current plan: evicted on staleness
- tool output: hard volume cap

Eviction scored by attention weight / entropy (ARC-style), not recency.

4/
Deterministic sim, 40 turns, 3 scenarios:

append-only: 5,099 tokens, CSR 0.0059
sliding window: 3,340 tokens, CSR 0.0077
bounded: 129 tokens, CSR 0.2000

5/
Where I'd push back on myself: the bound is elementary (Cauchy-Schwarz on
softmax) and vacuous at realistic norms. No live-model eval yet. The paper says
all of this in its limitations section rather than hiding it.

Stdlib only. `python ccb_bench.py` reproduces it.

[repo link]
```

---

## After you post

- Reply to every technical objection in the first two hours. That is what moves
  a thread, not the original post.
- If someone reports a concrete failure case, open an issue for it and link the
  issue in the thread. Visible maintenance is the signal people read for.
- If someone asks what they're allowed to do with it, answer plainly: Apache-2.0
  for the code, CC BY-NC-ND for the prose. Don't let it become a licence thread.
