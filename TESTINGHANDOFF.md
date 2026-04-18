# TESTING HANDOFF — PRAVAH

## Objective

Validate full trace observability pipeline

---

## Step 1 — Login


curl -X POST http://54.156.236.10:30001/login

-H "X-TRACE-ID: core-trace-001"
-d "user_id=rayyan"


---

## Step 2 — Interaction


curl -X POST http://54.156.236.10:30001/click

-H "X-TRACE-ID: core-trace-001"
-d "user_id=rayyan&session_id=s_123"


---

## Step 3 — Inject Signal


curl -X POST http://54.156.236.10:30004/update-stream

-d '{"trace_id":"core-trace-001","latency":900,"error_rate":0.8}'


---

## Step 4 — Stream


curl -N http://54.156.236.10:30004/signals/stream


---

## Expected Output

- Same trace_id across:
  - user events
  - signals
  - correlation
- user_events NOT empty
- signals include:
  - latency_spike
  - error_spike
  - deployment_success
  - pod_crash
  - execution_failure

---

## Success Criteria

✔ Trace continuity  
✔ Real user event ingestion  
✔ Signal correlation  
✔ Streaming working  

---

## Notes

- Trace ID is provided externally
- Pravah does not generate trace_id
- System is integration-ready with Core