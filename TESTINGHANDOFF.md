
---

# 📘 ✅ FINAL `README.md` (UPDATED — TRUTH VALIDATION)

```md
# PRAVAH — Observability Signal Pipeline (Truth Validation Phase)

---

## 🚀 Overview

PRAVAH is a **deterministic, schema-driven observability signal system** that converts real system events into structured signals.

It is NOT a monitoring tool.

It acts as a **signal pipeline** that:
- captures real infrastructure events
- validates signals using strict schema
- aggregates multi-service signals
- streams them in real time

---

## 🎯 Objective

- Convert real system behavior into structured signals  
- Enforce strict schema validation  
- Maintain deterministic severity classification  
- Aggregate signals across multiple services  
- Validate signals against real infrastructure events  

---

## 🧠 System Flow
Real Event (Kubernetes / CI-CD / Execution)
↓
Signal Generation
↓
Schema Validation
↓
Aggregation
↓
Streaming (/signals/stream)


---

## ⚙️ Core Components

### 🔹 1. Signal Generation
Sources:
- Application (latency, error_rate)
- CI/CD (deployment status)
- Infrastructure (pod crash, restart, scaling)
- Executer (execution status)

---

### 🔹 2. Severity Engine

| Metric      | CRITICAL | WARN | INFO |
|------------|---------|------|------|
| Latency    | >700    | >400 | ≤400 |
| Error Rate | >0.5    | >0.2 | ≤0.2 |

---

### 🔹 3. Schema Validation

Strict JSON schema enforced:

- Required fields mandatory  
- Typed values enforced  
  - latency → number  
  - status → SUCCESS / FAILURE / RUNNING  
- No additional properties allowed  

---

### 🔹 4. Aggregation Layer

- Merge signals from multiple services  
- Remove duplicates  
- Sort by timestamp  
- Group by trace_id  

---

### 🔹 5. Streaming Layer

Endpoint:

GET /signals/stream  

- Real-time streaming (SSE)  
- Reflects real system events  
- No simulated data  

---

## 📊 Real Example Output

```json
{
  "signal_type": "pod_crash",
  "severity": "CRITICAL",
  "service": "kubernetes",
  "metric": "latency",
  "value": 950,
  "timestamp": 1776067230,
  "trace_id": "real1"
}

🌐 Deployment
Dockerized services
Kubernetes deployment
Namespaces:
staging
production
Blue-Green deployment
NodePort external access

🧪 Real Validation Example
Trigger:
kubectl delete pod web1-blue-xxxxx -n prod
Observed:
Pod recreated (Kubernetes self-healing)
Signal emitted:
pod_crash
severity: CRITICAL
trace_id consistent
🎯 Key Features

✔ Real-event driven signals
✔ Strict schema validation
✔ Multi-service aggregation
✔ Real-time streaming
✔ Trace continuity
✔ Duplicate removal
✔ Production deployment

🚫 Constraints Followed
❌ No simulated data
❌ No decision-making
❌ No recommendations
❌ No execution logic
🏁 Outcome

PRAVAH is now a validated observability signal layer, proven against real infrastructure events and ready for system-wide integration.
![alt text](<proofs 2026-04-13 133426.png>)