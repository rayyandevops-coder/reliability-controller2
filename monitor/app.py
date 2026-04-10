from flask import Flask, request, jsonify
import random

from signal_builder import build_signal
from sources.infra import generate_infra_signals
from sources.cicd import generate_cicd_signals
from sources.app_metrics import generate_app_signals
from deployment_status import get_deployment_status

app = Flask(__name__)


@app.route("/metrics")
def metrics():
    return jsonify({
        "latency": random.randint(100, 900),
        "error_rate": round(random.uniform(0, 1), 2)
    })


@app.route("/emit-signal", methods=["POST"])
def emit_signal():
    try:
        data = request.get_json()

        trace_id = data.get("trace_id", None)
        latency = data.get("latency", 0)
        error_rate = data.get("error_rate", 0)

        # CI/CD source
        deployment_data = get_deployment_status()
        deployment_status = deployment_data["status"]

        raw_signals = []

        raw_signals += generate_app_signals(trace_id, latency, error_rate)
        raw_signals += generate_cicd_signals(trace_id, deployment_status)
        raw_signals += generate_infra_signals(trace_id, latency)

        final_signals = [
            build_signal(st, svc, metric, val, trace_id)
            for (st, svc, metric, val) in raw_signals
        ]

        return jsonify(final_signals)

    except Exception as e:
        return jsonify({
            "error": "Signal processing failed",
            "details": str(e)
        }), 400


@app.route("/health")
def health():
    return jsonify({"status": "pravah_running"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5004)