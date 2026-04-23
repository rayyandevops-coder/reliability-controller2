# PRAVAH — Real-Time Observability Layer

## 📌 Overview

Pravah is a **real-time observability system** that captures user events, execution behavior, and infrastructure changes using a **single trace spine**.

All signals are:

* Derived from real system events
* Streamed in real-time
* Traceable across all services

---

## 🧩 Architecture

Core (web1/web2)
→ Monitor (Pravah)
→ Sarathi (Decision Layer)
→ Executer (Kubernetes Action Layer)
→ Monitor (Streaming Output)

---

## 🔥 Key Features

* Real-time streaming (`/signals/stream`)
* Single trace_id across all layers
* Execution linkage using execution_id
* Multi-service signal attribution
* Kubernetes-based real execution
* No simulated or static signals

---

## 🔗 Trace Example

```id="trace-real"
trace_id = core-proof-1
```

---

## 📡 Real Output (Captured)

```json id="real-output-1"
{
  "trace_id": "core-proof-1",
  "signals": [
    {"signal_type": "login_detected:web1"}
  ],
  "timestamp": "2026-04-23T09:10:26.643649Z"
}
```

```json id="real-output-2"
{
  "trace_id": "core-proof-1",
  "signals": [
    {"signal_type": "login_detected:web1"},
    {"signal_type": "user_interaction:web1"}
  ],
  "timestamp": "2026-04-23T09:10:32.958289Z"
}
```

```json id="real-output-3"
{
  "trace_id": "core-proof-1",
  "signals": [
    {"signal_type": "login_detected:web1"},
    {"signal_type": "user_interaction:web1"},
    {"signal_type": "execution_completed:web1-blue"}
  ],
  "timestamp": "2026-04-23T09:10:56.715891Z"
}
```

---

## 🎯 Guarantee

> Every signal emitted by Pravah is directly tied to a real-world event and validated through real execution.
