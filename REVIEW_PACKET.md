# 📦 REVIEW PACKET – Pravah CI/CD Production Deployment

---

## 1️⃣ Entry Point

The CI/CD pipeline is triggered automatically on every push to the `main` branch.

No manual intervention is required at any stage.

---

## 2️⃣ Pipeline Flow

1. Code is pushed to GitHub
2. GitHub Actions pipeline starts
3. Docker images are built for all services
4. Images are tagged with commit SHA
5. Images are pushed to Docker Hub
6. Kubernetes cluster is accessed using kubeconfig (stored securely in GitHub Secrets)
7. Core services (sarathi, executer, monitor) are updated using rolling updates
8. Green versions of web1 and web2 are deployed
9. Rollout is verified
10. Traffic is switched from Blue → Green
11. If failure occurs → rollback is triggered automatically

---

## 3️⃣ Real Deployment Flow

* Deployment is performed on a **real Kubernetes cluster running on AWS EC2**
* Cluster created using kubeadm
* No local clusters used (Minikube/Kind not used)
* Services exposed using NodePort

Live endpoints:

* Application: http://98.92.84.149:30001/health
* Metrics: http://98.92.84.149:30004/metrics

---

## 4️⃣ What Changed (This Task)

* Migrated from local setup to real EC2 cluster
* Implemented full CI/CD pipeline using GitHub Actions
* Added secure kubeconfig handling
* Implemented rolling updates for core services
* Implemented Blue-Green deployment for web1 and web2
* Added health checks and graceful shutdown
* Enabled automatic rollback mechanism

---

## 5️⃣ Failure + Rollback Proof

### Failure Simulation:

* Deployment intentionally broken using incorrect image

### Pipeline Behavior:

* Rollout failure detected
* Traffic switch to Green stopped
* System automatically reverted to Blue

### Result:

* Previous stable version restored
* No downtime observed

---

## 6️⃣ Zero Downtime Proof

Test performed using continuous curl:

```bash
while true; do curl http://98.92.84.149:30001/health; done
```

During deployment:

* No failed responses
* No downtime observed

---

## 7️⃣ Proof Artifacts

Available in `proofs/` folder:

* GitHub Actions logs
* Rollout logs
* Pod states (before/during/after)
* Curl output logs
* Rollback logs

---

## 🎯 Final Result

* CI/CD pipeline fully functional
* Real cluster deployment achieved
* Zero downtime validated
* Blue-Green + Rolling updates implemented
* Automatic rollback verified
* Production-ready system

---

## 👨‍💻 Submitted By

Rayyan Shaikh
