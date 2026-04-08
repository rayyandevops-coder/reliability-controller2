# monitor/app.py — PRAVAH (Observability + Signal Layer)

from flask import Flask, request, jsonify
import time

app = Flask(__name__)

# ─────────────────────────────────────────────
# STANDARD SIGNAL CONTRACT
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
# METRICS ENGINE
# ─────────────────────────────────────────────
@app.route("/metrics")
def metrics():
    import random

    latency = random.randint(100, 900)
    error_rate = round(random.uniform(0, 1), 2)
    pod_health = "healthy" if latency < 700 else "degraded"

    data = {
        "latency": latency,
        "error_rate": error_rate,
        "pod_health": pod_health
    }

    print(f"[PRAVAH METRICS] {data}", flush=True)
    return jsonify(data)

# ─────────────────────────────────────────────
# SIGNAL EMISSION (NO EXECUTION)
# ─────────────────────────────────────────────
@app.route("/emit-signal", methods=["POST"])
def emit_signal():
    data = request.get_json()

    trace_id = data.get("trace_id", "unknown")
    latency = data.get("latency", 0)
    error_rate = data.get("error_rate", 0)
    deployment_status = data.get("deployment_status", "success")

    # ─── DETERMINISTIC SIGNALS ───
    if deployment_status == "failed":
        signal_type = "deployment_failure"
        severity = "HIGH"
        recommended_action = "rollback"

    elif latency > 700:
        signal_type = "latency_spike"
        severity = "HIGH"
        recommended_action = "scale_up"

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

    print(f"[PRAVAH SIGNAL EMITTED] {signal}", flush=True)

    if severity == "HIGH":
        print(f"[ALERT] {signal_type} detected trace={trace_id}", flush=True)

    return jsonify(signal)

@app.route("/health")
def health():
    return jsonify({"status": "pravah_running"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5004)