# 🚀 Pravah – Production CI/CD Deployment (Blue-Green + Rolling Updates)

## 📌 Overview

Pravah is a microservices-based system deployed using a **production-grade CI/CD pipeline** on a real Kubernetes cluster.

The system is deployed on **AWS EC2 (kubeadm-based Kubernetes cluster)** and supports:

* Automated CI/CD using GitHub Actions
* Zero downtime deployments
* Blue-Green deployment strategy
* Rolling updates
* Automatic rollback

---

## 🏗️ Architecture

### Microservices:

* web1
* web2
* sarathi
* executer
* monitor

### Deployment Strategy:

* **web1, web2 → Blue-Green Deployment**
* **sarathi, executer, monitor → Rolling Updates**

---

## ☸️ Kubernetes Cluster

* Cluster setup using kubeadm on AWS EC2
* Fully managed remote cluster (no Minikube)
* Namespace used:

  * `prod` (production)

---

## ⚙️ CI/CD Pipeline

### 🔁 Trigger

* Runs on push to `main` branch

---

### 🔄 Pipeline Flow

1. Build Docker images
2. Tag images using commit SHA
3. Push images to Docker Hub
4. Load kubeconfig from GitHub Secrets
5. Deploy services to Kubernetes cluster
6. Perform rolling updates (core services)
7. Deploy green version (web1, web2)
8. Verify rollout
9. Switch traffic (Blue → Green)
10. Rollback automatically on failure

---

## 🔐 Security

* Kubeconfig stored securely in GitHub Secrets
* No credentials hardcoded
* Secure remote cluster access

---

## 🚀 Deployment Strategies

### 🔵🟢 Blue-Green Deployment (web1, web2)

* Two versions run simultaneously
* Traffic controlled via Kubernetes Service
* Instant switch between versions
* Immediate rollback capability

---

### 🔄 Rolling Updates (sarathi, executer, monitor)

* Zero downtime ensured
* Pods updated gradually
* Health checks ensure stability

---

## 🌐 Live Access

### Application

http://98.92.84.149:30001/health

### Metrics

http://98.92.84.149:30004/metrics

---

## 🧪 Zero Downtime Test

```bash
while true; do curl http://98.92.84.149:30001/health; done
```

Then trigger deployment:

```bash
git commit --allow-empty -m "test"
git push
```

✅ No downtime observed

---

## 🔁 Rollback Mechanism

* Failure detected during rollout
* Automatic rollback triggered
* For Blue-Green:

  * Traffic switched back to Blue
* For rolling updates:

  * `kubectl rollout undo` used

---

## 📸 Proof

All screenshots are available in the `proofs/` folder:

* GitHub Actions logs
* Pod states
* Zero downtime curl output
* Rollout logs
* Rollback logs

---

## 🎯 Result

* Fully automated CI/CD pipeline
* Real Kubernetes deployment
* Zero downtime achieved
* Blue-Green + Rolling updates implemented
* Automatic rollback verified
* Production-ready system

---

## 👨‍💻 Author

Rayyan Shaikh
