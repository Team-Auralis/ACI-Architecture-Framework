# AI Security & Identity

How VEIL controls SENTIENCE.

## SPIFFE for AI
Every individual AI agent (e.g., the Triage LLM vs the Routing ML) is issued its own distinct SPIFFE workload identity. They do not share a generic "AI API Key".

If the Triage LLM is compromised via a prompt injection attack embedded in a civilian text message, we instantly revoke that specific agent's SPIFFE certificate. The rest of the AI ensemble continues to function.

## Defense Against Data Poisoning
In Federated Learning, edge nodes send mathematical gradients back to the cloud. If an edge node is captured, the attacker might try to send poisoned gradients to slowly corrupt the global ORION AI model. 
VEIL mandates **Byzantine Fault Tolerant (BFT) Aggregation**. The central aggregator mathematically compares all incoming gradients. If one edge node's gradient deviates wildly from the consensus of the other 50 nodes, it is flagged as poisoned and discarded.
