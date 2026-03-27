from flask import Flask, jsonify
import requests
import time
import json
import logging

app = Flask(__name__)

# ---------------- SERVICES ----------------
services = {
    "web1": "http://web1-service:5001/health",
    "web2": "http://web2-service:5002/health",
    "executer": "http://executer-service:5003/health"
}

# ---------------- LOGGING ----------------
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Prevent duplicate handlers
if not logger.handlers:
    file_handler = logging.FileHandler("monitor.log")
    file_handler.setFormatter(logging.Formatter('%(message)s'))

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter('%(message)s'))

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
# ---------------- DETECTION LOGIC ----------------
def analyze_metrics(cpu, memory, error_rate):
    if cpu > 0.85:
        return True, "cpu_spike", "scale_up"
    elif memory > 0.85:
        return True, "memory_leak", "restart"
    elif error_rate > 0.3:
        return True, "crash", "restart"
    else:
        return False, "none", "noop"

# ---------------- METRICS ----------------
@app.route("/metrics")
def metrics():
    results = []

    for service_id in sorted(services.keys()):
        url = services[service_id]

        # Deterministic base values
        cpu = 0.3
        memory = 0.5
        error_rate = 0.0
        uptime = 100
        status = "healthy"

        try:
            start = time.time()
            response = requests.get(url, timeout=3)
            response_time = int((time.time() - start) * 1000)

            # Deterministic rules
            if response.status_code != 200:
                status = "critical"
                error_rate = 1.0

            elif response_time > 500:
                status = "degraded"
                cpu = 0.9  # simulate spike

        except:
            status = "critical"
            error_rate = 1.0

        # Detection
        issue_detected, issue_type, recommended_action = analyze_metrics(cpu, memory, error_rate)

        timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ")

        # ---------------- OUTPUT ----------------
        output = {
            "service_id": service_id,
            "timestamp": timestamp,
            "status": status,
            "metrics": {
                "cpu": cpu,
                "memory": memory,
                "error_rate": error_rate,
                "uptime": uptime
            },
            "issue_detected": issue_detected,
            "issue_type": issue_type,
            "recommended_action": recommended_action
        }

        # ---------------- LOGGING ----------------

        # 1. DETECTION LOG
        logging.info(json.dumps({
            "timestamp": timestamp,
            "event": "DETECTION",
            "service_id": service_id,
            "status": status,
            "issue_type": issue_type
        }))

        # 2. RECOMMENDATION LOG (MANDATORY FIX)
        logging.info(json.dumps({
            "timestamp": timestamp,
            "event": "RECOMMENDATION",
            "service_id": service_id,
            "recommended_action": recommended_action
        }))

        results.append(output)

    return jsonify(results)

# ---------------- RUNTIME PAYLOAD ----------------
@app.route("/internal/runtime-payload")
def runtime_payload():
    # Deterministic mapping (fixed values)
    cpu = 0.3
    memory = 0.5
    error_rate = 0.0

    health_score = round(1 - max(cpu, memory, error_rate), 2)

    payload = {
        "cpu_usage": cpu,
        "memory_usage": memory,
        "error_rate": error_rate,
        "health_score": health_score,
        "environment": "docker"
    }

    return jsonify(payload)

# ---------------- HEALTH ----------------
@app.route("/health")
def health():
    return jsonify({"status": "healthy"})

# ---------------- MAIN ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5004, debug=False)