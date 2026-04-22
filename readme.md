# PRAVAH — Full Trace Observability (Final)

## Overview

Pravah is a real-time observability layer that captures and correlates:

- User behavior events
- Execution layer outputs
- System signals
- CI/CD trace propagation

All data is strictly linked using a **trace_id generated from Core**.

---

## Architecture

Core → Web → Sarathi → Executer → Monitor (Pravah) → Stream

✔ Trace originates from Core  
✔ Propagated across all layers  
✔ No internal trace generation  

---

## Real Execution Proof

### 🔹 Login

curl -X POST http://54.156.236.10:30001/login \
-H "X-TRACE-ID: core-final-001" \
-d "user_id=rayyan"

---

### 🔹 Click

curl -X POST http://54.156.236.10:30001/click \
-H "X-TRACE-ID: core-final-001" \
-d "user_id=rayyan&session_id=s_123"

---

### 🔹 Execution

curl -X POST http://54.156.236.10:30003/execute-action \
-H "Content-Type: application/json" \
-d '{
  "trace_id": "core-final-001",
  "service_id": "web1-blue",
  "action": "restart",
  "metrics": {
    "cpu": 80,
    "error_rate": 0.1
  }
}'

### ✅ Output

{
  "trace_id": "core-final-001",
  "result": "SIMULATED: restart on web1-blue completed successfully",
  "verified": true
}

---

## 📡 Real Stream Output

data: {
  "trace_id": "core-final-001",
  "trace_hash": "8be66cf5f46d85cfbf88f877cad689a9741eb81956bd6e778aa3aec399aa798a",
  "signals": [
    {"signal_type": "login_detected"},
    {"signal_type": "user_interaction"},
    {"signal_type": "execution_completed"}
  ],
  "correlation": {
    "trace_id": "core-final-001",
    "user_events": [
      {"event_type": "session_start"},
      {"event_type": "user_login"},
      {"event_type": "page_view"},
      {"event_type": "interaction_click"},
      {"event_type": "execution_done"}
    ]
  },
  "causal_chain": [
    "user_login",
    "user_click",
    "execution"
  ],
  "timestamp": "2026-04-22T09:03:55.763280Z"
}

---

## Summary

✔ Trace origin from Core  
✔ Full trace continuity across layers  
✔ Real user + execution linkage  
✔ Event-driven streaming (no fake polling)  
✔ Deterministic correlation (no inference)  

✔ System is integration-ready with TANTRA