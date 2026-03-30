"""
executer/app.py — SETU Execution Engine
Full pipeline: proposal → Mitra scoring → Sarathi decision → Core execution
→ Bucket logging → Outcome recording
"""

from flask import Flask, request, jsonify
import uuid
import time
import json

from mitra           import calculate_score
from sovereign_bridge import send_to_sarathi
from core            import execute_action, verify_deployment
from bucket          import log_event
from outcome         import record_outcome

app = Flask(__name__)

VALID_ACTIONS = {"restart", "scale_up", "scale_down", "noop"}


@app.route("/execute-action", methods=["POST"])
def execute():
    data       = request.get_json()
    service_id = data.get("service_id")
    action     = data.get("action", "noop")
    metrics    = data.get("metrics", {})
    trace_id   = str(uuid.uuid4())

    # ── VALIDATION ────────────────────────────────────────────────────────────
    if not service_id:
        return jsonify({"error": "service_id required"}), 400

    if action not in VALID_ACTIONS:
        return jsonify({"error": f"invalid action: {action}"}), 400

    if action == "noop":
        return jsonify({"trace_id": trace_id, "status": "noop", "action": "noop"})

    # ── STAGE 1: proposal created ─────────────────────────────────────────────
    log_event(trace_id, "proposal_created", {
        "service_id": service_id,
        "action":     action,
        "metrics":    metrics
    })

    # ── STAGE 2: Mitra scoring ────────────────────────────────────────────────
    score_data = calculate_score(metrics)
    data.update(score_data)

    log_event(trace_id, "proposal_scored", score_data)

    # ── STAGE 3: Sarathi decision ─────────────────────────────────────────────
    sarathi_payload = {
        "trace_id":   trace_id,
        "action_type": action,
        "service_id": service_id,
        "source":     "SETU",
        "payload": {
            **data,
            "decision_score": score_data["decision_score"]
        }
    }

    decision = send_to_sarathi(sarathi_payload)

    log_event(trace_id, "sarathi_decision", decision)

    sarathi_status = decision.get("status", "ERROR")

    if sarathi_status == "BLOCK":
        return jsonify({
            "trace_id":        trace_id,
            "status":          "blocked",
            "sarathi_decision": sarathi_status,
            "reason":          decision.get("reason", "policy blocked this action")
        })

    if sarathi_status == "ESCALATE":
        return jsonify({
            "trace_id":        trace_id,
            "status":          "escalated",
            "sarathi_decision": sarathi_status,
            "reason":          "requires manual approval"
        })

    if sarathi_status == "ERROR":
        # Sarathi unreachable — fail safe (do NOT execute)
        return jsonify({
            "trace_id": trace_id,
            "status":   "sarathi_error",
            "reason":   decision.get("reason", "unknown")
        }), 503

    # sarathi_status == "ALLOW" — proceed to execution
    # ── STAGE 4: Core execution ───────────────────────────────────────────────
    start  = time.time()
    result = execute_action(service_id, action)
    latency = time.time() - start

    success = not result.startswith("ERROR")
    status  = "success" if success else "failed"

    log_event(trace_id, "execution_result", {
        "service_id": service_id,
        "action":     action,
        "result":     result,
        "status":     status
    })

    # ── STAGE 5: Verification ─────────────────────────────────────────────────
    verified = verify_deployment(service_id)

    # ── STAGE 6: Outcome (feedback loop) ─────────────────────────────────────
    outcome = record_outcome(
        trace_id=trace_id,
        success=success,
        latency=latency,
        action=action,
        service_id=service_id
    )

    log_event(trace_id, "outcome", outcome)

    return jsonify({
        "trace_id":        trace_id,
        "status":          status,
        "action":          action,
        "result":          result,
        "verified":        verified,
        "sarathi_decision": sarathi_status,
        "decision_score":  score_data["decision_score"],
        "priority":        score_data["priority"]
    })


@app.route("/health")
def health():
    return jsonify({"status": "healthy"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003, use_reloader=False)