Pravah CI/CD – Traceable, Governed and Observable Deployment System

This project implements a production-grade CI/CD pipeline deployed on a real Kubernetes cluster hosted on AWS EC2. The system ensures zero downtime deployment, strict staging validation, automated rollback, and enhanced observability. The pipeline has been upgraded to a BHIV-compliant execution system by introducing traceability, governance, and observability features.

The system follows a microservices architecture with the following services:

web1 (Blue-Green Deployment)
web2 (Blue-Green Deployment)
sarathi (Decision Engine)
executer (Execution Engine)
monitor (Observability Layer)

The Kubernetes cluster is created using kubeadm on EC2 instances:

One master node
One worker node

Namespaces used:

staging
prod

A static Elastic IP is attached to the master node to ensure stable communication with the cluster from the CI/CD pipeline.

Main Features

Zero downtime deployment is achieved using blue-green strategy for web services and rolling updates for internal services.

Staging to production promotion ensures that every deployment is first validated in staging before being pushed to production.

Strict rollout verification ensures that deployments fail immediately if any service does not become healthy.

Automatic rollback is triggered when deployment fails, restoring the previous stable version.

Traceability is implemented using a unique trace_id, execution_id, and deployment_id generated at pipeline start and propagated across all logs and services.

Governance layer enforces deployment rules using deterministic validation before execution.

Observability includes structured logging, latency measurement, error rate tracking, and alert triggering.

System Architecture

The pipeline follows this flow:
Code Push → GitHub Actions → Build & Push Docker Images → Deploy to Staging → Validate → Deploy to Production → Health Check → Traffic Switch → Metrics Collection → Final Output

Execution layer flow:
Monitor → Detect issue → Executer → Governance check → Sarathi decision → Core execution → Verification → Logging → Outcome

Traceability

Each deployment is uniquely tracked using:

trace_id for full pipeline tracking
execution_id for run identification
deployment_id for version tracking

All logs across pipeline and services include trace_id, enabling full trace reconstruction.

Governance

A pre-deployment validation function validate_deployment_request() is implemented in the executer service.

This function applies deterministic rules such as:

blocking invalid service requests
preventing restricted actions
ensuring only allowed operations proceed

If governance returns BLOCK, execution is stopped immediately.

Observability

The monitor service continuously checks service health, latency, and system metrics.

The system detects:

service failures
high latency
error conditions

Alerts are triggered via webhook and structured logs.

Metrics collected:

latency
success rate
error rate
downtime

Structured Logging

All logs are emitted in JSON format and include:

trace_id
event name
timestamp
service information
execution data

These logs simulate integration with a memory layer (Bucket).

Deployment Strategy

Blue-Green deployment is used for web1 and web2 services to ensure zero downtime.

Rolling updates are used for internal services.

Traffic switching is handled via Kubernetes service selector updates.

Setup Instructions

Create EC2 instances for master and worker nodes
Install Kubernetes using kubeadm
Join worker node to cluster
Configure kubectl access
Allocate and associate Elastic IP to master node
Configure Security Groups to allow required NodePort traffic
Clone repository
Configure GitHub Secrets:
DOCKER_USERNAME
DOCKER_PASSWORD
KUBECONFIG
Push code to main branch to trigger pipeline

Verification

Deployment can be verified using:

kubectl get pods -n prod
kubectl rollout status deployment/<service> -n prod
curl http://<elastic-ip>:<nodeport>/health

Expected Result

A fully automated CI/CD pipeline that:

deploys without downtime
validates before production
rolls back on failure
tracks every deployment
enforces governance
provides observability metrics

This system represents a production-grade DevOps pipeline integrated with traceability, governance, and observability.