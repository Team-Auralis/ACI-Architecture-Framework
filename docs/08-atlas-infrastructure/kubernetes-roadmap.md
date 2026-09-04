# Kubernetes Roadmap

Why K8s is explicitly deferred for Phase 0/1.

## The Phase 0/1 Reality
Kubernetes is incredibly powerful, but it relies heavily on constant network communication (etcd sync, control plane heartbeats). If a standard K8s cluster is stretched across a satellite link and the link drops, nodes get marked as "NotReady," pods get evicted, and the cluster tears itself apart.
Therefore, Phase 0/1 relies on **Docker Compose** for rock-solid, isolated edge deployments.

## The Phase 2+ Roadmap (K3s / KubeEdge)
As ORION scales, managing 5,000 edge nodes via Docker Compose becomes untenable. 
The roadmap dictates a transition to lightweight edge orchestration:
*   **K3s:** For running isolated, single-node clusters on responder vehicles.
*   **KubeEdge/Fleet:** For managing the fleet centrally. 

This will allow ORION to dynamically schedule workloads. If a hurricane is approaching Florida, the cloud can automatically push the "Flood Prediction AI" container to all edge nodes in Florida before the storm hits.
