# PRAVAH — DEMO STEPS

## 1. Start Stream

curl -N http://pravah.blackholeinfiverse.com/signals/stream

---

## 2. Login

TRACE=core-live-1

curl -X POST http://pravah.blackholeinfiverse.com/login \
-H "X-TRACE-ID: $TRACE" \
-d "user_id=rayyan"

---

## 3. Click

curl -X POST http://pravah.blackholeinfiverse.com/click \
-H "X-TRACE-ID: $TRACE" \
-d "user_id=rayyan&session_id=s_123"

---

## 4. Execute

curl -X POST http://pravah.blackholeinfiverse.com/execute-action \
-H "Content-Type: application/json" \
-d '{
  "trace_id": "'"$TRACE"'",
  "service_id": "web1-blue",
  "action": "restart",
  "metrics": {"cpu": 90}
}'

---

## Expected Output

login_detected:web1  
user_interaction:web1  
execution_completed:web1-blue  

---

## Kubernetes Validation

kubectl get pods -n prod -w

Expected:
- Old pod terminating  
- New pod running  