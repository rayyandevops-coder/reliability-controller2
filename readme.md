# PRAVAH — Observability & Signal System

## Overview
Pravah is a TANTRA-compliant observability layer.

It:
- detects system behavior
- measures metrics
- emits signals

It does NOT:
- execute actions
- make decisions

---

## Architecture
CI → Pravah → Signal → Logs

---

## Endpoints
- /metrics
- /emit-signal
- /health

---

## Signal Types
- anomaly_detected
- deployment_failure
- latency_spike
- health_degradation

---

## Example Signal
{
  "trace_id": "abc123",
  "signal_type": "latency_spike",
  "severity": "HIGH",
  "source": "pravah"
}

---

## Status
✔ Fully working  
✔ No execution  
✔ TANTRA compliant  