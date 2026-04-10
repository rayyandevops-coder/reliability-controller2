# PRAVAH — Canonical Signal System (TANTRA Observability Layer)

---

## 🚀 Overview

PRAVAH is a **canonical signal language system** designed to standardize how distributed systems communicate **health and state**.

It is NOT a monitoring tool.

It generates:
- Deterministic signals
- Structured outputs
- Schema-validated data
- Severity-aware metrics

---

## 🧠 Objective

- Define a **unified signal format**
- Ensure **strict validation**
- Provide **reliable inputs** to decision systems (Sarathi)
- Enable future processing (InsightFlow)

---

## ⚙️ Signal Schema (STRICT)

Defined in: `signal_schema.json`

```json
{
  "type": "object",
  "required": [
    "signal_type",
    "severity",
    "service",
    "metric",
    "value",
    "timestamp",
    "trace_id"
  ],
  "properties": {
    "signal_type": { "type": "string" },
    "severity": {
      "type": "string",
      "enum": ["INFO", "WARN", "CRITICAL"]
    },
    "service": { "type": "string" },
    "metric": { "type": "string" },
    "value": {},
    "timestamp": { "type": "integer" },
    "trace_id": {
      "type": ["string", "null"]
    }
  },
  "additionalProperties": false
}
⚙️ Core Features
✅ 1. Strict Schema Enforcement
All signals validated using JSON Schema
Rejects invalid structure
No extra fields allowed
✅ 2. Deterministic Severity Engine

Implemented in severity_engine.py

Metric	CRITICAL	WARN	INFO
CPU	>85	>60	≤60
Memory	>80	>60	≤60
Latency	>700	>400	≤400
Error Rate	>0.5	>0.2	≤0.2
✅ 3. Validation Layer (Strict)
Implemented in validator.py
Uses JSON schema validation
Rejects:
Missing fields
Invalid types
Extra fields
✅ 4. Multi-Source Signal Generation
🔹 Application Signals
latency_spike
error_spike
🔹 CI/CD Signals
deployment_success
deployment_failure
🔹 Infrastructure Signals
pod_crash
restart_loop
scaling_event
✅ 5. Trace Continuity
trace_id is preserved across system
If missing → explicitly null
No artificial generation
✅ 6. Standard Output Format
{
  "signal_type": "latency_spike",
  "severity": "CRITICAL",
  "service": "application",
  "metric": "latency",
  "value": 850,
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
✅ CI/CD
GitHub Actions
Docker build & push
Kubernetes deployment
✅ Environments
Environment	Namespace
Staging	staging
Production	prod
🔵 Blue-Green Deployment
Blue → active version
Green → new version
Traffic switched using Kubernetes services
🌐 External Access
Service	URL
Web1	http://<NODE-IP>:30001
Web2	http://<NODE-IP>:30002
Monitor	http://<NODE-IP>:30004/metrics
🎯 Outcome

✔ Strict schema validation
✔ Deterministic signal generation
✔ Multi-source coverage
✔ Production-ready deployment
✔ TANTRA compliant

🚫 Constraints Followed
❌ No execution logic
❌ No decision-making
❌ No recommended actions
❌ No system triggering
👨‍💻 Author

Rayyan Shaikh