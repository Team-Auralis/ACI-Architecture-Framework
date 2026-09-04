# Federated Learning & Edge AI Synchronization

## The Problem
ORION's **SENTIENCE AI** needs to detect anomalies (e.g., predicting a cascading power grid failure or identifying novel structural collapse patterns). To train this AI, it needs massive amounts of telemetry from the edge. However, transmitting terabytes of raw sensor data from disaster zones over slow, expensive satellite (NTN) links is impossible.

## State-of-the-Art Solution: Edge Federated Learning (FL)
Instead of bringing the data to the AI model, ORION brings the AI model to the data.

### How it works in ORION
1.  **Local Training:** An ORION Edge Node (e.g., a mobile command center) runs a local version of the anomaly detection model. It trains this model continuously on the massive firehose of local telemetry.
2.  **Model Updates (Not Raw Data):** Instead of sending the raw data back to the cloud, the Edge Node only calculates the *mathematical gradients* (how the model needs to change based on what it learned).
3.  **Low-Bandwidth Communication:** To fit these updates over a satellite link, ORION utilizes:
    *   **Quantization:** Converting 32-bit floating-point weights to 8-bit integers.
    *   **Sparse Updates:** Only transmitting the most critical 5% of the gradients (Dual-Sided Sparse Aggregation).
    *   **Asynchronous Aggregation:** The global cloud model updates whenever it receives a sparse update from any edge node, without waiting for the rest of the disconnected fleet.

## Security Implication (Model Poisoning)
Because edge nodes are training the global AI, a compromised edge node could intentionally send malicious mathematical gradients to sabotage the global model (Data Poisoning). 
To prevent this, the central aggregation server uses **Byzantine Fault Tolerance (BFT)** algorithms to compare incoming gradients against the baseline and discard extreme outliers before integrating them into the global SENTIENCE model.