# TESTING HANDOFF — PRAVAH SYSTEM

## 🔹 How to Run System

1. Ensure Kubernetes cluster is running
2. Deploy all services:
   - monitor
   - executer
   - sarathi
   - web1 / web2

3. Get node IP:
kubectl get nodes -o wide

4. Access monitor:
http://54.156.236.10:30004

---

## 🔹 Endpoints to Hit

### 1. Health Check
GET /health

---

### 2. Metrics
GET /metrics

---

### 3. Emit Signal
POST /emit-signal

Example:

```json
{
  "trace_id": "123",
  "latency": 800,
  "error_rate": 0.6
}
4. Streaming (IMPORTANT)

GET /signals/stream

🔹 Expected Outputs
Streaming Output:
data: [{signal}, {signal}, ...]

Each signal must include:
signal_type
severity (INFO/WARN/CRITICAL)
service
metric
value
timestamp
trace_id

🔹 Failure Scenarios to Test
❌ 1. Invalid Input
Send:
{}

Expected:
Request rejected
Error returned

❌ 2. Wrong Severity
Send invalid severity
Expected:
Validation fails
Signal rejected

❌ 3. Missing Fields
Expected:
Validation error

❌ 4. Duplicate Signals
Expected:
Duplicates removed in aggregation
🔹 Load Testing

Run:
for i in {1..10}; do
  curl -X POST http://<NODE-IP>:30004/emit-signal \
  -H "Content-Type: application/json" \
  -d '{"trace_id":"'$i'","latency":800,"error_rate":0.5}'

done
Expected:

System stable
No crashes
Correct structure
🔹 PASS Criteria
✔ Continuous streaming
✔ Valid JSON structure
✔ Correct severity classification
✔ No duplicate signals
✔ All services present in output
✔ System stable under load

🔹 FAIL Criteria
❌ Missing fields
❌ Wrong severity
❌ Invalid JSON
❌ Duplicate signals
❌ Stream not working
❌ System crashes

🎯 Final Goal
System should be:
deterministic
structured
validated
reliable