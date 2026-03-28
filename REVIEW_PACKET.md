REVIEW PACKET – TASK 4

---

1. ENTRY POINT

* Monitor: `/metrics`
* Executer: `/execute-action`

---

2. CORE EXECUTION FLOW

1. Monitor collects:

   * CPU
   * Memory
   * Service health

2. Emits deterministic JSON

3. External system (RL / Control Plane):

   * Consumes payload
   * Decides action

4. Executer:

   * Validates action
   * Applies via Kubernetes

---

3. LIVE FLOW

Example:

Step 1:
GET /metrics

Step 2:
Decision system selects:
"restart web1"

Step 3:
POST /execute-action

Step 4:
Kubernetes executes:
kubectl rollout restart deployment/web1

---

4. CHANGES MADE

| Area       | Before            | After                 |
| ---------- | ----------------- | --------------------- |
| Monitoring | Simulated metrics | Real metrics (psutil) |
| Decision   | Inside monitor    | Removed               |
| Execution  | Simulated         | Real kubectl          |
| Payload    | cpu_usage         | cpu                   |
| Safety     | None              | Cooldown added        |

---

5. FAILURE CASES

1. Invalid action → rejected (400)
2. Rapid repeated action → blocked (429)
3. Service down → detected via /metrics
4. Kubernetes failure → logged in executer

---

6. PROOF

* Logs: monitor.log, executer.log
* API outputs (curl)
* Kubernetes commands executed

---

7. SYSTEM GUARANTEES

* Deterministic outputs
* No randomness
* External control only
* Safe execution layer

---



