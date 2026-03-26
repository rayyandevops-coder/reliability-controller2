from flask import Flask, jsonify
import requests
import time
import json
import logging

app = Flask(__name__)

# Deterministic service list
services = {
    "web1": "http://web1-service:5001/health",
    "web2": "http://web2-service:5002/health",
    "executer": "http://executer-service:5003/health"
}

# Logging setup
logging.basicConfig(
    filename="monitor.log",
    level=logging.INFO,
    format='%(message)s'
)


@app.route("/metrics")
def metrics():
    results = []

    for service_id in sorted(services.keys()):
        url = services[service_id]

        status = "healthy"
        issue_detected = False
        issue_type = "none"
        recommended_action = "noop"

        # Deterministic metrics (fixed values)
        cpu = 0.3
        memory = 0.5
        error_rate = 0.0
        uptime = 100

        try:
            start = time.time()
            response = requests.get(url, timeout=3)
            response_time = int((time.time() - start) * 1000)

            # Logic for degradation (deterministic rules)
            if response.status_code != 200:
                status = "critical"
                issue_detected = True
                issue_type = "crash"
                recommended_action = "restart"

            elif response_time > 500:
                status = "degraded"
                issue_detected = True
                issue_type = "cpu_spike"
                recommended_action = "scale_up"

        except Exception as e:
            status = "critical"
            issue_detected = True
            issue_type = "crash"
            recommended_action = "restart"

            error_message = str(e)
        else:
            error_message = None

        timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ")

        # Structured output
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

        # Structured logging (MANDATORY)
        log_entry = {
            "event": "DETECTION",
            "service_id": service_id,
            "status": status,
            "issue_type": issue_type,
            "recommended_action": recommended_action,
            "timestamp": timestamp,
            "error": error_message
        }

        logging.info(json.dumps(log_entry))

        results.append(output)

    return jsonify(results)


@app.route("/health")
def health():
    return jsonify({"status": "healthy"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5004)