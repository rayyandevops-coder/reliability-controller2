"""
sarathi/app.py — Policy Decision Point (PDP)
Receives proposals from SETU and returns: ALLOW / BLOCK / ESCALATE
Decision is based on Mitra decision_score:
  score > 0.6  → ALLOW   (high urgency + impact, act immediately)
  score > 0.35 → ESCALATE (medium confidence, needs review)
  else         → BLOCK    (low score, unsafe to act)
"""

from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/decision", methods=["POST"])
def decision():
    data  = request.get_json()
    score = data.get("payload", {}).get("decision_score", 0)
    action_type = data.get("action_type", "unknown")
    trace_id    = data.get("trace_id", "unknown")

    # ─── Policy rules ─────────────────────────────────────────────────────────
    if score > 0.6:
        status = "ALLOW"
        reason = f"Score {score} exceeds ALLOW threshold (0.6). Action approved."

    elif score > 0.35:
        status = "ESCALATE"
        reason = f"Score {score} in ESCALATE range (0.35–0.6). Manual review required."

    else:
        status = "BLOCK"
        reason = f"Score {score} below minimum threshold (0.35). Action blocked."

    print(f"[Sarathi] trace={trace_id} action={action_type} score={score} → {status}", flush=True)

    return jsonify({
        "status":   status,
        "reason":   reason,
        "trace_id": trace_id,
        "score":    score
    })


@app.route("/health")
def health():
    return jsonify({"status": "healthy"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)