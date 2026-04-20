from flask import Flask, request, jsonify
import uuid
import time
import requests
import os

from governance import validate_deployment_request
from core import execute_action, verify_deployment
from bucket import log_event
from outcome import record_outcome
from mitra import calculate_score

app = Flask(__name__)

SARATHI_URL = os.getenv("SARATHI_URL", "http://sarathi-service:5001/decision")


@app.route("/execute-action", methods=["POST"])
def execute():
    data = request.get_json(force=True)

    service_id = data.get("service_id")
    action = data.get("action")
    metrics = data.get("metrics", {})

    # 🔥 STRICT TRACE CONTINUITY
    trace_id = data.get("trace_id")
    if not trace_id:
        return jsonify({"error": "trace_id required"}), 400

    if not service_id or not action:
        return jsonify({"error": "missing fields"}), 400

    print(f"[EXECUTION START] trace_id={trace_id} service={service_id} action={action}", flush=True)

    # =========================
    # 🔹 STEP 1 — MITRA SCORE
    # =========================
    score_data = calculate_score(metrics)

    log_event(trace_id, "mitra_score", score_data)

    # =========================
    # 🔹 STEP 2 — SARATHI DECISION
    # =========================
    try:
        sarathi_res = requests.post(
            SARATHI_URL,
            json={
                "trace_id": trace_id,
                "action_type": action,
                "payload": score_data
            },
            timeout=3
        ).json()

    except Exception as e:
        log_event(trace_id, "sarathi_error", {"error": str(e)})
        return jsonify({
            "trace_id": trace_id,
            "status": "sarathi_unreachable"
        }), 500

    decision = sarathi_res.get("status")

    log_event(trace_id, "decision_received", {
        "decision": decision,
        "score": score_data
    })

    if decision != "ALLOW":
        return jsonify({
            "trace_id": trace_id,
            "status": "blocked",
            "decision": decision
        })

    # =========================
    # 🔹 STEP 3 — GOVERNANCE
    # =========================
    gov = validate_deployment_request(service_id, action)

    log_event(trace_id, "governance", {"decision": gov})

    if gov == "BLOCK":
        return jsonify({
            "trace_id": trace_id,
            "status": "blocked_by_governance"
        })

    # =========================
    # 🔹 STEP 4 — EXECUTION
    # =========================
    start = time.time()

    result = execute_action(service_id, action)
    latency = time.time() - start

    success = not result.startswith("ERROR")

    log_event(trace_id, "execution", {
        "result": result,
        "latency": latency
    })

    # =========================
    # 🔹 STEP 5 — VERIFY
    # =========================
    verified = verify_deployment(service_id)

    log_event(trace_id, "verification", {
        "verified": verified
    })

    # =========================
    # 🔹 STEP 6 — OUTCOME
    # =========================
    outcome = record_outcome(
        trace_id=trace_id,
        success=success,
        latency=latency,
        action=action,
        service_id=service_id
    )

    log_event(trace_id, "final_status", outcome)

    print(f"[EXECUTION END] trace_id={trace_id} success={success}", flush=True)

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