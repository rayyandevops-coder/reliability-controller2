======================== README.md ========================

Pravah CI/CD – Traceable, Governed and Observable Deployment System

This project implements a production-grade CI/CD pipeline deployed on Kubernetes using AWS EC2 instances. The system ensures safe, controlled, and observable deployments.

Architecture Overview

The system is built using microservices deployed on a Kubernetes cluster with:

one master node
one worker node
namespaces: staging and production

An Elastic IP is used to ensure consistent access to services.

Services included:

web1 using blue-green deployment
web2 using blue-green deployment
sarathi for decision making
executer for execution
monitor for observability

Pipeline Flow

Code push triggers GitHub Actions pipeline.

Pipeline stages:

generate trace identifiers
build and push Docker images
deploy to staging
validate staging rollout
deploy to production
verify deployments
perform health checks
switch traffic
collect metrics
output final deployment status

Traceability

Each deployment is tracked using:

trace_id
execution_id
deployment_id

These identifiers are included in all logs to ensure full traceability.

Governance

A governance layer enforces deterministic rules after decision-making. It ensures that only valid deployment actions are executed.

If governance blocks a request:

deployment stops immediately
no changes are applied

Observability

The system provides observability through:

structured logging
latency tracking
error rate monitoring
health checks
alert generation

Monitor service detects issues and emits signals without triggering execution.

Bucket Logging

All logs are written to an append-only logging system. Logs are structured in JSON format and include trace information.

Deployment Strategy

Blue-green deployment is used for web services to ensure zero downtime. Rolling updates are used for internal services.

Rollback Mechanism

If deployment fails:

previous version is restored
traffic is redirected back
rollback event is logged

Setup Instructions

Create EC2 instances
Install Kubernetes using kubeadm
Join worker node to cluster
Configure kubectl
Allocate Elastic IP
Configure security groups
Set GitHub secrets
Push code to main branch

Verification

Commands:

kubectl get pods -n prod
kubectl rollout status deployment/web1-blue -n prod

Test endpoints:

curl http://<elastic-ip>:30001/health

Expected Output

zero downtime deployment
successful rollout
structured logs
metrics output
traceable deployment

Final Result

The system evolves from a standard CI/CD pipeline into a governed and observable execution system aligned with BHIV architecture principles.