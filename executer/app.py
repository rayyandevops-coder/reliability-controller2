from flask import Flask, request, jsonify
import time
import requests
import os

from governance import validate_deployment_request
from core import execute_action, verify_deployment
from mitra import calculate_score

app = Flask(__name__)

SARATHI_URL = os.getenv("SARATHI_URL", "http://sarathi-service:5001/decision")
MONITOR_URL = os.getenv("MONITOR_URL", "http://monitor-service:5004/track-event")


@app.route("/execute-action", methods=["POST"])
def execute():
    data = request.get_json(force=True)

    trace_id = data.get("trace_id")
    service_id = data.get("service_id")
    action = data.get("action")

    if not trace_id:
        return jsonify({"error": "trace_id required"}), 400

    print(f"[EXECUTION REQUEST] trace_id={trace_id}", flush=True)

    # STEP 1 — MITRA
    score = calculate_score(data.get("metrics", {}))

    # STEP 2 — SARATHI
    res = requests.post(SARATHI_URL, json={
        "trace_id": trace_id,
        "payload": score,
        "action_type": action
    }).json()

    if res.get("status") != "ALLOW":
        return jsonify({"trace_id": trace_id, "status": "blocked"})

    # STEP 3 — GOVERNANCE
    gov = validate_deployment_request(service_id, action)
    if gov == "BLOCK":
        return jsonify({"trace_id": trace_id, "status": "blocked_by_governance"})

    # STEP 4 — EXECUTION
    start = time.time()
    result = execute_action(service_id, action)
    latency = time.time() - start

    verified = verify_deployment(service_id)

    print(f"[EXECUTION RESULT] trace_id={trace_id} result={result}", flush=True)

    # 🔥 IMPORTANT: SEND EVENT TO MONITOR (REAL LINK)
    try:
        requests.post(MONITOR_URL, json={
            "user_id": "system",
            "event_type": "execution_done",
            "timestamp": int(time.time()),
            "session_id": "system",
            "trace_id": trace_id
        })
    except:
        pass

    return jsonify({
        "trace_id": trace_id,
        "result": result,
        "latency": latency,
        "verified": verified
    })


@app.route("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003)