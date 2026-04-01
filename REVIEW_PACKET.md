Review Packet Pravah CI CD

Entry Point
Pipeline is triggered on push to main branch using GitHub Actions.

Pipeline Flow
Code pushed to repository
Pipeline starts
Docker images are built
Images tagged with commit SHA
Images pushed to Docker Hub
Kubernetes cluster accessed using kubeconfig
Manifests applied
Deployments updated
Rollout verified
Rollback triggered if failure

Live Deployment
Cluster running on AWS EC2
Namespace used prod
All services deployed and running

Changes from Previous Task
Local cluster replaced with EC2 cluster
Manual deployment replaced with automated pipeline
Rolling updates added
Rollback added

Failure and Rollback
If rollout fails pipeline executes rollback command
Previous stable version restored automatically

Proof
Pipeline logs showing build and deploy
Pods before deployment
Pods during deployment
Pods after deployment
Continuous curl output showing no downtime

Commands Used
kubectl get pods
kubectl rollout status
kubectl rollout undo

Observability
Deployment start
Pod creation
Readiness achieved
Old pod termination
Rollout success or failure

Final Result
System is continuously deployable
Zero downtime achieved
Rollback working
Production ready

Submitted by
Rayyan Shaikh
