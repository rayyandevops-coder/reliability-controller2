# PRAVAH — Testing Handoff (Vinayak)

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

Expected:

* Keepalive initially
* New output ONLY on events

---

## 🔹 STEP 2 — Login Event

```
TRACE=core-proof-1

curl -X POST http://54.156.236.10:30001/login \
-H "X-TRACE-ID: $TRACE" \
-d "user_id=rayyan"
```

Expected:

```
login_detected:web1
```

---

## 🔹 STEP 3 — Click Event

```
curl -X POST http://54.156.236.10:30001/click \
-H "X-TRACE-ID: $TRACE" \
-d "user_id=rayyan&session_id=s_123"
```

Expected:

```
user_interaction:web1
```

---

## 🔹 STEP 4 — Execution Event (REAL)

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

## 🔹 STEP 5 — Verify Kubernetes Action

```
kubectl get pods -n prod -w
```

Expected:

* Old pod terminating
* New pod created

---

## 🔹 STEP 6 — Stream Validation

Expected sequence:

1. login_detected:web1
2. user_interaction:web1
3. execution_completed:web1-blue

---

## 🔹 FAILURE TEST

Kill a pod manually:

```
kubectl delete pod <pod-name> -n prod
```

Expected:

* Signal emitted
* Same trace_id maintained

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

## 🚫 Failure Cases

* Missing trace_id → request fails
* No stream update → system invalid
* Duplicate output → streaming broken

---

## 🎯 Final Statement

System is valid ONLY if:

> signals change with real events AND trace remains consistent across all layers
