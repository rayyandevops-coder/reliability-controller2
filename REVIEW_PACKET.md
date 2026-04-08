# PRAVAH REVIEW PACKET (FINAL)

## 🔹 Entry Point
The system is triggered via GitHub Actions pipeline on push to the main branch.

---

## 🔹 System Role

Pravah is implemented as an **Observability + Signal Routing Layer**.

It:
- detects system behavior
- measures infrastructure metrics
- emits structured signals
- routes signals via logs/output

It does NOT:
- execute actions
- make decisions
- call executer or Sarathi

---

## 🔹 Final Architecture Flow

CI/CD Pipeline  
→ Metrics Collection (Pravah)  
→ Signal Generation  
→ Signal Emission  
→ Logging / Routing  

---

## 🔹 Signal Schema (Standard Contract)

All signals follow:

```json
{
  "trace_id": "",
  "signal_type": "",
  "severity": "",
  "source": "pravah",
  "metrics": {},
  "recommended_action": "",
  "timestamp": ""
}
🔹 Signal Types Implemented
anomaly_detected
deployment_failure
latency_spike
health_degradation
🔹 Deterministic Behavior

Same input always produces same signal:

Input Condition	Output
latency > 700	latency_spike
deployment_status = failed	deployment_failure
error_rate > 0.5	health_degradation
normal values	anomaly_detected
🔹 Observability Metrics

Captured:

{"trace_id":"test123","latency":200,"error_rate":0.1,"deployment_status":"success"}'
{"metrics":{"deployment_status":"success","error_rate":0.1,"latency":200},"recommended_action":"observe","severity":"LOW","signal_type":"anomaly_detected","source":"pravah","timestamp":1775635015,"trace_id":"test123"}

🔹 Trace Continuity 

Same trace_id is maintained across:

GitHub Actions logs
Pravah signal output
Kubernetes logs
🔹 Full Trace Example
{
  "trace_id": "abc123",
  "stage": "metrics_collected"
}
{
  "trace_id": "abc123",
  "stage": "signal_emitted",
  "signal_type": "deployment_failure"
}
🔹 Signal Output Examples
🔴 Failure Case
{
  "trace_id": "abc123",
  "signal_type": "deployment_failure",
  "severity": "HIGH",
  "source": "pravah",
  "metrics": {
    "latency": 850,
    "error_rate": 0.2,
    "deployment_status": "failed"
  },
  "recommended_action": "rollback"
}
🟢 Normal Case
{
  "trace_id": "xyz123",
  "signal_type": "anomaly_detected",
  "severity": "LOW",
  "source": "pravah",
  "metrics": {
    "latency": 200,
    "error_rate": 0.1,
    "deployment_status": "success"
  },
  "recommended_action": "observe"
}
🔹 Logs Proof (IMPORTANT)

logs:
[PRAVAH SIGNAL EMITTED] {'trace_id': 'test123', 'signal_type': 'deployment_failure', 'severity': 'HIGH', 'source': 'pravah', 'metrics': {'latency': 850, 'error_rate': 0.2, 'deployment_status': 'failed'}, 'recommended_action': 'rollback', 'timestamp': 1775635041}
[ALERT] deployment_failure detected trace=test123
192.168.164.192 - - [08/Apr/2026 07:57:21] "POST /emit-signal HTTP/1.1" 200 -

🔹 System Running Proof
kubectl get pods -n prod

Output:
[root@ip-172-31-79-57 ~]# kubectl get pods -n prod
NAME                          READY   STATUS      RESTARTS      AGE
curl-test                     0/1     Completed   0             20h
executer-5d98cd65c9-6tlfz     1/1     Running     0             3m15s
monitor-684c85784c-j72tz      1/1     Running     0             3m15s
sarathi-9954dbf88-4ct4l       1/1     Running     0             3m15s
web1-blue-7fdbc6d79b-vbtp2    1/1     Running     0             3m16s
web2-blue-6cc85fc9dd-zk5wb    1/1     Running     0             3m16s
web2-green-57c598d8bd-hh9wt   1/1     Running     1 (44m ago)   21h

🔹 Endpoint Proof
Metrics
curl http://54.156.236.10:30004/metrics
Signal Emission
curl -X POST http://54.156.236.10:30004/emit-signal
🔹 Monitor Isolation Proof (CRITICAL)

Pravah strictly maintains separation:

❌ Does NOT call executer
❌ Does NOT trigger deployment
❌ Does NOT perform rollback
❌ Does NOT make decisions

Only emits signals.

🔹 Final Statement

Pravah is successfully implemented as a TANTRA-compliant Observability Layer.

It strictly follows:

detect
measure
emit
route

with zero execution or decision responsibilities.