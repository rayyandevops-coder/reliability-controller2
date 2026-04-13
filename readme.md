# TESTING HANDOFF — PRAVAH SYSTEM (TRUTH VALIDATION)

---

## 🔹 How to Run System

1. Ensure Kubernetes cluster is running

2. Deploy all services:
   - monitor
   - executer
   - sarathi
   - web1
   - web2

3. Get node IP:
kubectl get nodes -o wide

4. Access monitor service:
http://<NODE-IP>:30004


---

## 🔹 Endpoints to Hit

### 1. Health Check
GET /health

---

### 2. Emit Signal (REAL INPUT)
POST /emit-signal

Example:
```json
{
  "trace_id": "real1",
  "latency": 900,
  "error_rate": 0.7
}
3. Update Stream Input

POST /update-stream

{
  "trace_id": "real1",
  "latency": 950,
  "error_rate": 0.8
}
4. Streaming (CRITICAL)

GET /signals/stream

🔹 Expected Outputs

Streaming Output:

data: [{signal}, {signal}, ...]

Each signal must include:

signal_type
severity (INFO / WARN / CRITICAL)
service
metric
value (typed)
timestamp
trace_id
🔹 Real Infra Validation Test (MANDATORY)
Step 1: Trigger real event
kubectl delete pod web1-blue-xxxxx -n prod
Step 2: Verify infra
kubectl get pods -n prod

(New pod should be created)

Step 3: Validate stream
curl http://<NODE-IP>:30004/signals/stream

Expected:

signal_type: pod_crash
service: kubernetes
severity: CRITICAL
trace_id: real1
🔹 Failure Scenarios to Test
❌ 1. Invalid Input
{}

Expected:

Request rejected
Error returned
❌ 2. Invalid Data Type
{
  "trace_id": "t1",
  "latency": "high"
}

Expected:

Validation failure
❌ 3. Schema Violation
Missing fields
Extra fields

Expected:

Rejected by validator
❌ 4. Duplicate Signals

Expected:

Removed in aggregation
🔹 Load Testing
for i in {1..10}; do
  curl -X POST http://<NODE-IP>:30004/emit-signal \
  -H "Content-Type: application/json" \
  -d '{"trace_id":"'$i'","latency":800,"error_rate":0.5}'
done

Expected:

Stable system
No crashes
Correct structured output
🔹 PASS Criteria

✔ Real infra event reflected in signals
✔ Continuous streaming working
✔ Correct schema (typed values)
✔ Same trace_id across signals
✔ No duplicate signals
✔ System stable under load

🔹 FAIL Criteria

❌ Simulated/random data used
❌ Missing fields
❌ Invalid schema
❌ Duplicate signals
❌ Stream not reflecting real events
❌ System crash

🎯 Final Goal

System must be:

deterministic
schema-validated
real-event driven
reliable