Pravah CI CD Production Deployment

Overview
This project implements a production grade CI CD pipeline for Pravah. The system is deployed on a Kubernetes cluster set up on AWS EC2 and fully managed. The pipeline performs real deployment with zero downtime and automatic rollback.

Cluster Setup
A Kubernetes cluster was created on AWS EC2 using kubeadm. The system was first deployed manually and verified. The cluster is fully managed and used for all CI CD deployments.

CI CD Pipeline
Trigger
Pipeline runs on every push to main branch

Steps
Build Docker images
Tag images using commit SHA
Push images to Docker Hub
Authenticate to Kubernetes cluster using kubeconfig
Apply Kubernetes manifests
Wait for rollout
Fail if rollout fails

Rollback
If deployment fails the pipeline automatically runs rollout undo and restores the previous version.

Zero Downtime
Rolling update strategy ensures no service interruption. During deployment health and metrics endpoints remain available.

Access
Application
http://98.92.84.149:30001/health

Metrics
http://98.92.84.149:30004/metrics

Environment
Namespace used prod

Proof
Pipeline logs
Pods before and after deployment
Zero downtime curl output
All screenshots are in proofs folder

Result
CI CD pipeline deploys to real cluster
No manual steps required
Zero downtime achieved
Rollback working
Kubernetes cluster deployed on EC2 and fully managed

Author
Rayyan Shaikh
