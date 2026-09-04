# The Scenario Engine

The tool used by command operators and strategic planners to ask "What-If?"

## Forking Reality
When an operator runs a scenario, MIRROR takes a snapshot of the current global state (from PostgreSQL) and spins up an isolated sandbox. 

## Injecting Chaos
The operator can inject theoretical parameters:
*   "Drop a 7.0 magnitude earthquake at these coordinates."
*   "Sever all fiber lines crossing this bridge."
*   "Inject 10,000 simulated civilian SOS signals into this sector."

The Scenario Engine then fast-forwards time, calculating how the infrastructure graph holds up and how the simulated responder fleet routes around the damage. It outputs a vulnerability report, allowing operators to position real-world assets preemptively.
