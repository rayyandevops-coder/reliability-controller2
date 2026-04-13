from flask import Flask, request, jsonify, Response

from signal_builder import build_signal
from sources.infra import generate_infra_signals
from sources.cicd import generate_cicd_signals
from sources.app_metrics import generate_app_signals
from sources.executer_logs import generate_executer_signals
from deployment_status import get_deployment_status

from aggregator import aggregate_signals
from streamer import stream_signals

app = Flask(__name__)


# ✅ REAL INPUT METRICS (NO RANDOM)
@app.route("/metrics")
def metrics():
    latency = int(request.args.get("latency", 0))
    error_rate = float(request.args.get("error_rate", 0))
    trace_id = request.args.get("trace_id", None)

    return jsonify({
        "latency": latency,
        "error_rate": error_rate,
        "trace_id": trace_id
    })


# ✅ GENERATE SIGNALS FROM REAL INPUT
def generate_all_signals_from_input(trace_id, latency, error_rate):
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


# ✅ MAIN SIGNAL ENDPOINT (REAL DATA ONLY)
@app.route("/emit-signal", methods=["POST"])
def emit_signal():
    try:
        data = request.get_json()

        trace_id = data.get("trace_id")
        latency = data.get("latency")
        error_rate = data.get("error_rate")

        if trace_id is None:
            return jsonify({"error": "trace_id required"}), 400

        signals = generate_all_signals_from_input(trace_id, latency, error_rate)
        aggregated = aggregate_signals(signals)

        return jsonify(aggregated)

    except Exception as e:
        return jsonify({"error": str(e)}), 400


# ✅ STREAM USING LAST INPUT (NO RANDOM)
last_input = {
    "trace_id": "stream-1",
    "latency": 0,
    "error_rate": 0
}


@app.route("/update-stream", methods=["POST"])
def update_stream():
    data = request.get_json()

    last_input["trace_id"] = data.get("trace_id")
    last_input["latency"] = data.get("latency")
    last_input["error_rate"] = data.get("error_rate")

    return jsonify({"status": "updated"})


def stream_generator():
    while True:
        signals = generate_all_signals_from_input(
            last_input["trace_id"],
            last_input["latency"],
            last_input["error_rate"]
        )
        yield f"data: {signals}\n\n"


# 🔥 STREAM ENDPOINT (REAL DATA BASED)
@app.route("/signals/stream")
def stream():
    return Response(stream_generator(), mimetype="text/event-stream")


@app.route("/health")
def health():
    return jsonify({"status": "pravah_running"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5004)