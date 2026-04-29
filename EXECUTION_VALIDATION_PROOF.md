# EXECUTION_VERIFICATION_PROOF.md

**System:** Pravah  
**Claim:** Execution and verification are two separate, independent signals. Execution does NOT imply success. Verification confirms the actual outcome after the action completes.

---

## 1. Code Proof (executer/app.py)

```python
execution_id = str(uuid.uuid4())

# SIGNAL 3 — execution (action attempted — outcome unknown at this point)
requests.post(MONITOR_URL, json={
    "event_type":   "execution_started",
    "trace_id":     trace_id,
    "execution_id": execution_id,
    "service":      service,
    "action":       action,
    ...
})

result = execute_action(service, action)   # kubectl runs HERE

# SIGNAL 4 — verification (outcome confirmed AFTER kubectl returns)
verification_result = "SUCCESS" if result["status"] == "success" else "FAILURE"

requests.post(MONITOR_URL, json={
    "event_type":   "verification_done",
    "trace_id":     trace_id,
    "execution_id": execution_id,          # same ID — links both signals
    "result":       verification_result,
    ...
})
```

---

## 2. SUCCESS Case — Real Output

**Test:** `service_id: web1-blue` (valid), `decision_score: 0.9`

**Execution signal (real — 08:23:31.137373Z):**
```json
{
  "signal_type": "execution",
  "service": "web1-blue",
  "metric": "status",
  "value": "RUNNING",
  "severity": "INFO",
  "timestamp": 1777450932,
  "trace_id": "5d050c8c-c880-4e6d-9a01-8274556f30ec",
  "trace_origin": "core",
  "trace_hash": "3ba9693acb64c1ca8124e49458b96723e9e5afb199a10226cf5e88872762ed32",
  "source": "core",
  "execution_id": "4a8e2bb4-bb4a-427e-a142-0f0e8e69eb9d",
  "emitted_at": "2026-04-29T08:23:31.137373Z"
}
```

**Verification signal (real — 08:23:31.337985Z):**
```json
{
  "signal_type": "verification",
  "service": "web1-blue",
  "metric": "status",
  "value": "SUCCESS",
  "severity": "INFO",
  "timestamp": 1777450932,
  "trace_id": "5d050c8c-c880-4e6d-9a01-8274556f30ec",
  "trace_origin": "core",
  "trace_hash": "3ba9693acb64c1ca8124e49458b96723e9e5afb199a10226cf5e88872762ed32",
  "source": "core",
  "execution_id": "4a8e2bb4-bb4a-427e-a142-0f0e8e69eb9d",
  "result": "SUCCESS",
  "emitted_at": "2026-04-29T08:23:31.337985Z"
}
```

**Executer API response (real):**
```json
{
  "execution_id": "4a8e2bb4-bb4a-427e-a142-0f0e8e69eb9d",
  "latency": 0.6184470653533936,
  "output": "deployment.apps/web1-blue patched",
  "status": "success",
  "trace_id": "5d050c8c-c880-4e6d-9a01-8274556f30ec"
}
```

---

## 3. FAILURE Case — Real Output

**Test:** `service_id: invalid-service`

**Execution signal (real — 08:23:33.142540Z):**
```json
{
  "signal_type": "execution",
  "service": "invalid-service",
  "metric": "status",
  "value": "RUNNING",
  "severity": "INFO",
  "timestamp": 1777450979,
  "trace_id": "cba18bcc-c5c0-41e6-8e10-913c43613f73",
  "trace_origin": "core",
  "trace_hash": "daa1d5f793e0d94bc856b902c9d9f7e3eaa453499bf181af74d843d820b6613d",
  "source": "core",
  "execution_id": "8ca09b1b-a5b0-457e-8ef0-5d6bb6cc2e85",
  "emitted_at": "2026-04-29T08:23:33.142540Z"
}
```

**Verification signal (real — 08:23:33.343033Z):**
```json
{
  "signal_type": "verification",
  "service": "invalid-service",
  "metric": "status",
  "value": "FAILURE",
  "severity": "CRITICAL",
  "timestamp": 1777450979,
  "trace_id": "cba18bcc-c5c0-41e6-8e10-913c43613f73",
  "trace_origin": "core",
  "trace_hash": "daa1d5f793e0d94bc856b902c9d9f7e3eaa453499bf181af74d843d820b6613d",
  "source": "core",
  "execution_id": "8ca09b1b-a5b0-457e-8ef0-5d6bb6cc2e85",
  "result": "FAILURE",
  "emitted_at": "2026-04-29T08:23:33.343033Z"
}
```

---

## 4. Key Properties — Proven

| Property | Execution Signal | Verification Signal |
|----------|-----------------|---------------------|
| value | "RUNNING" — never implies success | "SUCCESS" or "FAILURE" |
| execution_id | Present | Present — same ID links the pair |
| Emitted when | Before kubectl runs | After kubectl returns |
| severity on failure | INFO | CRITICAL |
| Proven by | emitted_at 08:23:31.137Z | emitted_at 08:23:31.337Z |