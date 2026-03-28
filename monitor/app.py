from flask import Flask, jsonify
import requests
import time
import json
import logging
import psutil
import os

app = Flask(__name__)

# ---------------- CONFIG ----------------
ENV = os.getenv("ENV", "DEV")

services = {
    "web1": "http://web1-service:5001/health",
    "web2": "http://web2-service:5002/health",
    "executer": "http://executer-service:5003/health"
}

# ---------------- LOGGING ----------------
logger = logging.getLogger()
logger.setLevel(logging.INFO)

if not logger.handlers:
    fh = logging.FileHandler("monitor.log")
    ch = logging.StreamHandler()

    formatter = logging.Formatter('%(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)

# ---------------- METRICS ----------------
@app.route("/metrics")
def metrics():
    results = []

    system_cpu = psutil.cpu_percent(interval=1) / 100
    system_memory = psutil.virtual_memory().percent / 100

    for service_id in sorted(services.keys()):
        url = services[service_id]

        status = "healthy"
        error_rate = 0.0

        try:
            start = time.time()
            response = requests.get(url, timeout=3)
            latency = int((time.time() - start) * 1000)

            if response.status_code != 200:
                status = "critical"
                error_rate = 1.0

            elif latency > 500:
                status = "degraded"

        except:
            status = "critical"
            error_rate = 1.0

        timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ")

        output = {
            "service_id": service_id,
            "timestamp": timestamp,
            "status": status,
            "cpu": round(system_cpu, 2),
            "memory": round(system_memory, 2),
            "error_rate": error_rate,
            "env": ENV
        }

        # DETECTION LOG ONLY (NO DECISION)
        logging.info(json.dumps({
            "timestamp": timestamp,
            "event": "DETECTION",
            "service_id": service_id,
            "status": status,
            "cpu": output["cpu"],
            "memory": output["memory"]
        }))

        results.append(output)

    return jsonify(results)

# ---------------- RUNTIME PAYLOAD ----------------
@app.route("/internal/runtime-payload")
def runtime_payload():
    cpu = psutil.cpu_percent(interval=1) / 100
    memory = psutil.virtual_memory().percent / 100

    status = "healthy"
    if cpu > 0.85 or memory > 0.85:
        status = "degraded"

    payload = {
        "cpu": round(cpu, 2),
        "memory": round(memory, 2),
        "status": status,
        "env": ENV
    }

    return jsonify(payload)

# ---------------- HEALTH ----------------
@app.route("/health")
def health():
    return jsonify({"status": "healthy"})

# ---------------- MAIN ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5004)