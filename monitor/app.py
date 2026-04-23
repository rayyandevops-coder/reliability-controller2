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

            output = {
                "trace_id": trace_id,
                "trace_hash": trace_hash(trace_id),
                "signals": generate_signals(trace_id),
                "correlation": correlate(trace_id),
                "causal_chain": causal_chain(trace_id),
                "timestamp": now()
            }

            # 🔥 CRITICAL FIX: ignore timestamp for duplicate check
            temp = dict(output)
            temp.pop("timestamp", None)

            current_hash = hashlib.md5(json.dumps(temp, sort_keys=True).encode()).hexdigest()

            if last_hash.get(trace_id) != current_hash:
                last_hash[trace_id] = current_hash

                print(f"[STREAM EMIT] {trace_id}", flush=True)

                yield f"data: {json.dumps(output)}\n\n"
            else:
                yield ": keepalive\n\n"

        except Exception as e:
            print(f"[STREAM ERROR] {str(e)}", flush=True)
            yield ": error\n\n"

        time.sleep(0.2)


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