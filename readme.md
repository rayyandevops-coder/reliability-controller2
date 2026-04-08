
---

# 📄 `README.md`

```markdown
# PRAVAH — Observability & Signal System

## 📌 Overview

Pravah is an Eagle-Eye Observability Layer designed for distributed infrastructure systems.

It functions as the **eyes and nervous system**, providing real-time signals without executing any actions.

---

## 🎯 Objectives

- Detect anomalies
- Measure system metrics
- Emit structured signals
- Maintain trace continuity

---

## 🚫 What Pravah Does NOT Do

- Does NOT execute actions
- Does NOT make decisions
- Does NOT call executer or Sarathi

---

## 🧠 Architecture

CI/CD Pipeline  
→ Pravah (metrics + signal engine)  
→ Signal Output (JSON)  
→ Logs / Routing  

---

## ⚙️ Tech Stack

- Python (Flask)
- Docker
- Kubernetes
- GitHub Actions
- AWS EC2

---

## 📡 Endpoints

| Endpoint | Description |
|----------|------------|
| /metrics | Returns system metrics |
| /emit-signal | Generates structured signal |
| /health | Service health |

---

## 📊 Signal Types

- anomaly_detected
- deployment_failure
- latency_spike
- health_degradation

---

## 📦 Sample Signal

```json
{
  "trace_id": "abc123",
  "signal_type": "latency_spike",
  "severity": "HIGH",
  "source": "pravah",
  "metrics": {
    "latency": 850
  },
  "recommended_action": "scale_up"
}
🔄 Trace Continuity

Each lifecycle maintains a single trace_id across:

CI/CD pipeline
Monitoring layer
Signal emission
🚀 Deployment

Push to main branch:

git push origin main

Pipeline will:

trigger Pravah
collect metrics
emit signals
📊 Example Usage
Metrics
curl http://54.156.236.10:30004/metrics
Signal
curl -X POST http://54.156.236.10:30004/emit-signal
🏁 Status

✔ Fully working
✔ Signal-based architecture
✔ TANTRA compliant
✔ Production-ready