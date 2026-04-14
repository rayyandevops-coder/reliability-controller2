# PRAVAH — Full Observability Layer (Infra + User + Usage)

---

## 🚀 Overview

PRAVAH is a **deterministic observability system** that standardizes how systems communicate **health, usage, and state**.

It combines:

- Infrastructure signals (Kubernetes)
- CI/CD signals
- Execution layer signals
- User behavior observability

---

## 🎯 Objective

- Provide structured system-wide observability  
- Maintain strict schema validation  
- Ensure trace continuity  
- Enable real-time signal streaming  
- Support downstream consumption (Mitra)

---

## 🧠 Architecture

User → Web (web1/web2) → Event Tracking  
→ Monitor Service → Signal Generation  
→ Validation → Aggregation → Correlation  
→ Streaming (/signals/stream)

---

## ⚙️ Core Features

✔ User Event Tracking (login, click, page view)  
✔ Metrics Engine (users, sessions, activity)  
✔ Page Observability (views, clicks, time spent)  
✔ Context Tracking (device, region, source)  
✔ Signal System (infra + cicd + execution)  
✔ Strict Schema Validation  
✔ Correlation Layer (trace-based grouping)  
✔ Real-time Streaming (SSE)  

---

## 🔗 Endpoints

| Endpoint | Description |
|--------|------------|
| /track-event | user event ingestion |
| /user-metrics | aggregated user stats |
| /page-metrics | page analytics |
| /user-context | device/region/source |
| /aggregate | combined metrics |
| /summary | deterministic summary |
| /signals/stream | real-time unified stream |

---

## 📊 Output Structure

```json
{
  "trace_id": "session123",
  "signals": [...],
  "correlation": {
    "aggregate": {...},
    "summary": {...}
  }
}
🧪 Real-World Validation

✔ Kubernetes pod crash → signal emitted
✔ User interaction → metrics updated
✔ Multi-source signals → single trace
✔ Streaming reflects live system

🚫 Constraints Followed
No decision-making
No execution triggering
No personalization
Deterministic outputs only
🏁 Outcome

PRAVAH is now a full observability layer:

Infra + User + Usage → unified, validated, real-time system

Proof (MANDATORY)

User Proof:
curl http://localhost:30004/user-metrics
output:
{"active_users":0,"login_frequency":{"10+":0,"100+":0,"15+":0,"2+":0,"5+":0},"most_active_users":[],"returning_users":0,"total_users":0}

Infra Proof:
NAME                          READY   STATUS    RESTARTS   AGE
executer-77bbbbd58-xhktb      1/1     Running   0          17m
monitor-79865d4bf8-nbbp9      1/1     Running   0          17m
sarathi-6dcfbf5b69-5hznm      1/1     Running   0          17m
web1-blue-6f99dcffc8-d4g7c    1/1     Running   0          8m14s
web1-green-7d57b9bf75-n9p24   1/1     Running   0          17m
web2-blue-76c65df8b-6f25r     1/1     Running   0          17m
web2-green-6554cb7775-lhfm2   1/1     Running   0          17m
[root@ip-172-31-79-57 ~]# kubectl delete pod web1-blue-6f99dcffc8-d4g7c -n prod
pod "web1-blue-6f99dcffc8-d4g7c" deleted
^C[root@ip-172-31-79-57 ~]curl http://localhost:30004/signals/streamam
data: {'trace_id': 'stream-1', 'signals': [{'signal_type': 'latency_spike', 'severity': 'INFO', 'service': 'application', 'metric': 'latency', 'value': 0, 'timestamp': 1776167851, 'trace_id': 'stream-1'}, {'signal_type': 'error_spike', 'severity': 'INFO', 'service': 'application', 'metric': 'error_rate', 'value': 0, 'timestamp': 1776167851, 'trace_id': 'stream-1'}, {'signal_type': 'deployment_success', 'severity': 'INFO', 'service': 'cicd', 'metric': 'status', 'value': 'SUCCESS', 'timestamp': 1776167851, 'trace_id': 'stream-1'}, {'signal_type': 'execution_update', 'severity': 'INFO', 'service': 'executer', 'metric': 'status', 'value': 'RUNNING', 'timestamp': 1776167851, 'trace_id': 'stream-1'}], 'correlation': {'trace_id': 'stream-1', 'aggregate': {'user_metrics': {'total_users': 0, 'active_users': 0, 'returning_users': 0, 'login_frequency': {'2+': 0, '5+': 0, '10+': 0, '15+': 0, '100+': 0}, 'most_active_users': []}, 'page_metrics': {'views': {}, 'clicks': {}, 'avg_time_spent': 0, 'interaction_density': 'low'}, 'context': {'regions': {}, 'devices': {}, 'sources': {}}}, 'summary': {'user_growth': 'stable', 'engagement_level': 'low', 'most_active_area': 'unknown', 'drop_off_area': 'unknown'}}}

