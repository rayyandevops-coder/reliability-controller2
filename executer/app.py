"""
executer/app.py — BHIV CORRECT EXECUTION ENGINE
Flow: Mitra → Sarathi → Governance → Execution → Logging
"""

from flask import Flask, request, jsonify
import uuid
import time

from governance import validate_deployment_request
from mitra import calculate_score
from sovereign_bridge import send_to_sarathi
from core import execute_action, verify_deployment
from bucket import log_event
from outcome import record_outcome

app = Flask(__name__)

VALID_ACTIONS = {"restart", "scale_up", "scale_down", "noop"}


@app.route("/execute-action", methods=["POST"])
def execute():
    data       = request.get_json()
    service_id = data.get("service_id")
    action     = data.get("action", "noop")
    metrics    = data.get("metrics", {})
    trace_id   = str(uuid.uuid4())

    if not service_id:
        return jsonify({"error": "service_id required"}), 400

    if action not in VALID_ACTIONS:
        return jsonify({"error": f"invalid action: {action}"}), 400

    if action == "noop":
        return jsonify({"trace_id": trace_id, "status": "noop"})

    # STAGE 1 — Proposal
    log_event(trace_id, "proposal_created", {
        "service_id": service_id,
        "action": action,
        "metrics": metrics
    })

    # STAGE 2 — Mitra
    score_data = calculate_score(metrics)
    data.update(score_data)
    log_event(trace_id, "proposal_scored", score_data)

    # STAGE 3 — Sarathi (DECISION FIRST)
    sarathi_payload = {
        "trace_id": trace_id,
        "action_type": action,
        "service_id": service_id,
        "source": "SETU",
        "payload": {
            **data,
            "decision_score": score_data["decision_score"]
        }
    }

    decision = send_to_sarathi(sarathi_payload)
    log_event(trace_id, "sarathi_decision", decision)

    sarathi_status = decision.get("status", "ERROR")

    if sarathi_status != "ALLOW":
        return jsonify({
            "trace_id": trace_id,
            "status": sarathi_status.lower()
        })

    # STAGE 4 — GOVERNANCE (FINAL CONTROL)
    governance_decision = validate_deployment_request(service_id, action)
    log_event(trace_id, "governance_decision", {"decision": governance_decision})

    if governance_decision == "BLOCK":
        return jsonify({
            "trace_id": trace_id,
            "status": "blocked_by_governance"
        }), 403

    # STAGE 5 — EXECUTION
    start = time.time()
    result = execute_action(service_id, action)
    latency = time.time() - start

    success = not result.startswith("ERROR")
    status  = "success" if success else "failed"

    log_event(trace_id, "execution_result", {
        "service_id": service_id,
        "action": action,
        "result": result,
        "status": status,
        "latency": latency
    })

    # STAGE 6 — VERIFY
    verified = verify_deployment(service_id)

    # STAGE 7 — OUTCOME
    outcome = record_outcome(
        trace_id=trace_id,
        success=success,
        latency=latency,
        action=action,
        service_id=service_id
    )

    log_event(trace_id, "outcome", outcome)

    return jsonify({
        "trace_id": trace_id,
        "status": status,
        "deployment_type": "automated_action",
        "result": result,
        "verified": verified,
        "metrics": {
            "latency": latency,
            "success": success
        }
    })


@app.route("/health")
def health():
    return jsonify({"status": "healthy"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003, use_reloader=False)