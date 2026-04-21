# TESTING HANDOFF — PRAVAH

## Objective

Validate full trace observability pipeline across:

- User actions  
- System signals  
- CI/CD events  

---

## Step 1 — Login (User Trace)

curl -X POST http://54.156.236.10:30001/login  
-H "X-TRACE-ID: trace-1"  
-d "user_id=rayyan"

---

## Step 2 — Interaction

curl -X POST http://54.156.236.10:30001/click  
-H "X-TRACE-ID: trace-1"  
-d "user_id=rayyan&session_id=s_123"

---

## Step 3 — Inject Signal

curl -X POST http://54.156.236.10:30004/update-stream  
-d '{"trace_id":"trace-1","latency":900,"error_rate":0.8}'

---

## Step 4 — Stream Output

curl -N http://54.156.236.10:30004/signals/stream

---

## Step 5 — CI/CD Trace Validation

Check stream output for:

trace_id = ci-xxxxx  

---

## Expected Output

- Same trace_id across:
  - user events  
  - signals  
  - correlation  

- user_events NOT empty for user traces  
- user_events empty for CI/CD traces  

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
✔ CI/CD trace visible  
✔ Multi-trace support  

---

## Notes

- Trace origin is external (simulated for testing)  
- Pravah does not generate trace_id  
- Correlation is trace-based (not causal)  
- System is integration-ready  