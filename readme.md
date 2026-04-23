# PRAVAH — Real-Time Observability Layer

## 📌 Overview

Pravah is a **real-time observability system** that tracks user behavior, system execution, and infrastructure events using a **single trace spine** across all services.

It ensures:

* No simulated signals
* Real-time streaming
* End-to-end traceability

---

## 🧩 Architecture

Core (web1/web2)
→ Monitor (Pravah)
→ Sarathi (decision layer)
→ Executer (real action layer)
→ Monitor (signal emission)

---

## 🔥 Key Features

* ✅ Real-time event streaming (`/signals/stream`)
* ✅ Single trace_id across all layers
* ✅ Execution trace linkage with execution_id
* ✅ Multi-service signal attribution
* ✅ Kubernetes-based real execution
* ✅ No fake / static signals

---

## ⚙️ Services

| Service   | Role                          |
| --------- | ----------------------------- |
| web1/web2 | User interaction layer        |
| monitor   | Observability + streaming     |
| sarathi   | Decision engine               |
| executer  | Action execution (Kubernetes) |

---

## 🚀 Endpoints

### User Layer

* `/login`
* `/click`
* `/logout`

### Observability

* `/track-event`
* `/signals/stream`

### Execution

* `/execute-action`

---

## 🔗 Trace Example

```
trace_id = core-proof-1
```

Flow:

```
web → monitor → executer → monitor → stream
```

---

## 📡 Sample Real Output

```json
{
  "trace_id": "core-proof-1",
  "signals": [
    "login_detected:web1",
    "user_interaction:web1",
    "execution_completed:web1-blue"
  ]
}
```

---

## 🧪 How to Run

1. Deploy services using Kubernetes
2. Ensure all pods are running:

```
kubectl get pods -n prod
```

3. Start stream:

```
curl -N http://54.156.236.10:30004/signals/stream
```

---

## 🎯 Guarantee

> Every signal emitted by Pravah is tied to a real event, traceable across the system, and verifiable in real-time.

---

## 👨‍💻 Author

Rayyan Shaikh
