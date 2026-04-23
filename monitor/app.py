from flask import Flask, request, jsonify, Response
import time
import json
from collections import deque
import threading
from datetime import datetime
import hashlib

app = Flask(__name__)

MAX_EVENTS = 1000

user_events = deque(maxlen=MAX_EVENTS)
event_queue = deque(maxlen=MAX_EVENTS)

lock = threading.Lock()

# 🔥 STREAM STATE (prevents duplicate emissions)
last_sent = {}


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

    if not all(data.get(k) for k in required):
        return jsonify({"error": "invalid event"}), 400

    with lock:
        user_events.append(data)

        event_queue.append({
            "trace_id": data["trace_id"],
            "timestamp": data["timestamp"]
        })

    print(f"[TRACE EVENT] {data['trace_id']} -> {data['event_type']}", flush=True)

    return jsonify({"status": "ok"})


# =========================
# SIGNALS (STRICT ORDER)
# =========================
def generate_signals(trace_id):
    # 🔥 find latest event for this trace
    latest = None

    for e in reversed(user_events):
        if e.get("trace_id") == trace_id:
            latest = e
            break

    if not latest:
        return []

    etype = latest.get("event_type")
    source = latest.get("metadata", {}).get("source", "unknown")

    if etype == "user_login":
        return [{"signal_type": f"login_detected:{source}"}]

    elif etype == "interaction_click":
        return [{"signal_type": f"user_interaction:{source}"}]

    elif etype == "execution_done":
        service = latest.get("service", "unknown")
        return [{"signal_type": f"execution_completed:{service}"}]

    return []
# =========================
# CAUSAL CHAIN
# =========================
def causal_chain(trace_id):
    for e in reversed(user_events):
        if e.get("trace_id") == trace_id:
            et = e.get("event_type")

            if et == "user_login":
                return ["user_login"]

            elif et == "interaction_click":
                return ["user_click"]

            elif et == "execution_done":
                return ["execution"]

    return []
# =========================
# CORRELATION
# =========================
def correlate(trace_id):
    events = sorted(
        [e for e in user_events if e.get("trace_id") == trace_id],
        key=lambda x: x["timestamp"]
    )

    return {
        "trace_id": trace_id,
        "user_events": events
    }


# =========================
# STREAM GENERATOR (FINAL FIX)
# =========================
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
                time.sleep(0.2)
                continue

            # 🔥 BUILD CORE OUTPUT (NO TIMESTAMP)
            core_output = {
                "trace_id": trace_id,
                "trace_hash": trace_hash(trace_id),
                "signals": generate_signals(trace_id),
                "correlation": correlate(trace_id),
                "causal_chain": causal_chain(trace_id)
            }

            prev = last_sent.get(trace_id)

            # 🔥 COMPARE WITHOUT TIMESTAMP
            if prev != core_output:
                last_sent[trace_id] = core_output

                final_output = {
                    **core_output,
                    "timestamp": now()
                }

                print(f"[STREAM EMIT] {trace_id}", flush=True)

                yield f"data: {json.dumps(final_output)}\n\n"

            else:
                yield ": keepalive\n\n"

        except Exception as e:
            print(f"[STREAM ERROR] {str(e)}", flush=True)
            yield ": error\n\n"

        time.sleep(0.2)

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