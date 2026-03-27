from flask import Flask, request, jsonify
import uuid
import json
import logging
from datetime import datetime

app = Flask(__name__)

logging.basicConfig(
    filename="executer.log",
    level=logging.INFO,
    format='%(message)s'
)

VALID_ACTIONS = ["restart", "scale_up", "scale_down", "noop"]

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

# ---------------- EXECUTE ACTION ----------------
@app.route("/execute-action", methods=["POST"])
def execute_action():
    data = request.get_json()

    service_id = data.get("service_id")
    action = data.get("action")
    source = data.get("source")

    execution_id = str(uuid.uuid4())

    # 🔹 STEP 1: ACTION RECEIVED
    log_event("ACTION_RECEIVED", service_id, action, source)

    # 🔹 STEP 2: VALIDATION
    if action not in VALID_ACTIONS:
        log_event("ACTION_REJECTED", service_id, action, "invalid_action")

        return jsonify({
            "execution_id": execution_id,
            "status": "rejected",
            "reason": "invalid action"
        }), 400

    # 🔹 STEP 3: ACCEPTED
    log_event("ACTION_ACCEPTED", service_id, action, "valid")

    # 🔹 STEP 4: EXECUTION (SIMULATED — CORRECT AS PER TASK)
    result = "executed"

    # 🔹 STEP 5: EXECUTED
    log_event("ACTION_EXECUTED", service_id, action, result)

    return jsonify({
        "execution_id": execution_id,
        "status": result,
        "reason": f"{action} applied successfully"
    })

# ---------------- HEALTH ----------------
@app.route("/health")
def health():
    return jsonify({"status": "healthy"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003)