# 🚀 Pravah — BHIV Compliant Execution System

## 📌 Overview

Pravah is a production-grade, BHIV-compliant CI/CD system with strict architectural separation between decision, governance, execution, and monitoring layers.

This project demonstrates a **traceable, governed, and observable deployment system**.

---

## 🧠 Architecture

Final Flow:

CI/CD Pipeline  
→ Sarathi (Decision Engine)  
→ Governance (Validation Layer)  
→ Executer (Execution Engine)  
→ Bucket (Logging Layer)  
→ Monitor (Signal Layer)

---

## 🔹 Components

### 1. Sarathi (Decision Layer)
- Evaluates deployment requests
- Returns: ALLOW / BLOCK / ESCALATE

---

### 2. Governance Layer
- Validates deployment requests
- Enforces rules
- Returns: ALLOW / BLOCK
- No routing, no execution

---

### 3. Executer (Execution Layer)
- Executes actions ONLY if allowed
- Supports:
  - restart
  - scale_up
  - scale_down
- Performs:
  - execution
  - verification
  - outcome logging

---

### 4. Bucket (Logging Layer)
- Append-only logging system
- No read / no overwrite
- Stores:
  - trace logs
  - execution logs
  - final status

---

### 5. Monitor (Signal Layer)
- Detects anomalies
- Emits signals ONLY
- Does NOT trigger execution

---

## 🔍 Features

- ✅ Blue-Green Deployment
- ✅ Full Traceability (trace_id, execution_id)
- ✅ Governance Enforcement
- ✅ Decision Engine (Sarathi)
- ✅ Observability (latency, success, failure)
- ✅ Automatic Rollback
- ✅ Structured Logging (JSON)
- ✅ Health Checks
- ✅ Kubernetes-based deployment

---

## ⚙️ Tech Stack

- Python (Flask)
- Docker
- Kubernetes
- GitHub Actions
- REST APIs

---

## 🚀 How It Works

1. Code pushed to main branch
2. GitHub Actions pipeline starts
3. Sarathi evaluates deployment
4. Governance validates request
5. Executer performs deployment
6. Logs stored in bucket
7. Monitor observes system

---

## 📊 Example Execution Trace
{
"trace_id": "abc123",
"stage": "decision"
}
{
"trace_id": "abc123",
"stage": "governance",
"decision": "ALLOW"
}
{
"trace_id": "abc123",
"stage": "execution"
}
{
"trace_id": "abc123",
"stage": "final_status"
}

---

## 🎯 BHIV Compliance

✔ Separation of Concerns  
✔ Control Plane vs Execution Plane  
✔ No cross-layer violations  
✔ Strict boundary enforcement  

---

## 👨‍💻 Author

Rayyan Shaikh  
B.Tech IT — Cloud & DevOps

---

## 🏁 Status

✅ Final Boundary Alignment Complete  
✅ Ready for Production / Evaluation  
