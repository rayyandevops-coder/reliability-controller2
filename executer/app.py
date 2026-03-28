from flask import Flask, request, jsonify
import uuid
import json
import logging
from datetime import datetime, timedelta
import subprocess

app = Flask(__name__)

logging.basicConfig(
    filename="executer.log",
    level=logging.INFO,
    format='%(message)s'
)

VALID_ACTIONS = ["restart", "scale_up", "scale_down", "noop"]

# Cooldown tracker (Task 4 safety)
cooldowns = {}
COOLDOWN_TIME = 10  # seconds

# ---------------- LOGGER ----------------
def log_event(event_type, service_id, action, result):
    log = {
        "timestamp": datetime.utcnow().isoformat(),
        "event": event_type,
        "service_id": service_id,
        "action": action,
        "result": result
    }
    logging.info(json.dumps(log))

# ---------------- EXECUTION LOGIC ----------------
def execute_real_action(service_id, action):
    try:
        if action == "restart":
            subprocess.run(["kubectl", "rollout", "restart", f"deployment/{service_id}"], check=True)

        elif action == "scale_up":
            subprocess.run(["kubectl", "scale", f"deployment/{service_id}", "--replicas=2"], check=True)

        elif action == "scale_down":
            subprocess.run(["kubectl", "scale", f"deployment/{service_id}", "--replicas=1"], check=True)

        return "success"

    except Exception as e:
        return str(e)

# ---------------- EXECUTE ACTION ----------------
@app.route("/execute-action", methods=["POST"])
def execute_action():
    data = request.get_json()

    service_id = data.get("service_id")
    action = data.get("action")

    execution_id = str(uuid.uuid4())

    log_event("ACTION_RECEIVED", service_id, action, "incoming")

    # VALIDATION
    if action not in VALID_ACTIONS:
        log_event("ACTION_REJECTED", service_id, action, "invalid")

        return jsonify({
            "execution_id": execution_id,
            "status": "rejected",
            "reason": "invalid action"
        }), 400

    # COOLDOWN CHECK
    now = datetime.utcnow()
    if service_id in cooldowns and now < cooldowns[service_id]:
        log_event("ACTION_BLOCKED", service_id, action, "cooldown")

        return jsonify({
            "execution_id": execution_id,
            "status": "blocked",
            "reason": "cooldown active"
        }), 429

    cooldowns[service_id] = now + timedelta(seconds=COOLDOWN_TIME)

    log_event("ACTION_ACCEPTED", service_id, action, "valid")

    # REAL EXECUTION
    result = execute_real_action(service_id, action)

    log_event("ACTION_EXECUTED", service_id, action, result)

    return jsonify({
        "execution_id": execution_id,
        "status": result,
        "service_id": service_id,
        "action": action
    })

# ---------------- HEALTH ----------------
@app.route("/health")
def health():
    return jsonify({"status": "healthy"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003)