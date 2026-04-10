from flask import Flask, request, jsonify, Response
import random

from signal_builder import build_signal
from sources.infra import generate_infra_signals
from sources.cicd import generate_cicd_signals
from sources.app_metrics import generate_app_signals
from sources.executer_logs import generate_executer_signals
from deployment_status import get_deployment_status

from aggregator import aggregate_signals
from streamer import stream_signals

app = Flask(__name__)


@app.route("/metrics")
def metrics():
    return jsonify({
        "latency": random.randint(100, 900),
        "error_rate": round(random.uniform(0, 1), 2)
    })


def generate_all_signals():
    trace_id = str(random.randint(100, 999))

    latency = random.randint(100, 900)
    error_rate = round(random.uniform(0, 1), 2)

    deployment_status = get_deployment_status()["status"]

    raw = []

    raw += generate_app_signals(trace_id, latency, error_rate)
    raw += generate_cicd_signals(trace_id, deployment_status)
    raw += generate_infra_signals(trace_id, latency)
    raw += generate_executer_signals(trace_id)

    built = [
        build_signal(st, svc, metric, val, trace_id)
        for (st, svc, metric, val) in raw
    ]

    return built


@app.route("/emit-signal", methods=["POST"])
def emit_signal():
    try:
        data = request.get_json()

        trace_id = data.get("trace_id", None)
        latency = data.get("latency", 0)
        error_rate = data.get("error_rate", 0)

        deployment_status = get_deployment_status()["status"]

        raw = []
        raw += generate_app_signals(trace_id, latency, error_rate)
        raw += generate_cicd_signals(trace_id, deployment_status)
        raw += generate_infra_signals(trace_id, latency)
        raw += generate_executer_signals(trace_id)

        built = [
            build_signal(st, svc, metric, val, trace_id)
            for (st, svc, metric, val) in raw
        ]

        aggregated = aggregate_signals(built)

        return jsonify(aggregated)

    except Exception as e:
        return jsonify({"error": str(e)}), 400


# 🔥 STREAM ENDPOINT
@app.route("/signals/stream")
def stream():
    return Response(
        stream_signals(generate_all_signals),
        mimetype="text/event-stream"
    )


@app.route("/health")
def health():
    return jsonify({"status": "pravah_running"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5004)