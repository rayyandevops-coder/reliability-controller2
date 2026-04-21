# PRAVAH — Trace-Based Observability Layer

## Overview

Pravah is a strict observability layer that captures and correlates:

- User behavior events  
- System signals (latency, errors)  
- CI/CD deployment traces  
- Execution-layer signals  

All data is linked using a **trace_id propagated from upstream systems (Core / CI/CD)**.

Pravah does NOT generate trace_id. It only **propagates, validates, and correlates**.

---

## Architecture

Core / CI-CD (Trace Origin)
        ↓
Web Layer (trace propagation)
        ↓
Monitor (Pravah Core)
        ↓
Signal Generation + Correlation
        ↓
Streaming Output (SSE)

Control Plane (external to Pravah):
Mitra → Sarathi → Executer → Execution Signals → Pravah

---

## Key Features

- Strict trace-based observability  
- Real user event ingestion  
- CI/CD trace linkage  
- Multi-trace concurrency  
- Deterministic summary (no inference)  
- Real-time streaming (SSE)  

---

## Trace Model

- Trace originates externally (Core / CI/CD)
- Passed via headers (simulated in testing)
- Propagated across all layers
- Used ONLY for correlation (no modification)

---

## Deployment

- Dockerized microservices  
- Kubernetes (staging + prod)  
- Blue/Green deployment  
- CI/CD via GitHub Actions  

---

## Real Execution Proof

### 🔹 CI/CD Trace (Deployment)

From GitHub Actions:

TRACE_ID=ci-24652284212

Observed in Pravah:

[STREAM UPDATE] trace_id=ci-24652284212 latency=200 error=0.05

---

### 🔹 User Login (Trace Propagation)

curl -X POST http://54.156.236.10:30001/login  
-H "X-TRACE-ID: trace-1"  
-d "user_id=rayyan"

Monitor Logs:

[TRACE EVENT] trace_id=trace-1 event=session_start  
[TRACE EVENT] trace_id=trace-1 event=user_login  
[TRACE EVENT] trace_id=trace-1 event=page_view  

---

### 🔹 User Interaction

curl -X POST http://54.156.236.10:30001/click  
-H "X-TRACE-ID: trace-1"  
-d "user_id=rayyan&session_id=s_123"

Logs:

[TRACE EVENT] trace_id=trace-1 event=interaction_click  

---

### 🔹 Signal Injection

curl -X POST http://54.156.236.10:30004/update-stream  
-d '{"trace_id":"trace-1","latency":900,"error_rate":0.8}'

---

## 📊 Real Stream Output

data: {
  "trace_id": "trace-1",
  "signals": [
    {"signal_type": "latency_spike", "severity": "CRITICAL"},
    {"signal_type": "error_spike", "severity": "CRITICAL"},
    {"signal_type": "deployment_success"},
    {"signal_type": "pod_crash"},
    {"signal_type": "execution_failure"}
  ],
  "correlation": {
    "trace_id": "trace-1",
    "user_events": [
      {"event_type": "session_start"},
      {"event_type": "user_login"},
      {"event_type": "page_view"},
      {"event_type": "interaction_click"}
    ]
  }
}

---

## Observability Scope

✔ Trace continuity across layers  
✔ Multi-source signal aggregation  
✔ CI/CD + user + infra linkage  

---

## Limitations (Current Phase)

- Trace origin simulated via header (Core integration pending)  
- Correlation is trace-based grouping (not causal inference)  
- Execution signals are observed, not deeply linked with execution_id  
- Trace validation (hashing) not implemented  
- Event ordering based on timestamps (no distributed clock sync)  

---

## Summary

- Trace continuity maintained across system  
- Multi-layer observability achieved  
- CI/CD integration demonstrated  
- System is integration-ready with Core and Control Plane  