# monitor/app.py — PRAVAH (Observability + Signal Layer)

from flask import Flask, request, jsonify
import time

app = Flask(__name__)

# ─────────────────────────────────────────────────────────────
# SIGNAL GENERATOR (STANDARD CONTRACT)
# ─────────────────────────────────────────────────────────────
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


# ─────────────────────────────────────────────────────────────
# METRICS ENGINE
# ─────────────────────────────────────────────────────────────
@app.route("/metrics", methods=["GET"])
def metrics():
    import random

    latency = random.randint(100, 900)
    error_rate = round(random.uniform(0, 1), 2)

    data = {
        "latency": latency,
        "error_rate": error_rate,
        "status": "healthy"
    }

    print(f"[PRAVAH METRICS] {data}", flush=True)
    return jsonify(data)


# ─────────────────────────────────────────────────────────────
# SIGNAL EMISSION (CORE)
# ─────────────────────────────────────────────────────────────
@app.route("/emit-signal", methods=["POST"])
def emit_signal():
    data = request.get_json()

    trace_id = data.get("trace_id", "unknown")
    latency = data.get("latency", 0)
    error_rate = data.get("error_rate", 0)

    # ─── DETERMINISTIC SIGNAL LOGIC ───
    if latency > 700:
        signal_type = "latency_spike"
        severity = "HIGH"
        recommended_action = "scale_up"

    elif error_rate > 0.5:
        signal_type = "health_degradation"
        severity = "MEDIUM"
        recommended_action = "restart"

    elif latency < 300 and error_rate < 0.2:
        signal_type = "normal"
        severity = "LOW"
        recommended_action = "none"

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
            "error_rate": error_rate
        },
        recommended_action
    )

    # ─── LOG SIGNAL (NO EXECUTION) ───
    print(f"[PRAVAH SIGNAL EMITTED] {signal}", flush=True)

    # ─── ALERT (NO EXECUTION) ───
    if severity == "HIGH":
        print(f"[ALERT] High severity issue detected: {signal_type}", flush=True)

    return jsonify(signal)


# ─────────────────────────────────────────────────────────────
# HEALTH CHECK
# ─────────────────────────────────────────────────────────────
@app.route("/health")
def health():
    return jsonify({"status": "pravah_running"})


# ─────────────────────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5004)