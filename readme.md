Monitoring Layer - Distributed Control Loop System
Overview
This project implements a deterministic monitoring layer integrated into a distributed infrastructure control loop.
It is designed to:
Detect service health
Emit structured metrics
Feed a decision engine
Accept control actions
Provide full observability via logs

Architecture
Monitoring → Decision Engine → Control Plane
Monitoring Layer (This Project) → Detect → Structure → Emit
Decision Engine (Ritesh) → Analyze → Decide
Control Plane (Shivam) → Execute → Enforce

Key Features:
Deterministic monitoring (no randomness)
Fixed schema output
Control-loop compatible
Structured logging
Plug-and-play integration

Services:
Service	   Port
web1	     5001
web2	     5002
executer	 5003
monitor	   5004


API Endpoints:
1. Health Check
GET /health

2. Metrics (Core Output)
GET /metrics
Output Schema:
{
  "service_id": "string",
  "timestamp": "UTC ISO",
  "status": "healthy | degraded | critical",
  "metrics": {
    "cpu": float,
    "memory": float,
    "error_rate": float,
    "uptime": int
  },
  "issue_detected": boolean,
  "issue_type": "cpu_spike | memory_leak | crash | none",
  "recommended_action": "noop | restart | scale_up | scale_down"
}


3. Runtime Payload (Decision Input)
GET /internal/runtime-payload
{
  "cpu_usage": float,
  "memory_usage": float,
  "error_rate": float,
  "health_score": float,
  "environment": "docker"
}


4. Execute Action
POST /execute-action
Input:
{
  "service_id": "web1",
  "action": "restart",
  "source": "decision_engine"
}

Output:
{
  "execution_id": "uuid",
  "status": "executed",
  "reason": "restart applied successfully"
}


Integration Flow
Monitoring detects issue
/metrics emits structured data
Decision engine reads runtime payload
Action generated
/execute-action triggered
Action executed and logged

Logging
Monitor Logs
DETECTION
RECOMMENDATION
Executer Logs:
ACTION_RECEIVED
ACTION_ACCEPTED
ACTION_EXECUTED

Docker Setup:
Pull Images
docker pull rayyandevopss/monitor-service:latest
docker pull rayyandevopss/executer-service:latest
docker pull rayyandevopss/web1-service:latest
docker pull rayyandevopss/web2-service:latest


Run System
docker-compose up


Stop System
docker-compose down


Kubernetes Deployment:
kubectl apply -f web1.yaml
kubectl apply -f web2.yaml
kubectl apply -f executer.yaml
kubectl apply -f monitor.yaml

Expose monitor:
kubectl port-forward service/monitor 5004:5004


Testing:
Simulate Failure
docker stop web1

Check Metrics
http://localhost:5004/metrics

Execute Action (PowerShell)
Invoke-RestMethod -Uri "http://localhost:5003/execute-action" `
-Method Post `
-Headers @{"Content-Type"="application/json"} `
-Body '{
  "service_id": "web1",
  "action": "restart",
  "source": "decision_engine"
}'


Outcome:
A deterministic monitoring system integrated into a control loop, capable of driving real-time infrastructure decisions.


