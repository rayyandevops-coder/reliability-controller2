Reliability Controller – Monitoring Layer (Task 4)

Overview:
This project implements a deterministic monitoring + execution layer designed for integration into a control loop system:
Monitoring → Decision → Execution
The system is built to be:
Deterministic
Integration-ready
Observable
Safe (cooldown + validation)

Architecture:
[ Monitoring Service ]
↓
(metrics JSON)
↓
[ Decision System (External) ]
↓
(action JSON)
↓
[ Execution Service ]
↓
(Kubernetes / Docker)

Services:
1. Monitor Service
Collects real system metrics using psutil
Checks service health
Emits structured signals (NO decision logic)
Endpoints:
/metrics
/internal/runtime-payload
/health

2. Execution Service
Accepts external actions
Validates inputs
Executes real operations using Kubernetes
Enforces cooldown (safety)

Endpoints:
/execute-action
/health

API CONTRACTS
/metrics
{
  "service_id": "web1",
  "timestamp": "...",
  "status": "healthy",
  "cpu": 0.45,
  "memory": 0.62,
  "error_rate": 0.0,
  "env": "DEV"
}


/internal/runtime-payload
{
  "cpu": 0.5,
  "memory": 0.6,
  "status": "healthy",
  "env": "DEV"
}


/execute-action
Request:
{
  "service_id": "web1",
  "action": "restart"
}

Response:
{
  "execution_id": "...",
  "status": "success",
  "service_id": "web1",
  "action": "restart"
}


Safety Features:
Cooldown system (prevents repeated actions)
Action validation
Structured logging
No auto-recovery (external control enforced)

Logging:
Monitor Logs
DETECTION events
Executer Logs
ACTION_RECEIVED
ACTION_ACCEPTED
ACTION_EXECUTED
ACTION_BLOCKED

How to Run
Docker
docker-compose up --build

Kubernetes
kubectl apply -f k8s/


Testing
Check metrics
curl http://localhost:5004/metrics

Trigger action
curl -X POST http://localhost:5003/execute-action \
-H "Content-Type: application/json" \
-d '{"service_id":"web1","action":"restart"}'


Key Design Decisions
Removed decision logic from monitoring
Standardized payload for RL integration
Implemented real execution (kubectl)
Ensured deterministic outputs

Outcome
This system is now:
Integration-ready
Deterministic
Safe
Production-aligned


