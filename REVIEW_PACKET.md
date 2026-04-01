Review Packet Pravah CI CD

1 Entry Point
Pipeline is triggered on push to main branch using GitHub Actions.

2 Pipeline Flow
Code push triggers pipeline
Docker images are built
Images are tagged with commit SHA
Images are pushed to Docker Hub
Kubernetes cluster on EC2 is accessed securely using kubeconfig
Manifests are applied
Deployments are updated using rolling update
Rollout is verified and pipeline fails if rollout fails

3 Live Deployment
Deployment is performed on a real Kubernetes cluster running on AWS EC2
Namespace used is prod
All services are running and accessible

4 What Changed
Local Minikube setup replaced with real EC2 cluster
Manual deployment replaced with automated CI CD pipeline
Rolling updates implemented
Automatic rollback added

5 Failure and Rollback Behavior
If rollout fails pipeline detects failure
Rollback is triggered automatically using rollout undo
Previous stable version is restored

6 Proof
Pipeline execution logs
Pods before deployment
Pods during deployment
Pods after deployment
Continuous curl output showing no downtime
Metrics endpoint accessible

Result
System is continuously deployable
Zero downtime verified
Rollback working
Production deployment achieved on EC2 cluster

Submitted by
Rayyan Shaikh
