from flask import Flask, request, jsonify, Response
import time
from collections import defaultdict

from signal_builder import build_signal
from sources.infra import generate_infra_signals
from sources.cicd import generate_cicd_signals
from sources.app_metrics import generate_app_signals
from sources.executer_logs import generate_executer_signals
from deployment_status import get_deployment_status
from aggregator import aggregate_signals

app = Flask(__name__)

# =========================
# STORAGE
# =========================
user_events = []

# =========================
# PHASE 1 — EVENT TRACKING
# =========================
@app.route("/track-event", methods=["POST"])
def track_event():
    try:
        data = request.get_json()

        required = ["user_id", "event_type", "timestamp", "session_id"]

        for field in required:
            if field not in data:
                return jsonify({"error": f"{field} missing"}), 400

        user_id = data.get("user_id")

        if not user_id or str(user_id).strip() == "":
            return jsonify({"error": "invalid user_id"}), 400

        # 🔥 TRACE CONTINUITY
        data["trace_id"] = data.get("session_id")

        user_events.append(data)

        print("[EVENT]", data, flush=True)

        return jsonify({"status": "event recorded"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# =========================
# PHASE 2 — USER METRICS
# =========================
def compute_user_metrics():
    users = set()
    active_users = set()
    user_sessions = defaultdict(set)
    login_count = defaultdict(int)
    user_activity = defaultdict(int)

    now = int(time.time())

    for event in user_events:
        u = event["user_id"]
        users.add(u)

        if now - event["timestamp"] < 600:
            active_users.add(u)

        user_sessions[u].add(event["session_id"])
        user_activity[u] += 1

        if event["event_type"] == "user_login":
            login_count[u] += 1

    returning_users = [u for u in user_sessions if len(user_sessions[u]) > 1]

    freq = {"2+":0,"5+":0,"10+":0,"15+":0,"100+":0}
    for u,c in login_count.items():
        if c>=2: freq["2+"]+=1
        if c>=5: freq["5+"]+=1
        if c>=10: freq["10+"]+=1
        if c>=15: freq["15+"]+=1
        if c>=100: freq["100+"]+=1

    most_active = sorted(user_activity.items(), key=lambda x:x[1], reverse=True)[:3]

    return {
        "total_users": len(users),
        "active_users": len(active_users),
        "returning_users": len(returning_users),
        "login_frequency": freq,
        "most_active_users": most_active
    }


@app.route("/user-metrics")
def user_metrics():
    return jsonify(compute_user_metrics())


# =========================
# PHASE 3 — PAGE METRICS
# =========================
def compute_page_metrics():
    page_views = {}
    page_clicks = {}
    session_times = {}

    for e in user_events:
        page = e.get("metadata", {}).get("page", "unknown")
        ts = e["timestamp"]
        s = e["session_id"]

        if e["event_type"] == "page_view":
            page_views[page] = page_views.get(page,0)+1

        if e["event_type"] == "interaction_click":
            page_clicks[page] = page_clicks.get(page,0)+1

        if s not in session_times:
            session_times[s] = [ts,ts]
        else:
            session_times[s][0] = min(session_times[s][0], ts)
            session_times[s][1] = max(session_times[s][1], ts)

    avg_time = 0
    if session_times:
        total = sum(end-start for start,end in session_times.values())
        avg_time = total//len(session_times)

    clicks = sum(page_clicks.values())

    if clicks>10: density="high"
    elif clicks>5: density="medium"
    else: density="low"

    return {
        "views": page_views,
        "clicks": page_clicks,
        "avg_time_spent": avg_time,
        "interaction_density": density
    }


@app.route("/page-metrics")
def page_metrics():
    return jsonify(compute_page_metrics())


# =========================
# PHASE 4 — CONTEXT
# =========================
def compute_context():
    region_count = {}
    device_count = {}
    source_count = {}

    for e in user_events:
        m = e.get("metadata", {})
        r = m.get("region","unknown")
        d = m.get("device","unknown")
        s = m.get("source","web")

        region_count[r] = region_count.get(r,0)+1
        device_count[d] = device_count.get(d,0)+1
        source_count[s] = source_count.get(s,0)+1

    return {
        "regions": region_count,
        "devices": device_count,
        "sources": source_count
    }


@app.route("/user-context")
def user_context():
    return jsonify(compute_context())


# =========================
# PHASE 5 — AGGREGATION
# =========================
def compute_aggregate():
    return {
        "user_metrics": compute_user_metrics(),
        "page_metrics": compute_page_metrics(),
        "context": compute_context()
    }


@app.route("/aggregate")
def aggregate():
    return jsonify(compute_aggregate())


# =========================
# PHASE 6 — SUMMARY
# =========================
def compute_summary():
    m = compute_user_metrics()
    p = compute_page_metrics()

    growth = "increasing" if m["total_users"]>1 else "stable"
    engagement = "high" if m["active_users"]>1 else "low"
    most_page = max(p["views"], key=p["views"].get) if p["views"] else "unknown"

    return {
        "user_growth": growth,
        "engagement_level": engagement,
        "most_active_area": most_page,
        "drop_off_area": "unknown"
    }


@app.route("/summary")
def summary():
    return jsonify({"summary": compute_summary()})


# =========================
# SIGNAL SYSTEM (FIXED)
# =========================
def generate_all_signals(trace_id, latency, error_rate):
    deployment_status = get_deployment_status()["status"]

    raw = []
    raw += generate_app_signals(trace_id, latency, error_rate)
    raw += generate_cicd_signals(trace_id, deployment_status)
    raw += generate_infra_signals(trace_id, latency)
    raw += generate_executer_signals(trace_id)

    return [build_signal(st,svc,metric,val,trace_id) for (st,svc,metric,val) in raw]


# =========================
# CORRELATION (NEW)
# =========================
def correlate_all(trace_id):
    return {
        "trace_id": trace_id,
        "aggregate": compute_aggregate(),
        "summary": compute_summary()
    }


# =========================
# STREAM (FINAL)
# =========================
last_input={"trace_id":"stream-1","latency":0,"error_rate":0}

@app.route("/update-stream", methods=["POST"])
def update_stream():
    data=request.get_json()
    last_input.update(data)
    return jsonify({"status":"updated"})


def stream_generator():
    while True:
        trace_id = last_input["trace_id"]

        signals = generate_all_signals(
            trace_id,
            last_input["latency"],
            last_input["error_rate"]
        )

        correlated = correlate_all(trace_id)

        output = {
            "trace_id": trace_id,
            "signals": signals,
            "correlation": correlated
        }

        yield f"data: {output}\n\n"
        time.sleep(2)


@app.route("/signals/stream")
def stream():
    return Response(stream_generator(), mimetype="text/event-stream")


@app.route("/health")
def health():
    return jsonify({"status":"healthy"})


if __name__=="__main__":
    app.run(host="0.0.0.0", port=5004)