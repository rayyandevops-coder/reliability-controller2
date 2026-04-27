# DEMO_STEPS — FULL REPRODUCIBLE FLOW
**System:** Pravah  
**Domain:** pravah.blackholeinfiverse.com  
**Prerequisites:** `curl` installed. No other tools required.

---

## PHASE 5 — DNS LOCK

### What is required
The domain `pravah.blackholeinfiverse.com` must resolve to the Pravah server IP.  
All curl commands below use the domain exclusively — no raw IP.

### Infra team action (Alay)
```bash
# In your DNS provider (Route 53 / Cloudflare / etc):
# Create an A record:
#   Name:  pravah.blackholeinfiverse.com
#   Type:  A
#   Value: 54.156.236.10
#   TTL:   60

# Verify propagation:
dig pravah.blackholeinfiverse.com +short
# Expected: your-server-IP

# Verify HTTP:
curl -s http://pravah.blackholeinfiverse.com/health
# Expected: {"status":"ok"}
```

### Nginx / ingress routing (already in k8s/monitor.yml)
```bash
# The monitor service runs on port 5004 internally.
# Nginx or k8s ingress must route external port 80 → monitor-service:5004
# Sarathi must be accessible at /decision
# Executer at /execute-action (internal only — no external exposure needed)
```

---

## PHASE 6 — FULL REPRODUCIBLE FLOW

Run all commands in order. Anyone can follow this without asking.

---

### STEP 0 — Set your trace_id (Core provides this)
```bash
TRACE_ID="$(python3 -c 'import uuid; print(uuid.uuid4())')"
echo "Using trace_id: $TRACE_ID"
```

---

### STEP 1 — Start the SSE stream (in a separate terminal)
```bash
curl -N http://pravah.blackholeinfiverse.com/signals/stream
```
Keep this running. You will see events appear here in real time.

---

### STEP 2 — Register a user login event (Core → Monitor)
```bash
curl -s -X POST http://pravah.blackholeinfiverse.com/track-event \
  -H "Content-Type: application/json" \
  -d "{
    \"user_id\": \"raj\",
    \"event_type\": \"user_login\",
    \"timestamp\": $(date +%s),
    \"session_id\": \"sess-demo-001\",
    \"trace_id\": \"$TRACE_ID\",
    \"metadata\": {\"source\": \"web1-blue\"}
  }"
```

Expected response:
```json
{"status": "ok"}
```

Stream output (within 1–2 seconds):
```json
data: {"trace_id":"<your-trace>","signals":[{"signal_type":"login_detected","service":"web1-blue"}],...}
```

---

### STEP 3 — Register an interaction event
```bash
curl -s -X POST http://pravah.blackholeinfiverse.com/track-event \
  -H "Content-Type: application/json" \
  -d "{
    \"user_id\": \"raj\",
    \"event_type\": \"interaction_click\",
    \"timestamp\": $(date +%s),
    \"session_id\": \"sess-demo-001\",
    \"trace_id\": \"$TRACE_ID\",
    \"metadata\": {\"source\": \"web1-blue\"}
  }"
```

---

### STEP 4 — Trigger execution via Sarathi (the ONLY valid execution path)
```bash
curl -s -X POST http://pravah.blackholeinfiverse.com/decision \
  -H "Content-Type: application/json" \
  -d "{
    \"trace_id\": \"$TRACE_ID\",
    \"action_type\": \"restart\",
    \"service_id\": \"web1-blue\",
    \"payload\": {
      \"decision_score\": 0.75,
      \"confidence\": 0.9,
      \"priority\": \"HIGH\"
    }
  }"
```

Expected response:
```json
{
  "status": "executed",
  "trace_id": "<your-trace>",
  "executer_response": {
    "execution_id": "<uuid>",
    "trace_id": "<your-trace>",
    "status": "success"
  }
}
```

Stream output:
```json
data: {"trace_id":"<your-trace>","signals":[{"signal_type":"execution_completed","service":"web1-blue"}],...}
```

---

### STEP 5 — Observe final stream output

In your stream terminal you should now see the full causal chain:
```json
{
  "trace_id": "<your-trace>",
  "trace_hash": "<sha256>",
  "signals": [
    {"signal_type": "execution_completed", "service": "web1-blue"}
  ],
  "correlation": {
    "trace_id": "<your-trace>",
    "user_events": [
      {"event_type": "user_login",       "timestamp": ...},
      {"event_type": "interaction_click","timestamp": ...},
      {"event_type": "decision_made",    "timestamp": ...},
      {"event_type": "execution_done",   "timestamp": ...}
    ]
  },
  "causal_chain": ["execution"],
  "timestamp": "2024-04-27T10:00:00Z"
}
```

---

### STEP 6 — Verify failure case (invalid service)
```bash
curl -s -X POST http://pravah.blackholeinfiverse.com/decision \
  -H "Content-Type: application/json" \
  -d "{
    \"trace_id\": \"$TRACE_ID\",
    \"action_type\": \"restart\",
    \"service_id\": \"invalid-xyz\",
    \"payload\": {\"decision_score\": 0.8}
  }"
```

Expected: execution fails, stream shows `execution_failed`.

---

### STEP 7 — Verify security lock (direct execution attempt)
```bash
curl -s -X POST http://pravah.blackholeinfiverse.com/execute-action \
  -H "Content-Type: application/json" \
  -d "{\"service_id\":\"web1-blue\",\"action\":\"restart\",\"trace_id\":\"$TRACE_ID\"}"
```

Expected:
```json
{"error": "unauthorized"}
```
HTTP 403.

---

### STEP 8 — Health check
```bash
curl -s http://pravah.blackholeinfiverse.com/health
# {"status": "ok"}
```

---

## COMPLETE SEQUENCE (one-liner copy-paste)

```bash
TRACE_ID="$(python3 -c 'import uuid; print(uuid.uuid4())')" && echo "TRACE: $TRACE_ID"

# Terminal 1:
curl -N http://pravah.blackholeinfiverse.com/signals/stream

# Terminal 2 (run in order):
curl -s -X POST http://pravah.blackholeinfiverse.com/track-event \
  -H "Content-Type: application/json" \
  -d "{\"user_id\":\"raj\",\"event_type\":\"user_login\",\"timestamp\":$(date +%s),\"session_id\":\"sess-001\",\"trace_id\":\"$TRACE_ID\",\"metadata\":{\"source\":\"web1-blue\"}}"

curl -s -X POST http://pravah.blackholeinfiverse.com/decision \
  -H "Content-Type: application/json" \
  -d "{\"trace_id\":\"$TRACE_ID\",\"action_type\":\"restart\",\"service_id\":\"web1-blue\",\"payload\":{\"decision_score\":0.75}}"
```