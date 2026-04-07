
---

# 📄 2. `README.md`

```markdown
# Reliability Controller (BHIV Architecture)

## 📌 Overview

This project implements a distributed reliability control system using a clean BHIV architecture:

- Sarathi → Decision Engine
- Governance → Validation Layer
- Executer → Execution Layer
- Monitor → Observability (Signal Only)
- Bucket → Append-only Logging

---

## ⚙️ Tech Stack

- Python (Flask)
- Docker
- Kubernetes
- GitHub Actions (CI/CD)
- AWS EC2

---

## 🚀 Architecture Flow

GitHub Actions  
→ Sarathi (Decision)  
→ Governance (Validation)  
→ Executer (Execution)  
→ Bucket (Logging)  
→ Monitor (Signals)

---

## 🧠 Components

### 🔹 Sarathi
- Policy Decision Point
- Returns: ALLOW / BLOCK / ESCALATE

### 🔹 Governance
- Validates request
- No decision-making

### 🔹 Executer
- Executes actions (scale, restart)
- Verifies deployment

### 🔹 Monitor
- Detects anomalies
- Emits signals only

### 🔹 Bucket
- Append-only logging
- No read/write interference

---

## 🌐 External Access

| Service | URL |
|--------|-----|
| Web1 | http://<public-ip>:30001/health |
| Web2 | http://<public-ip>:30002/health |
| Monitor | http://<public-ip>:30004/metrics |

---

## ⚙️ Deployment

### Push to deploy:

```bash
git push origin main

CI/CD pipeline will:

Build Docker images
Push to Docker Hub
Deploy to Kubernetes
Trigger decision & execution flow
✅ Features
Blue-Green Deployment
Traceable Execution
Policy-driven Decisions
Clean Layer Separation
External Access via NodePort
📊 Metrics

Monitor endpoint:

/metrics
🏁 Status

✔ Fully functional
✔ BHIV compliant
✔ Production-ready


---

# ✉️ 3. SUBMISSION MESSAGE (VERY SHORT)

Use this:


BHIV architecture aligned with strict layer separation. CI/CD, governance flow, execution pipeline, and external access fully implemented and verified.