Integration Readiness Hardening — Monitoring & Execution Layer

Overview:
This project implements a deterministic monitoring and execution system designed for integration into a distributed control loop architecture.
The system acts as:
Monitoring + Signal Layer → Detects system state and emits structured signals
Execution Layer → Accepts external control and performs validated actions

Objective:
To convert an existing system into a:
Deterministic
Structured
Externally controlled
Safe and auditable module

Architecture:
Monitor → Emits signals
↓
Decision System (external)
↓
Control Plane (external)
↓
Executer → Executes actions

Services
Service  	Port	Description
web1	    5001	Sample service
web2	    5002	Sample service
executer	5003	Executes actions
monitor	    5004	Emits metrics


How to Run
1. Build & Start
docker-compose down
docker-compose up --build


2. Access Services
Monitor:
http://localhost:5004/metrics

Executer:
http://localhost:5003/execute-action


API Endpoints:

/health
Returns system health
{
  "status": "healthy"
}


/metrics (GET)
Returns deterministic system state
{
  "service_id": "web1",
  "status": "critical",
  "issue_type": "crash",
  "recommended_action": "restart"
}


/execute-action (POST)
Request:
{
  "service_id": "web1",
  "action": "restart"
}

Response:
{
  "status": "SUCCESS",
  "service_id": "web1",
  "action": "restart"
}


Safety Features:
✅ Cooldown system (prevents repeated actions)
✅ Rate limiting (max requests per window)
✅ Strict input validation
✅ Structured JSON logging
❌ No auto-recovery (external control only)

Logging:
All logs are structured JSON:
Detection logs
Recommendation logs
Action requests
Execution results

Design Principle:
The system does not take decisions or auto-heal.
It emits signals and waits for external control.

Outcome:
A deterministic, integration-ready monitoring system suitable for real-world distributed environments.


