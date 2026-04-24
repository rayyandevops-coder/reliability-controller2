# DEMO STEPS (REPRODUCIBLE)

## 1. Start stream
curl -H "Host: pravah.blackholeinfiverse.com" \
-N http://54.156.236.10/signals/stream

---

## 2. Generate trace
TRACE=$(uuidgen)

---

## 3. Login
curl -X POST http://54.156.236.10:30001/login \
-H "X-TRACE-ID: $TRACE" \
-d "user_id=rayyan"

---

## 4. Click
curl -X POST http://54.156.236.10:30001/click \
-H "X-TRACE-ID: $TRACE" \
-d "user_id=rayyan&session_id=s_123"

---

## 5. Execute (via Sarathi)
curl -X POST http://54.156.236.10:30005/decision \
-H "Content-Type: application/json" \
-d '{
  "trace_id": "'"$TRACE"'",
  "service_id": "web1-blue",
  "action_type": "restart",
  "payload": {"decision_score": 0.9}
}'

---

## EXPECTED RESULT

Stream shows:
- login_detected
- user_interaction
- decision_made
- execution_completed