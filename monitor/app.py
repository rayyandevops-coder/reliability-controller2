from flask import Flask, request, jsonify, Response
import time
import json
from collections import deque
import threading
import psutil
from datetime import datetime
import hashlib

app = Flask(__name__)

MAX_EVENTS = 1000

user_events = deque(maxlen=MAX_EVENTS)
event_queue = deque(maxlen=MAX_EVENTS)

lock = threading.Lock()


# =========================
# TIME (ISO STANDARD)
# =========================
def now():
    return datetime.utcnow().isoformat() + "Z"


# =========================
# TRACE HASH (INTEGRITY)
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

    if not all([
        data.get("user_id"),
        data.get("event_type"),
        data.get("timestamp"),
        data.get("session_id"),
        data.get("trace_id")
    ]):
        return jsonify({"error": "invalid event"}), 400

    with lock:
        user_events.append(data)

        event_queue.append({
            "trace_id": data["trace_id"],
            "type": data["event_type"],
            "timestamp": data["timestamp"]
        })

    print(f"[TRACE EVENT] {data['trace_id']} -> {data['event_type']}", flush=True)

    return jsonify({"status": "ok"})


# =========================
# SIGNALS (REAL ONLY)
# =========================
def generate_signals(trace_id):
    seen = set()
    signals = []

    for e in user_events:
        if e.get("trace_id") != trace_id:
            continue

        etype = e.get("event_type")

        if etype == "user_login":
            s = "login_detected"

        elif etype == "interaction_click":
            s = "user_interaction"

        elif etype == "execution_done":
            s = "execution_completed"
        else:
            continue

        if s not in seen:
            seen.add(s)
            signals.append({"signal_type": s})

    return signals


# =========================
# CAUSAL CHAIN (ORDERED)
# =========================
def causal_chain(trace_id):
    chain = []

    events = [
        e for e in user_events
        if e["trace_id"] == trace_id
        and e.get("user_id")  # 🔥 ignore broken events
    ]

    events.sort(key=lambda x: x["timestamp"])

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
# CORRELATION (ORDERED)
# =========================
def correlate(trace_id):
    events = [
        e for e in user_events
        if e["trace_id"] == trace_id
        and e.get("user_id")
    ]

    events.sort(key=lambda x: x["timestamp"])

    return {
        "trace_id": trace_id,
        "user_events": events
    }

# =========================
# STREAM (REAL EVENT DRIVEN)
# =========================
last_sent = {}

def stream_generator():
    while True:
        try:
            with lock:
                if event_queue:
                    evt = event_queue.popleft()
                    trace_id = evt.get("trace_id")
                else:
                    trace_id = None

            if not trace_id:
                yield ": keepalive\n\n"
                time.sleep(0.1)
                continue

            output = {
                "trace_id": trace_id,
                "trace_hash": trace_hash(trace_id),
                "signals": generate_signals(trace_id),
                "correlation": correlate(trace_id),
                "causal_chain": causal_chain(trace_id),
                "timestamp": now()
            }

            # 🔥 emit only on change
            prev = last_sent.get(trace_id)
            if prev != output:
                last_sent[trace_id] = output
                print(f"[STREAM EMIT] {trace_id}", flush=True)
                yield f"data: {json.dumps(output)}\n\n"
            else:
                yield ": keepalive\n\n"

        except Exception as e:
            print(f"[STREAM ERROR] {str(e)}", flush=True)
            yield ": error\n\n"

        time.sleep(0.1)
# =========================
# STREAM ROUTE
# =========================
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