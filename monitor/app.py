from flask import Flask, request, jsonify, Response
import time, json, threading, hashlib
from collections import deque
from datetime import datetime

app = Flask(__name__)

MAX_EVENTS = 1000
user_events = deque(maxlen=MAX_EVENTS)
event_queue = deque(maxlen=MAX_EVENTS)
lock = threading.Lock()
last_sent = {}

def now():
    return datetime.utcnow().isoformat() + "Z"

def trace_hash(trace_id):
    return hashlib.sha256(trace_id.encode()).hexdigest()

@app.route("/track-event", methods=["POST"])
def track_event():
    data = request.get_json(force=True)

    required = ["user_id","event_type","timestamp","session_id","trace_id"]
    if not all(data.get(k) for k in required):
        return jsonify({"error":"invalid event"}),400

    with lock:
        user_events.append(data)
        event_queue.append({"trace_id": data["trace_id"]})

    return jsonify({"status":"ok"})


# =========================
# SIGNALS (FINAL STRUCTURED)
# =========================
def generate_signals(trace_id):
    for e in reversed(user_events):
        if e["trace_id"] == trace_id:

            et = e["event_type"]

            if et == "user_login":
                return [{"signal_type":"login_detected","service":e["metadata"].get("source")}]

            if et == "interaction_click":
                return [{"signal_type":"user_interaction","service":e["metadata"].get("source")}]

            if et == "decision_made":
                return [{"signal_type":"decision_made","service":"sarathi"}]

            if et == "execution_done":
                if e.get("status") == "success":
                    return [{"signal_type":"execution_completed","service":e.get("service")}]
                else:
                    return [{"signal_type":"execution_failed","service":e.get("service")}]

    return []


def causal_chain(trace_id):
    for e in reversed(user_events):
        if e["trace_id"] == trace_id:
            if e["event_type"] == "execution_done":
                return ["execution"]
            if e["event_type"] == "interaction_click":
                return ["user_click"]
            if e["event_type"] == "user_login":
                return ["user_login"]
    return []


def correlate(trace_id):
    return {
        "trace_id": trace_id,
        "user_events": sorted(
            [e for e in user_events if e["trace_id"] == trace_id],
            key=lambda x: x["timestamp"]
        )
    }


def stream_generator():
    while True:
        try:
            with lock:
                trace_id = event_queue.popleft()["trace_id"] if event_queue else None

            if not trace_id:
                yield ": keepalive\n\n"
                time.sleep(0.2)
                continue

            core = {
                "trace_id": trace_id,
                "trace_hash": trace_hash(trace_id),
                "signals": generate_signals(trace_id),
                "correlation": correlate(trace_id),
                "causal_chain": causal_chain(trace_id)
            }

            if last_sent.get(trace_id) != core:
                last_sent[trace_id] = core

                yield f"data: {json.dumps({**core,'timestamp':now()})}\n\n"
            else:
                yield ": keepalive\n\n"

        except Exception as e:
            print("[STREAM ERROR]", e)
            yield ": error\n\n"

        time.sleep(0.2)


@app.route("/signals/stream")
def stream():
    return Response(stream_generator(), mimetype="text/event-stream",
                    headers={"Cache-Control":"no-cache","X-Accel-Buffering":"no"})


@app.route("/health")
def health():
    return {"status":"ok"}

app.run(host="0.0.0.0", port=5004)