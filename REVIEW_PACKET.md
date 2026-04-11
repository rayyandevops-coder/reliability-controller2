# REVIEW PACKET — PRAVAH (PHASE 3)

---

## 🔹 Aggregation Flow

Signals are generated from multiple sources:
- Application (latency, error_rate)
- CI/CD (deployment status)
- Infrastructure (pod crash, restart, scaling)
- Executer (execution status)

Flow:

Metrics → Signal Generation → Validation → Aggregation → Streaming

Aggregation is handled using:
- Merge signals from all sources
- Remove duplicates
- Sort by timestamp
- Group by trace_id

---

## 🔹 Streaming Design

Endpoint:
GET /signals/stream

Implementation:
- Server-Sent Events (SSE)
- Continuous streaming every few seconds
- Sends batched signals

Output format:

data: [{signal}, {signal}, ...]

---

## 🔹 Real Multi-Service Signal Output

Example:

```json
[
  {
    "signal_type": "latency_spike",
    "severity": "CRITICAL",
    "service": "application",
    "metric": "latency",
    "value": 777,
    "timestamp": 1775851324,
    "trace_id": "753"
  },
  {
    "signal_type": "deployment_success",
    "severity": "INFO",
    "service": "cicd",
    "metric": "status",
    "value": 0,
    "timestamp": 1775851324,
    "trace_id": "753"
  },
  {
    "signal_type": "execution_update",
    "severity": "INFO",
    "service": "executer",
    "metric": "status",
    "value": 1,
    "timestamp": 1775851324,
    "trace_id": "753"
  }
]
Failure Handling

1. Invalid Input
Input:
{}

Result:

Validation fails
Signal rejected
Error returned

2. Schema Violation
Missing fields → rejected
Invalid severity → rejected
Extra fields → rejected

3. Duplicate Signals
Removed during aggregation using unique key

4. System Stability
Under load, system remains stable
No crashes
No malformed signals

🎯 Final Result
✔ Aggregation working
✔ Streaming working
✔ Multi-service signals present
✔ Validation strict
✔ System stable

🚫 Compliance
Rule	Status
No execution logic	✅
No decision-making	✅
No recommendations	✅
Schema strict	✅