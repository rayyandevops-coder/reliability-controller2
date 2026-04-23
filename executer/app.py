from flask import Flask, request, jsonify
import time
import requests
import os
import subprocess
import uuid

from governance import validate_deployment_request
from mitra import calculate_score

app = Flask(__name__)

SARATHI_URL = os.getenv("SARATHI_URL", "http://sarathi-service:5001/decision")
MONITOR_URL = os.getenv("MONITOR_URL", "http://monitor-service:5004/track-event")

# 🔒 SAFETY (ONLY ALLOWED TARGETS)
ALLOWED_SERVICES = ["web1-blue", "web1-green", "web2-blue", "web2-green"]
ALLOWED_ACTIONS = ["restart", "scale"]


# =========================
# REAL EXECUTION FUNCTION
# =========================
def execute_action(service, action, trace_id):
    try:
        if service not in ALLOWED_SERVICES:
            return {"status": "blocked", "reason": "invalid service"}

        if action not in ALLOWED_ACTIONS:
            return {"status": "blocked", "reason": "invalid action"}

        # =========================
        # 🔥 REAL EXECUTION (FORCED)
        # =========================
        if action == "restart":
            cmd = [
                "kubectl",
                "patch",
                f"deployment/{service}",
                "-n", "prod",
                "-p",
                '{"spec":{"template":{"metadata":{"annotations":{"restart-time":"' + str(time.time()) + '"}}}}}'
            ]

        elif action == "scale":
            cmd = [
                "kubectl",
                "scale",
                f"deployment/{service}",
                "--replicas=2",
                "-n", "prod"
            ]

        else:
            return {"status": "error", "message": "unsupported action"}

        print(f"[REAL EXECUTION] trace={trace_id} service={service} action={action}", flush=True)

        start = time.time()

        result = subprocess.run(cmd, capture_output=True, text=True)

        latency = time.time() - start

        return {
            "status": "success" if result.returncode == 0 else "failed",
            "output": result.stdout.strip(),
            "error": result.stderr.strip(),
            "latency": latency
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
# =========================
# VERIFY DEPLOYMENT
# =========================
def verify_rollout(service):
    try:
        cmd = [
            "kubectl",
            "rollout",
            "status",
            f"deployment/{service}",
            "-n",
            "prod"
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        return result.stdout.strip()

    except Exception as e:
        return str(e)


# =========================
# EXECUTION ENDPOINT
# =========================
@app.route("/execute-action", methods=["POST"])
def execute():
    data = request.get_json(force=True)

    trace_id = data.get("trace_id")
    service_id = data.get("service_id")
    action = data.get("action")

    if not trace_id:
        return jsonify({"error": "trace_id required"}), 400

    print(f"[EXECUTION REQUEST] trace_id={trace_id}", flush=True)

    # =========================
    # STEP 1 — MITRA
    # =========================
    score = calculate_score(data.get("metrics", {}))

    # =========================
    # STEP 2 — SARATHI
    # =========================
    res = requests.post(SARATHI_URL, json={
        "trace_id": trace_id,
        "payload": score,
        "action_type": action
    }).json()

    if res.get("status") != "ALLOW":
        return jsonify({
            "trace_id": trace_id,
            "status": "blocked",
            "decision": res.get("status")
        })

    # =========================
    # STEP 3 — GOVERNANCE
    # =========================
    gov = validate_deployment_request(service_id, action)
    if gov == "BLOCK":
        return jsonify({
            "trace_id": trace_id,
            "status": "blocked_by_governance"
        })

    # =========================
    # STEP 4 — REAL EXECUTION
    # =========================
    execution_id = str(uuid.uuid4())

    exec_result = execute_action(service_id, action, trace_id)

    verification = verify_rollout(service_id)

    print(f"[EXECUTION RESULT] trace={trace_id} result={exec_result}", flush=True)

    # =========================
    # STEP 5 — SEND EVENT TO MONITOR (TRACE LINK)
    # =========================
    try:
        requests.post(MONITOR_URL, json={
            "user_id": "system",
            "event_type": "execution_done",
            "timestamp": int(time.time()),
            "session_id": "system",
            "trace_id": trace_id,
            "execution_id": execution_id,
            "service": service_id,
            "action": action,
            "latency": exec_result.get("latency"),
            "status": exec_result.get("status")
        })
    except Exception as e:
        print(f"[MONITOR ERROR] {e}", flush=True)

    # =========================
    # FINAL RESPONSE
    # =========================
    return jsonify({
        "execution_id": execution_id,
        "trace_id": trace_id,
        "status": exec_result.get("status"),
        "latency": exec_result.get("latency"),
        "output": exec_result.get("output"),
        "error": exec_result.get("error"),
        "verification": verification
    })


# =========================
# HEALTH
# =========================
@app.route("/health")
def health():
    return {"status": "ok"}


# =========================
# MAIN
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003)