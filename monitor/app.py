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

    for f in required:
        if f not in data:
            return jsonify({"error": f"{f} missing"}), 400

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
    signals = []

    for e in user_events:
        if e.get("trace_id") != trace_id:
            continue

        etype = e.get("event_type")

        if etype == "user_login":
            signals.append({"signal_type": "login_detected"})

        elif etype == "interaction_click":
            signals.append({"signal_type": "user_interaction"})

        elif etype == "execution_done":
            signals.append({"signal_type": "execution_completed"})

    # 🔥 REAL INFRA SIGNAL
    cpu = psutil.cpu_percent(interval=0.1)
    if cpu > 70:
        signals.append({
            "signal_type": "cpu_high",
            "value": cpu
        })

    return signals


# =========================
# CAUSAL CHAIN (ORDERED)
# =========================
def causal_chain(trace_id):
    chain = []

    events = [e for e in user_events if e["trace_id"] == trace_id]

    # 🔥 ORDER BY TIME
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
    events = [e for e in user_events if e["trace_id"] == trace_id]

    events.sort(key=lambda x: x["timestamp"])

    return {
        "trace_id": trace_id,
        "user_events": events
    }


# =========================
# STREAM (REAL EVENT DRIVEN)
# =========================
def stream_generator():
    while True:
        try:
            output = None

            with lock:
                if event_queue:
                    evt = event_queue.popleft()
                    trace_id = evt.get("trace_id")

                    if not trace_id:
                        continue

                    output = {
                        "trace_id": trace_id,
                        "trace_hash": trace_hash(trace_id),
                        "signals": generate_signals(trace_id),
                        "correlation": correlate(trace_id),
                        "causal_chain": causal_chain(trace_id),
                        "timestamp": now()
                    }

            if output:
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