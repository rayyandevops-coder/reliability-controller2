import sys
sys.path.append(".")

from flask import Flask, request, jsonify, Response
import time
import json
from collections import defaultdict

from signal_builder import build_signal
from sources.infra import generate_infra_signals
from sources.cicd import generate_cicd_signals
from sources.app_metrics import generate_app_signals
from sources.executer_logs import generate_executer_signals
from deployment_status import get_deployment_status

app = Flask(__name__)

# =========================
# STORAGE
# =========================
user_events = []

# =========================
# EVENT TRACKING (STRICT)
# =========================
@app.route("/track-event", methods=["POST"])
def track_event():
    data = request.get_json(force=True, silent=True) or {}

    required = ["user_id", "event_type", "timestamp", "session_id", "trace_id"]

    for field in required:
        if field not in data:
            return jsonify({"error": f"{field} missing"}), 400

    user_events.append(data)

    print("[EVENT OK]", data, flush=True)

    return jsonify({"status": "event recorded"})


# =========================
# USER METRICS
# =========================
def compute_user_metrics():
    users = set()
    active_users = set()
    user_activity = defaultdict(int)
    login_counts = defaultdict(int)

    session_start = {}
    session_end = {}

    now = int(time.time())

    for e in user_events:
        u = e["user_id"]
        s = e["session_id"]

        users.add(u)

        if now - e["timestamp"] < 600:
            active_users.add(u)

        user_activity[u] += 1

        if e["event_type"] == "user_login":
            login_counts[u] += 1

        if e["event_type"] == "session_start":
            session_start[s] = e["timestamp"]

        if e["event_type"] == "session_end":
            session_end[s] = e["timestamp"]

    durations = []
    for s in session_start:
        if s in session_end:
            durations.append(session_end[s] - session_start[s])

    avg_session = sum(durations) // len(durations) if durations else 0

    most_active = sorted(user_activity.items(), key=lambda x: x[1], reverse=True)[:3]

    # login frequency buckets
    freq = {"2+": 0, "5+": 0, "10+": 0}
    for u, c in login_counts.items():
        if c >= 2: freq["2+"] += 1
        if c >= 5: freq["5+"] += 1
        if c >= 10: freq["10+"] += 1

    return {
        "total_users": len(users),
        "active_users": len(active_users),
        "most_active_users": most_active,
        "avg_session_duration": avg_session,
        "login_frequency": freq
    }


@app.route("/user-metrics")
def user_metrics():
    return jsonify(compute_user_metrics())


# =========================
# PAGE METRICS
# =========================
def compute_page_metrics():
    views = {}
    clicks = {}

    for e in user_events:
        page = e.get("metadata", {}).get("page", "unknown")

        if e["event_type"] == "page_view":
            views[page] = views.get(page, 0) + 1

        if e["event_type"] == "interaction_click":
            clicks[page] = clicks.get(page, 0) + 1

    return {"views": views, "clicks": clicks}


@app.route("/page-metrics")
def page_metrics():
    return jsonify(compute_page_metrics())


# =========================
# SUMMARY (STRICT)
# =========================
def compute_summary():
    m = compute_user_metrics()
    p = compute_page_metrics()

    return {
        "total_users": m["total_users"],
        "active_users": m["active_users"],
        "top_page": max(p["views"], key=p["views"].get) if p["views"] else None,
        "avg_session_time": m["avg_session_duration"]
    }


@app.route("/summary")
def summary():
    return jsonify(compute_summary())


# =========================
# SIGNALS
# =========================
def generate_all_signals(trace_id, latency, error_rate):
    deployment_status = get_deployment_status()["status"]

    raw = []
    raw += generate_app_signals(trace_id, latency, error_rate)
    raw += generate_cicd_signals(trace_id, deployment_status)
    raw += generate_infra_signals(trace_id, latency)
    raw += generate_executer_signals(trace_id)

    return [
        build_signal(st, svc, metric, val, trace_id)
        for (st, svc, metric, val) in raw
    ]


# =========================
# CORRELATION (STRICT TRACE)
# =========================
def correlate(trace_id):
    return {
        "trace_id": trace_id,
        "user_events": [e for e in user_events if e["trace_id"] == trace_id]
    }


# =========================
# STREAM (MULTI TRACE SAFE)
# =========================
last_inputs = {}

@app.route("/update-stream", methods=["POST"])
def update_stream():
    data = request.get_json(force=True)

    trace_id = data.get("trace_id")
    if not trace_id:
        return jsonify({"error": "trace_id required"}), 400

    last_inputs[trace_id] = {
        "latency": data.get("latency", 0),
        "error_rate": data.get("error_rate", 0)
    }

    return jsonify({"status": "updated"})


def stream_generator():
    while True:
        for trace_id, values in last_inputs.items():

            signals = generate_all_signals(
                trace_id,
                values["latency"],
                values["error_rate"]
            )

            output = {
                "trace_id": trace_id,
                "signals": signals,
                "correlation": correlate(trace_id)
            }

            yield f"data: {json.dumps(output)}\n\n"

        time.sleep(2)


@app.route("/signals/stream")
def stream():
    return Response(stream_generator(), mimetype="text/event-stream")


@app.route("/health")
def health():
    return jsonify({"status": "healthy"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5004)