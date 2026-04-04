The system is triggered by a push to the main branch. GitHub Actions acts as the entry point and initiates the CI/CD pipeline. The pipeline generates unique identifiers and begins deployment.

Trace Flow

Traceability is implemented across the entire pipeline. At the start of the pipeline, trace_id, execution_id, and deployment_id are generated. These identifiers are propagated through:

GitHub Actions logs
Kubernetes deployment steps
Executer service
Monitor service
Bucket logging system

Each log entry includes trace_id, allowing complete tracking of a deployment from start to finish.

Governance Flow

Before execution, every request passes through a governance validation layer implemented in executer/governance.py.

The function validate_deployment_request() applies deterministic rules to decide whether a deployment should proceed or be blocked.

If the decision is BLOCK:

execution stops immediately
no deployment changes occur
trace log records governance_decision event

If ALLOW:

request proceeds to Sarathi decision engine
execution continues normally

Observability Metrics

The system measures and logs key metrics including:

latency of execution
success or failure of deployment
error rate
service health status

Monitor service continuously checks system state and triggers actions when anomalies are detected.

Alerts are generated in case of:

deployment failure
service crash
execution errors

Structured logs are emitted in JSON format for all events.

One Real Deployment Trace (Example)

{
"trace_id": "abc123",
"event": "deployment_start",
"service": "web1"
}

{
"trace_id": "abc123",
"event": "governance_decision",
"decision": "ALLOW"
}

{
"trace_id": "abc123",
"event": "rollout_status",
"status": "successful"
}

{
"trace_id": "abc123",
"event": "final_status",
"result": "success"
}

Deployment Proof

The system successfully demonstrates:

staging to production flow
strict validation before production
automatic rollback on failure
alert generation on failure
structured trace logs
deployment metrics collection

Conclusion

The system has been successfully upgraded from a standard CI/CD pipeline to a BHIV-compliant execution system.