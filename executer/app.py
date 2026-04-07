from flask import Flask, request, jsonify
import uuid
import time

from governance import validate_deployment_request
from core import execute_action, verify_deployment
from bucket import log_event
from outcome import record_outcome

app = Flask(__name__)

VALID_ACTIONS = {"restart", "scale_up", "scale_down", "noop"}


@app.route("/execute-action", methods=["POST"])
def execute():
    data = request.get_json()

    service_id = data.get("service_id")
    action = data.get("action")
    decision = data.get("decision")   # decision comes from Sarathi
    metrics = data.get("metrics", {})

    trace_id = data.get("trace_id", str(uuid.uuid4()))

    if not service_id or not action:
        return jsonify({"error": "missing fields"}), 400

    # STAGE 1 — DECISION RECEIVED
    log_event(trace_id, "decision_received", {
        "decision": decision,
        "service_id": service_id,
        "action": action
    })

    if decision != "ALLOW":
        return jsonify({
            "trace_id": trace_id,
            "status": "blocked_by_decision"
        })

    # STAGE 2 — GOVERNANCE
    gov = validate_deployment_request(service_id, action)

    log_event(trace_id, "governance", {
        "decision": gov
    })

    if gov == "BLOCK":
        return jsonify({
            "trace_id": trace_id,
            "status": "blocked_by_governance"
        })

    # STAGE 3 — EXECUTION
    start = time.time()
    result = execute_action(service_id, action)
    latency = time.time() - start

    success = not result.startswith("ERROR")

    log_event(trace_id, "execution", {
        "result": result,
        "latency": latency
    })

    # STAGE 4 — VERIFY
    verified = verify_deployment(service_id)

    # STAGE 5 — OUTCOME
    outcome = record_outcome(
        trace_id=trace_id,
        success=success,
        latency=latency,
        action=action,
        service_id=service_id
    )

    log_event(trace_id, "final_status", outcome)

    return jsonify({
        "trace_id": trace_id,
        "status": "success" if success else "failed",
        "verified": verified
    })


@app.route("/health")
def health():
    return jsonify({"status": "healthy"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003)