# HANDOFF TESTING (ZERO CONTEXT REQUIRED)

## STEP 1 — START STREAM

curl -H "Host: pravah.blackholeinfiverse.com" \
-N http://54.156.236.10/signals/stream

---

## STEP 2 — GENERATE TRACE

TRACE=$(uuidgen)

---

## STEP 3 — USER FLOW

curl -X POST http://54.156.236.10:30001/login \
-H "X-TRACE-ID: $TRACE" \
-d "user_id=test"

curl -X POST http://54.156.236.10:30001/click \
-H "X-TRACE-ID: $TRACE" \
-d "user_id=test&session_id=s_1"

---

## STEP 4 — EXECUTION (MANDATORY VIA SARATHI)

curl -X POST http://54.156.236.10:30005/decision \
-H "Content-Type: application/json" \
-d '{
  "trace_id": "'"$TRACE"'",
  "service_id": "web1-blue",
  "action_type": "restart",
  "payload": {"decision_score": 0.9}
}'

---

## EXPECTED OUTPUT

Stream shows:

{
  "trace_id": "...",
  "signals": [
    {"signal_type":"execution_completed","service":"web1-blue"}
  ]
}

---

## STEP 5 — FAILURE TEST

TRACE=$(uuidgen)

curl -X POST http://54.156.236.10:30005/decision \
-H "Content-Type: application/json" \
-d '{
  "trace_id": "'"$TRACE"'",
  "service_id": "invalid-service",
  "action_type": "restart",
  "payload": {"decision_score": 0.9}
}'

---

## EXPECTED

{
  "signal_type": "execution_failed"
}

---

## STEP 6 — SECURITY TEST

curl -X POST http://54.156.236.10:30003/execute-action \
-H "Content-Type: application/json" \
-d '{"trace_id":"hack","service_id":"web1-blue","action":"restart"}'

---

## EXPECTED

{"error":"unauthorized"}

---

## STEP 7 — CONCURRENCY TEST

for i in {1..5}; do
  TRACE=$(uuidgen)
  curl -X POST http://54.156.236.10:30001/login \
  -H "X-TRACE-ID: $TRACE" \
  -d "user_id=test$i" &
done

---

## RESULT

Multiple traces appear independently.

---

## FINAL CONDITION

If all above works:

✔ system is valid  
✔ system is reproducible  
✔ system requires no developer  