# SARATHI_STREAM_PROOF.md

**System:** Pravah  
**Claim:** Sarathi emits two explicit, independent signals into the stream before any execution occurs. Both share the same trace_id. Both appear BEFORE execution signal.

---

## 1. Code Proof (sarathi/app.py)

### Signal 1 — Decision (emitted immediately after policy evaluation)
```python
requests.post(MONITOR_URL, json={
    "user_id":    "sarathi",
    "event_type": "decision_made",
    "timestamp":  int(time.time()),
    "session_id": "system",
    "trace_id":   trace_id,
    "metadata": {
        "decision":         decision_status,       # "ALLOW" / "BLOCK" / "ESCALATE"
        "action":           action,
        "policy_reference": "score_threshold_0.6"
    }
})
```

### Signal 2 — Enforcement (emitted after ALLOW, BEFORE executer is called)
```python
requests.post(MONITOR_URL, json={
    "user_id":            "sarathi",
    "event_type":         "enforcement_done",
    "timestamp":          int(time.time()),
    "session_id":         "system",
    "trace_id":           trace_id,
    "enforcement_status": "validated",
    "metadata":           {"source": "sarathi"}
})
# Executer is only called AFTER this line
res = requests.post(EXECUTER_URL, ...)
```

---

## 2. Live Stream Proof — Real Output

**Test command:**
```bash
TRACE=5d050c8c-c880-4e6d-9a01-8274556f30ec

curl -X POST http://54.156.236.10:30005/decision \
  -H "Content-Type: application/json" \
  -d "{\"trace_id\":\"$TRACE\",\"service_id\":\"web1-blue\",\"action_type\":\"restart\",\"payload\":{\"decision_score\":0.9}}"
```

**Decision signal (real — emitted at 08:23:30.736409Z):**
```json
{
  "signal_type": "decision",
  "service": "system",
  "metric": "status",
  "value": "RUNNING",
  "severity": "INFO",
  "timestamp": 1777450932,
  "trace_id": "5d050c8c-c880-4e6d-9a01-8274556f30ec",
  "trace_origin": "core",
  "trace_hash": "3ba9693acb64c1ca8124e49458b96723e9e5afb199a10226cf5e88872762ed32",
  "source": "core",
  "decision": "ALLOW",
  "policy_reference": "score_threshold_0.6",
  "action": "restart",
  "emitted_at": "2026-04-29T08:23:30.736409Z"
}
```

**Enforcement signal (real — emitted at 08:23:30.936904Z):**
```json
{
  "signal_type": "enforcement",
  "service": "sarathi",
  "metric": "status",
  "value": "RUNNING",
  "severity": "INFO",
  "timestamp": 1777450932,
  "trace_id": "5d050c8c-c880-4e6d-9a01-8274556f30ec",
  "trace_origin": "core",
  "trace_hash": "3ba9693acb64c1ca8124e49458b96723e9e5afb199a10226cf5e88872762ed32",
  "source": "core",
  "enforcement_status": "validated",
  "emitted_at": "2026-04-29T08:23:30.936904Z"
}
```

**Execution signal (real — emitted at 08:23:31.137373Z):**
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

---

## 3. Order Guarantee — Proven by Timestamps

| Signal | emitted_at | Order |
|--------|-----------|-------|
| decision | 08:23:30.736409Z | 1st |
| enforcement | 08:23:30.936904Z | 2nd |
| execution | 08:23:31.137373Z | 3rd ← after both Sarathi signals |

**decision → enforcement → execution** order is structurally enforced in code, confirmed by live timestamps.

---

## 4. Policy Reference — Visible in Stream

`"policy_reference": "score_threshold_0.6"` is present on every decision signal.  
Score used in test: `0.9 > 0.6` → `ALLOW`. Deterministic. No interpretation.