from flask import Flask, request, jsonify
import time
import json
import logging
import subprocess

app = Flask(__name__)

# Allowed services and actions
ALLOWED_SERVICES = {"web1", "web2"}
ALLOWED_ACTIONS = {"restart", "scale_up", "scale_down", "noop"}

# Cooldown tracking
cooldown_tracker = {}
COOLDOWN_SECONDS = 10

# Rate limiting
request_log = []
RATE_LIMIT = 5
WINDOW_SECONDS = 60

# Logging setup
logging.basicConfig(
    filename="executer.log",
    level=logging.INFO,
    format='%(message)s'
)


def is_rate_limited():
    current_time = time.time()

    # Remove old entries
    while request_log and current_time - request_log[0] > WINDOW_SECONDS:
        request_log.pop(0)

    if len(request_log) >= RATE_LIMIT:
        return True

    request_log.append(current_time)
    return False


@app.route("/execute-action", methods=["POST"])
def execute_action():
    timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ")

    # RATE LIMIT CHECK
    if is_rate_limited():
        log_entry = {
            "event": "ACTION_REQUEST",
            "status": "FAILED",
            "reason": "RATE_LIMIT_EXCEEDED",
            "timestamp": timestamp
        }
        logging.info(json.dumps(log_entry))

        return jsonify({
            "status": "FAILED",
            "reason": "RATE_LIMIT_EXCEEDED",
            "timestamp": timestamp
        }), 429

    data = request.json

    service_id = data.get("service_id")
    action = data.get("action")

    # LOG ACTION REQUEST
    logging.info(json.dumps({
        "event": "ACTION_REQUEST",
        "service_id": service_id,
        "action": action,
        "timestamp": timestamp
    }))

    # VALIDATION
    if service_id not in ALLOWED_SERVICES or action not in ALLOWED_ACTIONS:
        return jsonify({
            "status": "FAILED",
            "reason": "INVALID_INPUT",
            "timestamp": timestamp
        }), 400

    # COOLDOWN CHECK
    last_time = cooldown_tracker.get(service_id, 0)
    if time.time() - last_time < COOLDOWN_SECONDS:
        return jsonify({
            "status": "BLOCKED",
            "reason": "COOLDOWN_ACTIVE",
            "service_id": service_id,
            "timestamp": timestamp
        }), 403

    try:
        # EXECUTION (safe)
        if action == "restart":
            subprocess.run(["docker", "restart", service_id], check=True)

        # scale_up / scale_down / noop are simulated (as per task)
        
        cooldown_tracker[service_id] = time.time()

        # LOG SUCCESS
        logging.info(json.dumps({
            "event": "ACTION_EXECUTED",
            "service_id": service_id,
            "action": action,
            "status": "SUCCESS",
            "timestamp": timestamp
        }))

        return jsonify({
            "status": "SUCCESS",
            "service_id": service_id,
            "action": action,
            "timestamp": timestamp
        })

    except Exception as e:
        # LOG FAILURE
        logging.info(json.dumps({
            "event": "ACTION_EXECUTED",
            "service_id": service_id,
            "action": action,
            "status": "FAILED",
            "error": str(e),
            "timestamp": timestamp
        }))

        return jsonify({
            "status": "FAILED",
            "reason": "EXECUTION_ERROR",
            "timestamp": timestamp
        }), 500


@app.route("/health")
def health():
    return jsonify({"status": "healthy"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003)