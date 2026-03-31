Zero Downtime CI/CD Pipeline (Pravah System)

Overview:
This project implements a production-grade CI/CD pipeline for a distributed microservices system using Kubernetes and GitHub Actions.
The system ensures:
Zero downtime deployments
Automated build and deployment
Health-based traffic routing
Automatic rollback on failure

Architecture
Services:
web1
web2
sarathi
executer
monitor

Technologies:
Docker
Kubernetes
GitHub Actions
Minikube (local cluster)

CI/CD Pipeline Flow:
Code pushed to main
GitHub Actions triggers pipeline
Docker images are built
Images are tagged with commit SHA
Images are pushed to Docker Hub
Kubernetes deployments updated
Rolling update ensures zero downtime
Rollout is verified
Auto rollback if failure occurs

Deployment Strategy:
Rolling Update (Implemented)
maxUnavailable: 0
maxSurge: 1
Ensures:
No service interruption
New pods ready before old pods terminate

Health Checks:
Each service includes:
readinessProbe → ensures pod is ready before traffic
livenessProbe → restarts unhealthy pods

Rollback:
Automatic rollback using:
kubectl rollout undo
Triggered when rollout fails.

Zero Downtime Validation
During deployment:
Continuous curl requests sent to endpoints
No request failures observed
System remains responsive

Note (Minikube Setup)
This project uses Minikube (local Kubernetes cluster).
Due to this:
GitHub Actions cannot directly access the cluster
Deployment step in pipeline may fail
However:
Build and push steps work correctly
Deployment is verified locally using kubectl
In production:
A remote Kubernetes cluster would be used
Pipeline would complete fully without failure

Conclusion:
This project transforms the system into a:
 Continuously deployable, production-ready infrastructure

Key achievements:
Zero downtime deployment
Automated CI/CD pipeline
Safe rollback mechanism


All required proof screenshots are included in the proofs/ folder in this repository.