# monitor/app.py — FINAL PRAVAH (TANTRA COMPLIANT)

from flask import Flask, request, jsonify
import time
import random

app = Flask(__name__)

# ─────────────────────────────────────────────
# SIGNAL GENERATOR
# ─────────────────────────────────────────────
def generate_signal(trace_id, signal_type, severity, metrics, recommended_action):
    return {
        "trace_id": trace_id,
        "signal_type": signal_type,
        "severity": severity,
        "source": "pravah",
        "metrics": metrics,
        "recommended_action": recommended_action,
        "timestamp": int(time.time())
    }

# ─────────────────────────────────────────────
# METRICS ENGINE (DETECT + MEASURE ONLY)
# ─────────────────────────────────────────────
@app.route("/metrics")
def metrics():
    latency = random.randint(100, 900)
    error_rate = round(random.uniform(0, 1), 2)
    pod_health = "healthy" if latency < 700 else "degraded"

    data = {
        "latency": latency,
        "error_rate": error_rate,
        "pod_health": pod_health
    }

    print({
        "event": "METRICS_COLLECTED",
        "trace_id": "N/A",
        "metrics": data
    }, flush=True)

    return jsonify(data)

# ─────────────────────────────────────────────
# SIGNAL EMISSION (NO EXECUTION)
# ─────────────────────────────────────────────
@app.route("/emit-signal", methods=["POST"])
def emit_signal():
    data = request.get_json()

    trace_id = data.get("trace_id")
    latency = data.get("latency", 0)
    error_rate = data.get("error_rate", 0)
    deployment_status = data.get("deployment_status", "success")

    # 🔥 DETERMINISTIC SIGNAL LOGIC
    if deployment_status == "failed":
        signal_type = "deployment_failure"
        severity = "HIGH"
        recommended_action = "rollback"

    elif latency > 700:
        signal_type = "latency_spike"
        severity = "HIGH"
        recommended_action = "scale"

    elif error_rate > 0.5:
        signal_type = "health_degradation"
        severity = "MEDIUM"
        recommended_action = "restart"

    else:
        signal_type = "anomaly_detected"
        severity = "LOW"
        recommended_action = "observe"

    signal = generate_signal(
        trace_id,
        signal_type,
        severity,
        {
            "latency": latency,
            "error_rate": error_rate,
            "deployment_status": deployment_status
        },
        recommended_action
    )

    print({
        "event": "SIGNAL_EMITTED",
        "trace_id": trace_id,
        "signal": signal
    }, flush=True)

    # ALERT (ONLY LOG — NO ACTION)
    if severity == "HIGH":
        print({
            "event": "ALERT",
            "trace_id": trace_id,
            "signal_type": signal_type
        }, flush=True)

    return jsonify(signal)

@app.route("/health")
def health():
    return jsonify({"status": "pravah_running"})