# AI Simulation & Training

You cannot train an AI to respond to a nuclear meltdown by causing a nuclear meltdown. **SENTIENCE** requires a safe sandbox.

## Reinforcement Learning Environments
MIRROR acts as the training ground for the SENTIENCE AI agents.
*   We spawn an AI Routing Agent inside a MIRROR sandbox.
*   We simulate a massive earthquake that severs 40% of the virtual NATS mesh.
*   The AI attempts to route packets. If it fails and virtual SOS signals are dropped, it receives a negative reward.
*   If it successfully routes packets over degraded links, it receives a positive reward.

This allows ORION to train autonomous agents over millions of simulated disaster iterations, guaranteeing that when they are deployed to the real world, they have "experienced" the failure modes before.
