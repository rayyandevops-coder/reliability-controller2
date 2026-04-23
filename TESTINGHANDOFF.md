# PRAVAH — Testing Handoff

## 🎯 Objective

Validate:

* Real signals
* Real-time streaming
* Trace continuity
* Execution linkage

---

## 🔹 STEP 1 — Start Stream

```
curl -N http://54.156.236.10:30004/signals/stream
```

---

## 🔹 STEP 2 — Login

```
TRACE=core-proof-1

curl -X POST http://54.156.236.10:30001/login \
-H "X-TRACE-ID: $TRACE" \
-d "user_id=rayyan"
```

Observed Output:

```
login_detected:web1
```

---

## 🔹 STEP 3 — Click

```
curl -X POST http://54.156.236.10:30001/click \
-H "X-TRACE-ID: $TRACE" \
-d "user_id=rayyan&session_id=s_123"
```

Observed Output:

```
user_interaction:web1
```

---

## 🔹 STEP 4 — Execution (REAL)

```
curl -X POST http://54.156.236.10:30003/execute-action \
-H "Content-Type: application/json" \
-d '{
  "trace_id": "'"$TRACE"'",
  "service_id": "web1-blue",
  "action": "restart",
  "metrics": {"cpu": 90, "error_rate": 0.2}
}'
```

---

## 🔹 STEP 5 — Kubernetes Validation

```
kubectl get pods -n prod -w
```

Observed:

* New pod created
* Old pod terminated

---

## 🔹 STEP 6 — Final Stream Output

```
login_detected:web1
user_interaction:web1
execution_completed:web1-blue
```

---

## 🔹 VALIDATION CHECKLIST

| Check               | Status |
| ------------------- | ------ |
| Real signals        | ✅      |
| No static outputs   | ✅      |
| Single trace        | ✅      |
| Execution visible   | ✅      |
| Streaming real-time | ✅      |

---

## 🎯 FINAL STATEMENT

System is valid ONLY if:

> signals change with real events AND trace remains consistent across all layers
