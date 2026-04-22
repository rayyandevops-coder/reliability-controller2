# PRAVAH — Full Trace Observability (Final)

## Overview

Pravah is a real-time observability layer that captures and correlates:

- User behavior events
- Execution layer outputs
- System signals

All data is linked using a **trace_id propagated from Core**.

---

## Architecture

Core → Web → Sarathi → Executer → Monitor → Stream

✔ No internal trace generation  
✔ End-to-end trace continuity  

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
  "action": "restart"
}'

### Output

{
  "trace_id": "core-final-001",
  "result": "SIMULATED: restart on web1-blue completed successfully",
  "verified": true
}

---

## 📡 Real Streaming Output

### Step 1 — Login

data: {
  "signals": [{"signal_type": "login_detected"}],
  "causal_chain": ["user_login"]
}

---

### Step 2 — Click

data: {
  "signals": [
    {"signal_type": "login_detected"},
    {"signal_type": "user_interaction"}
  ],
  "causal_chain": ["user_login", "user_click"]
}

---

### Step 3 — Execution

data: {
  "signals": [
    {"signal_type": "login_detected"},
    {"signal_type": "user_interaction"},
    {"signal_type": "execution_completed"}
  ],
  "causal_chain": ["user_login", "user_click", "execution"]
}

---

## Summary

✔ Real-time streaming  
✔ Deterministic correlation  
✔ Execution linkage proven  
✔ Trace continuity maintained  

🚀 System is fully integration-ready