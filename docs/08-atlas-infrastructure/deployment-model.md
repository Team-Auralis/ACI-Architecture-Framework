# Deployment Model (GitOps)

ORION utilizes a strict GitOps deployment model.

## Git as the Source of Truth
No operator logs into a server via SSH to change a configuration file.
1.  All infrastructure, configurations, and OPA policies are defined in code within this Git repository.
2.  If an operator needs to update the authorization policy, they submit a Pull Request.
3.  Once merged, deployment operators (e.g., ArgoCD or Flux) automatically detect the change in Git and pull the new configuration down to the cloud and edge nodes.

## Self-Healing Nodes
If a responder vehicle is blown up, we do not restore from a backup tape. We take a brand new ruggedized server out of a box, plug it in, provide it a cryptographic identity, and point it at the Git repository. The node automatically pulls down its required containers and configurations, rebuilding itself from scratch in minutes.
