# Communication Model

ORION does not assume a homogenous network. It assumes a fractured, heterogeneous landscape.

## The Hybrid Transport Model
ORION nodes (gateways, leaf nodes, mobile apps) are completely agnostic to the underlying transport medium. They do not care if they are transmitting over gigabit fiber or a 9600-baud LoRaWAN link. 

The communication model is built on:
1.  **Asynchronous Messaging:** NATS Pub/Sub means a sender drops a message and forgets it. They do not wait for a synchronous TCP ACK from the final destination.
2.  **Message Queuing at the Edge:** If a physical link is severed, the NATS Leaf Node buffers the outbound events locally.
3.  **Medium Agnosticism:** When the physical link is restored (via any medium), the buffer flushes.

This decoupling of the application layer from the physical layer is why ORION can survive planetary-scale emergencies.
