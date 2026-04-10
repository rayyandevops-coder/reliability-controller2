# PRAVAH — Canonical Signal System (TANTRA Observability Layer)

---

## 🚀 Overview

PRAVAH is a **canonical signal generation system** that standardizes how distributed systems communicate **health and state**.

It is NOT a monitoring tool.

It generates:
- Deterministic signals
- Structured outputs
- Schema-validated data
- Severity-classified metrics

This system serves as the **foundation layer** for:
- Sarathi (Decision Layer)
- InsightFlow (Signal Processing Layer)

---

## 🧠 System Architecture


Infra / CI-CD / Application
↓
PRAVAH
(Signal Generator)
↓
Structured Signals
↓
Consumers
(Sarathi / Future Systems)


---

## ⚙️ Core Features

### ✅ 1. Strict Signal Schema

Defined in: `signal_schema.json`

All signals follow this structure:

```json
{
  "signal_type": "",
  "severity": "",
  "service": "",
  "metric": "",
  "value": "",
  "timestamp": "",
  "trace_id": ""
}

✔ Enforced strictly
✔ No deviation allowed

✅ 2. Deterministic Severity Engine

Implemented in: severity_engine.py

Metric	CRITICAL	WARN	INFO
CPU	>85	>60	≤60
Memory	>80	>60	≤60
Latency	>700	>400	≤400
Error Rate	>0.5	>0.2	≤0.2

✔ Pure function
✔ No randomness

✅ 3. Schema Validation Layer

Implemented in: validator.py

✔ Validates all signals
✔ Rejects:

Missing fields
Invalid types
Incorrect structure

✔ Uses JSON Schema

✅ 4. Multi-Source Signal Generation

Signals generated from:

🔹 Application
latency_spike
error_spike
🔹 CI/CD
deployment_success
deployment_failure
🔹 Infrastructure
pod_crash
restart_loop
✅ 5. Trace Continuity
trace_id is preserved across:
signal generation
logs
pipeline

✔ If unavailable → explicitly null
✔ No fake generation

✅ 6. Standardized Output

All signals follow strict format:

{
  "signal_type": "latency_spike",
  "severity": "CRITICAL",
  "service": "application",
  "metric": "latency",
  "value": 800,
  "timestamp": 1710000000,
  "trace_id": "123"
}
🧪 API Endpoints
🔹 Health
GET /health
🔹 Metrics
GET /metrics
🔹 Emit Signals
POST /emit-signal
🚀 Deployment
✅ CI/CD Pipeline
GitHub Actions
Docker build & push
Kubernetes deployment
✅ Environments
Environment	Namespace
Staging	staging
Production	prod
🔵 Blue-Green Deployment
Blue → current version
Green → new version
Traffic switched using Kubernetes service
🌐 External Access
Service	URL
Web1	http://54.156.236.10:30001
Web2	http://54.156.236.10:30002
Monitor	http://54.156.236.10:30004/metrics
🛠️ Tech Stack
Python (Flask)
Docker
Kubernetes
GitHub Actions
JSON Schema
🎯 Outcome

✔ Deterministic signal system
✔ Structured communication layer
✔ Validated outputs
✔ Production-ready deployment
✔ TANTRA compliant

🚫 Constraints (Strictly Followed)
❌ No execution logic
❌ No decision-making
❌ No recommendations
❌ No system triggering
👨‍💻 Author

Rayyan Shaikh