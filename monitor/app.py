from deployment_status import deployment_bp
from flask import Flask, jsonify
import requests
import time
import json
import logging
import psutil
import os
import threading
import sys

app = Flask(__name__)

ENV = os.getenv("ENV", "DEV")
EXECUTER_URL = os.getenv("EXECUTER_URL", "http://executer-service:5003")
POLL_INTERVAL = int(os.getenv("POLL_INTERVAL", "10"))  # seconds

# ─── Services to monitor ──────────────────────────────────────────────────────
services = {
    "web1":    "http://web1-service:5001/health",
    "web2":    "http://web2-service:5002/health",
    "executer": "http://executer-service:5003/health"
}

# ─── Logger (stdout — visible in kubectl logs) ────────────────────────────────
logger = logging.getLogger("monitor")
logger.setLevel(logging.INFO)
if not logger.handlers:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(handler)


def log(event, **kwargs):
    entry = {"event": event, "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"), **kwargs}
    print(json.dumps(entry), flush=True)


# ─── Core monitoring logic ────────────────────────────────────────────────────
def check_services():
    cpu    = round(psutil.cpu_percent(interval=1) / 100, 2)
    memory = round(psutil.virtual_memory().percent / 100, 2)

    for service_id, url in services.items():
        status     = "healthy"
        error_rate = 0.0
        action     = "noop"

        try:
            start   = time.time()
            res     = requests.get(url, timeout=2)
            latency = int((time.time() - start) * 1000)

            if res.status_code != 200:
                # Service returned non-200 → treat as crash
                status     = "critical"
                error_rate = 1.0
                action     = "restart"

            elif latency > 500:
                # Service is slow → needs more capacity
                status = "degraded"
                action = "scale_up"

        except Exception:
            # Connection refused / timeout → service is down
            status     = "critical"
            error_rate = 1.0
            action     = "restart"

        # Always log the detection event
        log("DETECTION", service=service_id, status=status, action=action,
            cpu=cpu, memory=memory, error_rate=error_rate)

        # Only call executer if action is needed
        if action == "noop":
            continue

        payload = {
            "service_id": service_id,
            "action":     action,
            "metrics": {
                "cpu":        cpu,
                "memory":     memory,
                "error_rate": error_rate
            }
        }

        try:
            response = requests.post(
                f"{EXECUTER_URL}/execute-action",
                json=payload,
                timeout=5
            )
            log("EXECUTION_TRIGGERED", service=service_id,
                action=action, response=response.json())

        except Exception as e:
            log("EXECUTION_FAILED", service=service_id, error=str(e))


# ─── Background loop ──────────────────────────────────────────────────────────
def monitor_loop():
    log("MONITOR_STARTED", interval_seconds=POLL_INTERVAL)
    while True:
        try:
            check_services()
        except Exception as e:
            log("MONITOR_ERROR", error=str(e))
        time.sleep(POLL_INTERVAL)


# ─── HTTP endpoints ───────────────────────────────────────────────────────────
@app.route("/metrics")
def metrics():
    """Manual trigger — also returns current status."""
    results = []
    cpu    = round(psutil.cpu_percent(interval=1) / 100, 2)
    memory = round(psutil.virtual_memory().percent / 100, 2)

    for service_id, url in services.items():
        status     = "healthy"
        error_rate = 0.0
        action     = "noop"
        try:
            start   = time.time()
            res     = requests.get(url, timeout=2)
            latency = int((time.time() - start) * 1000)
            if res.status_code != 200:
                status = "critical"; error_rate = 1.0; action = "restart"
            elif latency > 500:
                status = "degraded"; action = "scale_up"
        except Exception:
            status = "critical"; error_rate = 1.0; action = "restart"

        results.append({
            "service_id": service_id,
            "status": status,
            "action": action,
            "metrics": {"cpu": cpu, "memory": memory, "error_rate": error_rate}
        })

    return jsonify(results)


@app.route("/health")
def health():
    return jsonify({"status": "healthy", "env": ENV})


# ─── Start ────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # Start background monitoring thread
    t = threading.Thread(target=monitor_loop, daemon=True)
    t.start()

    app.run(host="0.0.0.0", port=5004, use_reloader=False)

app.register_blueprint(deployment_bp)