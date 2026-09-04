# Infrastructure Modeling

To predict cascading failures, ORION models cities as dependency graphs.

## The Dependency Graph
Physical reality is represented as nodes and edges.
*   **Node A:** City Hospital.
*   **Node B:** Main Power Substation.
*   **Node C:** Backup Diesel Generator.
*   **Edge:** Node A depends on Node B for power.

If a flood is predicted to destroy Node B, the graph instantly highlights Node A as compromised, unless Node C has enough simulated fuel. 
By modeling physical infrastructure as a graph, ORION can run millisecond traversal algorithms to warn operators of failures hours before they physically occur.
