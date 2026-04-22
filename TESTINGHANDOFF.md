# TESTING HANDOFF — PRAVAH

## Objective

Validate full real-time observability

---

## Step 1 — Set Trace

TRACE=core-final-001

---

## Step 2 — Login

curl -X POST http://54.156.236.10:30001/login \
-H "X-TRACE-ID: $TRACE" \
-d "user_id=rayyan"

---

## Step 3 — Click

curl -X POST http://54.156.236.10:30001/click \
-H "X-TRACE-ID: $TRACE" \
-d "user_id=rayyan&session_id=s_123"

---

## Step 4 — Execution

curl -X POST http://54.156.236.10:30003/execute-action \
-H "Content-Type: application/json" \
-d '{
  "trace_id": "'"$TRACE"'",
  "service_id": "web1-blue",
  "action": "restart"
}'

---

## Step 5 — Stream

curl -N http://54.156.236.10:30004/signals/stream

---

## Expected Behavior

✔ Signals evolve over time:
- login_detected  
- user_interaction  
- execution_completed  

✔ Causal chain grows step-by-step  
✔ Same trace_id everywhere  
✔ Real timestamps  

---

## Success Criteria

✔ No static output  
✔ No fake signals  
✔ Event-driven streaming  
✔ Execution linkage verified  