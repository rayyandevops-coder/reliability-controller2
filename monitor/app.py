from flask import Flask, request, jsonify, Response
import time
import json
from collections import deque, defaultdict
import threading
import psutil
from datetime import datetime
import hashlib

app = Flask(__name__)

MAX_EVENTS = 2000

user_events = deque(maxlen=MAX_EVENTS)
event_queue = deque(maxlen=MAX_EVENTS)

# ✅ persistent signals per trace
trace_signals = defaultdict(set)

# ✅ prevent duplicate stream output
last_hash = {}

lock = threading.Lock()


# =========================
# TIME
# =========================
def now():
    return datetime.utcnow().isoformat() + "Z"


# =========================
# TRACE HASH
# =========================
def trace_hash(trace_id):
    return hashlib.sha256(trace_id.encode()).hexdigest()


# =========================
# TRACK EVENT
# =========================
@app.route("/track-event", methods=["POST"])
def track_event():
    data = request.get_json(force=True)

    required = ["user_id", "event_type", "timestamp", "session_id", "trace_id"]

    if not all(data.get(f) for f in required):
        return jsonify({"error": "invalid event"}), 400

    with lock:
        user_events.append(data)

        event_queue.append({
            "trace_id": data["trace_id"],
            "event_type": data["event_type"],
            "timestamp": data["timestamp"]
        })

    print(f"[TRACE EVENT] {data['trace_id']} -> {data['event_type']}", flush=True)

    return jsonify({"status": "ok"})


# =========================
# SIGNAL GENERATION (REAL)
# =========================
def generate_signals(trace_id):
    signals = trace_signals[trace_id]

    for e in user_events:
        if e.get("trace_id") != trace_id:
            continue

        et = e.get("event_type")
        service = e.get("metadata", {}).get("source", "unknown")

        if et == "user_login":
            signals.add(f"login_detected:{service}")

        elif et == "interaction_click":
            signals.add(f"user_interaction:{service}")

        elif et == "execution_done":
            svc = e.get("service", "unknown")
            signals.add(f"execution_completed:{svc}")

    # ✅ REAL INFRA SIGNAL
    cpu = psutil.cpu_percent(interval=0.1)

    if cpu > 70:
        signals.add(f"cpu_high:{int(cpu)}")

    return [{"signal_type": s} for s in sorted(signals)]


# =========================
# CAUSAL CHAIN
# =========================
def causal_chain(trace_id):
    events = [e for e in user_events if e["trace_id"] == trace_id]
    events.sort(key=lambda x: x["timestamp"])

    chain = []

    for e in events:
        et = e["event_type"]

        if et == "user_login":
            chain.append("user_login")

        elif et == "interaction_click":
            chain.append("user_click")

        elif et == "execution_done":
            chain.append("execution")

    return chain


# =========================
# CORRELATION
# =========================
def correlate(trace_id):
    events = [e for e in user_events if e["trace_id"] == trace_id]
    events.sort(key=lambda x: x["timestamp"])

    return {
        "trace_id": trace_id,
        "user_events": events
    }


# =========================
# STREAM (TRUE REAL-TIME)
# =========================
def generate_signals(trace_id):
    signals = []
    seen = set()

    # ✅ STRICT ORDERING BY REAL TIME
    events = sorted(
        [e for e in user_events if e.get("trace_id") == trace_id],
        key=lambda x: x["timestamp"]
    )

    for e in events:
        etype = e.get("event_type")
        source = e.get("metadata", {}).get("source", "unknown")

        # =========================
        # USER SIGNALS
        # =========================
        if etype == "user_login":
            signal = f"login_detected:{source}"

        elif etype == "interaction_click":
            signal = f"user_interaction:{source}"

        # =========================
        # EXECUTION SIGNAL
        # =========================
        elif etype == "execution_done":
            service = e.get("service", "unknown")
            signal = f"execution_completed:{service}"

        else:
            continue

        # ✅ REMOVE DUPLICATES BUT PRESERVE ORDER
        if signal not in seen:
            seen.add(signal)
            signals.append({"signal_type": signal})

    return signals

@app.route("/signals/stream")
def stream():
    return Response(
        stream_generator(),
        mimetype="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no"
        }
    )


# =========================
# HEALTH
# =========================
@app.route("/health")
def health():
    return {"status": "ok"}


# =========================
# MAIN
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5004)