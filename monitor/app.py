from flask import Flask, request, jsonify, Response
import time
import json
from collections import deque
import threading
import psutil   # 🔥 real system metric

app = Flask(__name__)

MAX_EVENTS = 1000

user_events = deque(maxlen=MAX_EVENTS)
event_queue = deque(maxlen=MAX_EVENTS)

lock = threading.Lock()


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
# SIGNALS (REAL)
# =========================
def generate_signals(trace_id):
    signals = []

    # USER SIGNALS
    for e in user_events:
        if e["trace_id"] != trace_id:
            continue

        if e["event_type"] == "user_login":
            signals.append({"signal_type": "login_detected"})

        if e["event_type"] == "interaction_click":
            signals.append({"signal_type": "user_interaction"})

        if e["event_type"] == "execution_done":
            signals.append({"signal_type": "execution_completed"})

    # 🔥 REAL INFRA SIGNAL (NOT FAKE)
    cpu = psutil.cpu_percent(interval=0.1)
    if cpu > 70:
        signals.append({"signal_type": "cpu_high", "value": cpu})

    return signals


# =========================
# CAUSAL CHAIN
# =========================
def causal_chain(trace_id):
    chain = []

    for e in user_events:
        if e["trace_id"] != trace_id:
            continue

        if e["event_type"] == "user_login":
            chain.append("login")

        if e["event_type"] == "interaction_click":
            chain.append("click")

        if e["event_type"] == "execution_done":
            chain.append("execution")

    return chain


# =========================
# CORRELATION
# =========================
def correlate(trace_id):
    return {
        "trace_id": trace_id,
        "user_events": [e for e in user_events if e["trace_id"] == trace_id]
    }


# =========================
# STREAM (REAL EVENT DRIVEN)
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

    return signals


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
                        "signals": generate_signals(trace_id),
                        "correlation": correlate(trace_id),
                        "timestamp": int(time.time())
                    }

            if output:
                print(f"[STREAM EMIT] {output['trace_id']}", flush=True)
                yield f"data: {json.dumps(output)}\n\n"
            else:
                yield ": keepalive\n\n"

        except Exception as e:
            print(f"[STREAM ERROR] {str(e)}", flush=True)
            yield ": error\n\n"

        time.sleep(0.1)

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

@app.route("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5004)