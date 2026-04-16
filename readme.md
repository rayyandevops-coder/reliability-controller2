# PRAVAH — User + System Observability Layer

---

## 🚀 Overview

PRAVAH is a deterministic observability system that captures:

* Infrastructure signals (Kubernetes)
* User behavior (login, click, session tracking)
* Usage metrics (activity, sessions)
* Real-time streaming output

It does NOT perform decision-making — only structured observability.

---

## 🧠 Architecture

User → Web (web1/web2) → Event Tracking
→ Monitor → Metrics + Signals
→ Aggregation → Correlation → Streaming

---

## ⚙️ Features

✔ User tracking (login, click, session_start/end)
✔ Metrics engine (users, activity, session duration)
✔ Page tracking (views, clicks, time spent)
✔ Context tracking (device, region, source)
✔ Infra + CI/CD + Execution signals
✔ Correlation layer (trace-based grouping)
✔ Real-time streaming

---

## 📊 Real Output (PROOF)

### 🔹 User Metrics

```json
{
  "active_users": 2,
  "avg_session_duration": 0,
  "most_active_users": [["rayyan",8],["test1",7]],
  "total_users": 2
}
```

---

### 🔹 Summary

```json
{
  "summary": {
    "drop_off_area": "low",
    "engagement_level": "high",
    "most_active_area": "dashboard",
    "user_growth": "stable"
  }
}
```

---

### 🔹 Stream Output

```json
{
  "trace_id": "stream-1",
  "signals": [
    {"signal_type": "pod_crash", "metric": "restart_count"},
    {"signal_type": "execution_failure"},
    {"signal_type": "deployment_success"}
  ],
  "correlation": {
    "aggregate": {...},
    "summary": {...}
  }
}
```

---

## 🚫 Constraints Followed

* No execution logic
* No decision-making
* No personalization
* Deterministic outputs only

---

## 🏁 Outcome

PRAVAH provides:

✔ Infra + User + Usage observability
✔ Real-time validated system
✔ Trace-based correlation
