# PRAVAH — Full Trace Completion + Real User Observability

## Overview

Pravah is an observability layer that captures and correlates:

- User behavior events
- System signals (latency, errors)
- CI/CD deployment signals
- Execution layer signals

All data is linked using a **trace_id propagated from upstream (Core)**.

---

## Architecture

Core (Trace Origin) → Web → Monitor (Pravah) → Signals → Stream

- Trace ID is NOT generated inside Pravah
- Trace ID is received externally (simulated via header)
- Pravah only propagates and correlates

---

## Key Features

- Trace-based observability (strict)
- Real user event ingestion
- Multi-trace support
- CI/CD signal integration
- Deterministic summary (no inference)
- Live streaming (SSE)

---

## Deployment

- Dockerized microservices
- Kubernetes (staging + prod)
- Blue/Green deployment
- CI/CD via GitHub Actions

---

## Real Execution Proof

### 🔹 User Login
curl -X POST http://54.156.236.10:30001/login

-H "X-TRACE-ID: core-trace-001"
-d "user_id=rayyan"


---

### 🔹 User Click


curl -X POST http://54.156.236.10:30001/click

-H "X-TRACE-ID: core-trace-001"
-d "user_id=rayyan&session_id=s_123"


---

### 🔹 Signal Injection


curl -X POST http://54.156.236.10:30004/update-stream

-d '{"trace_id":"core-trace-001","latency":900,"error_rate":0.8}'


---

## 📊 Real Stream Output


data: {
"trace_id": "core-trace-001",
"signals": [
{"signal_type": "latency_spike", "value": 900},
{"signal_type": "error_spike", "value": 0.8},
{"signal_type": "deployment_success"},
{"signal_type": "pod_crash"},
{"signal_type": "execution_failure"}
],
"correlation": {
"trace_id": "core-trace-001",
"user_events": [
{"event_type": "session_start"},
{"event_type": "user_login"},
{"event_type": "page_view"},
{"event_type": "interaction_click"}
]
}
}


---

## Summary

- Trace continuity maintained across all layers
- No internal trace generation
- Real user + infra linkage proven
- System ready for Core integration