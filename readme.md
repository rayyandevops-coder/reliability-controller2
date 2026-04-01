Pravah CI CD Pipeline

Overview
Pravah is a microservices system deployed using a CI CD pipeline with zero downtime and automatic rollback. The system is containerized using Docker and deployed on a Kubernetes cluster running on AWS EC2.

Services
web1
web2
sarathi
executer
monitor

Each service runs in its own container and communicates using Kubernetes services.

Tech Stack
Docker
Kubernetes
GitHub Actions
AWS EC2
Linux

CI CD Pipeline Flow
Trigger on push to main branch

Steps
Build Docker images
Tag images using commit SHA
Push images to Docker Hub
Connect to Kubernetes cluster
Apply Kubernetes manifests
Update deployments
Verify rollout
Rollback if failure

Deployment Strategy
Rolling update
maxUnavailable 0
maxSurge 1

Ensures at least one pod is always running with no downtime.

Health Checks
Each service uses readiness probe and liveness probe to ensure only healthy pods receive traffic.

Rollback
If deployment fails the pipeline runs kubectl rollout undo and restores the previous version.

Access
http://EC2 PUBLIC IP 30001 health

Zero Downtime Test
Run continuous curl on health endpoint while triggering deployment and observe no failures.

Project Structure
monitor_latest
.github workflows deploy.yml
executer
k8s
monitor
sarathi
web1
web2
docker-compose.yml

Final Result
Fully automated CI CD pipeline
Zero downtime deployment achieved
Remote Kubernetes deployment working
Production ready setup

Author
Rayyan Shaikh
