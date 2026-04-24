# TRACE DEMO — PRAVAH

## Trace ID
75bcded9-202e-415f-b223-b857aacb35f2

---

## Flow

Core (Web1)
→ Monitor (/track-event)
→ Sarathi (/decision)
→ Executer (/execute-action)
→ Monitor (/signals/stream)

---

## Step 1 — Login (User Event)

curl -X POST http://pravah.blackholeinfiverse.com/login \
-H "X-TRACE-ID: 75bcded9-202e-415f-b223-b857aacb35f2" \
-d "user_id=rayyan"

---

## Step 2 — Click (Interaction)

curl -X POST http://pravah.blackholeinfiverse.com/click \
-H "X-TRACE-ID: 75bcded9-202e-415f-b223-b857aacb35f2" \
-d "user_id=rayyan&session_id=s_123"

---

## Step 3 — Execution (Infra Event)

curl -X POST http://pravah.blackholeinfiverse.com/execute-action \
-H "Content-Type: application/json" \
-d '{
  "trace_id": "75bcded9-202e-415f-b223-b857aacb35f2",
  "service_id": "web1-blue",
  "action": "restart",
  "metrics": {"cpu": 90}
}'

---

## Observed Stream Output

login_detected:web1  
user_interaction:web1  
execution_completed:web1-blue  

---

## Proof

✔ Same trace_id across all layers  
✔ Execution linked with execution_id  
✔ Signals reflect real system events  