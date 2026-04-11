# PRAVAH — Observability Signal Pipeline (Phase 3)

---

## 🚀 Overview

PRAVAH is a **deterministic, schema-driven signal system** that standardizes how distributed systems communicate **health and state**.

It is NOT a monitoring tool.

It acts as a **signal pipeline** that:
- generates signals
- validates them
- aggregates across services
- streams them in real time

---

## 🎯 Objective

- Convert system metrics into structured signals  
- Ensure strict schema validation  
- Maintain deterministic severity classification  
- Aggregate signals across multiple services  
- Stream signals continuously for downstream systems  

---

## 🧠 System Flow
Metrics (latency, error_rate, status)
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
Generates signals from:
- Application (latency, error_rate)
- CI/CD (deployment status)
- Infrastructure (restart, crash, scaling)
- Executer (execution status)

---

### 🔹 2. Severity Engine

Deterministic classification:

| Metric      | CRITICAL | WARN | INFO |
|------------|---------|------|------|
| Latency    | >700    | >400 | ≤400 |
| Error Rate | >0.5    | >0.2 | ≤0.2 |

---

### 🔹 3. Schema Validation

All signals follow strict JSON schema:

- Required fields enforced  
- Only allowed values  
- No extra fields  

---

### 🔹 4. Aggregation Layer

- Combines signals from multiple sources  
- Removes duplicates  
- Sorts by timestamp  
- Groups by trace_id  

---

### 🔹 5. Streaming Layer

Endpoint:

GET /signals/stream  

- Continuous streaming (SSE)  
- Real-time signal flow  
- Batched output  

data: [{"signal_type": "latency_spike", "severity": "WARN", "service": "application", "metric": "latency", "value": 423, "timestamp": 1775892627, "trace_id": "522"}, {"signal_type": "error_spike", "severity": "INFO", "service": "application", "metric": "error_rate", "value": 0.05, "timestamp": 1775892627, "trace_id": "522"}, {"signal_type": "deployment_success", "severity": "INFO", "service": "cicd", "metric": "status", "value": 0, "timestamp": 1775892627, "trace_id": "522"}, {"signal_type": "execution_update", "severity": "INFO", "service": "executer", "metric": "status", "value": 1, "timestamp": 1775892627, "trace_id": "522"}]

🧪 API Endpoints
🔹 Health
GET /health

🔹 Metrics
GET /metrics

🔹 Emit Signal
POST /emit-signal

🔹 Streaming (MAIN)
GET /signals/stream

🌐 Deployment
Dockerized services
Kubernetes deployment
Namespaces:
staging
production
Blue-Green deployment
NodePort external access

📊  Output
{
  "signal_type": "latency_spike",
  "severity": "CRITICAL",
  "service": "application",
  "metric": "latency",
  "value": 800,
  "timestamp": 1710000000,
  "trace_id": "123"
}

🧪 Load Simulation
for i in {1..10}; do
  curl -X POST http://<NODE-IP>:30004/emit-signal \
  -H "Content-Type: application/json" \
  -d '{"trace_id":"'$i'","latency":800,"error_rate":0.5}'
done

🎯 Key Features

✔ Deterministic signal generation
✔ Strict schema validation
✔ Multi-service aggregation
✔ Real-time streaming
✔ Trace-based grouping
✔ Duplicate removal
✔ Production deployment

🚫 Constraints Followed
❌ No execution logic
❌ No decision-making
❌ No recommendations
❌ No system triggering

🏁 Outcome
PRAVAH is now a distributed observability signal pipeline ready for:

system-wide monitoring abstraction
decision layer consumption
real-world testing
