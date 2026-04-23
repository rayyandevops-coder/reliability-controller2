from flask import Flask, request, render_template_string
import requests
import time

app = Flask(__name__)

MONITOR_URL = "http://monitor-service:5004/track-event"

# =========================
# UI TEMPLATES
# =========================
login_page = """
<h2>Login</h2>
<form method="POST" action="/login">
  User ID: <input name="user_id"><br><br>
  <button type="submit">Login</button>
</form>
"""

dashboard_page = """
<h2>Dashboard - Web1</h2>
<p>Welcome {{user_id}}</p>

<form method="POST" action="/click">
  <input type="hidden" name="user_id" value="{{user_id}}">
  <input type="hidden" name="session_id" value="{{session_id}}">
  <button type="submit">Click</button>
</form>

<form method="POST" action="/logout">
  <input type="hidden" name="user_id" value="{{user_id}}">
  <input type="hidden" name="session_id" value="{{session_id}}">
  <button type="submit">Logout</button>
</form>
"""


# =========================
# HOME
# =========================
@app.route("/")
def home():
    return login_page


# =========================
# LOGIN (TRACE STRICT)
# =========================
@app.route("/login", methods=["POST"])
def login():
    user_id = request.form.get("user_id")

    # 🔥 STRICT TRACE FROM HEADER ONLY
    trace_id = request.headers.get("X-TRACE-ID")
    if not trace_id:
        return "trace_id required in header", 400

    print(f"[WEB1 TRACE] {trace_id}", flush=True)

    session_id = f"s_{int(time.time())}"

    events = ["session_start", "user_login", "page_view"]

    for e in events:
        requests.post(MONITOR_URL, json={
            "user_id": user_id,
            "event_type": e,
            "timestamp": int(time.time()),
            "session_id": session_id,
            "trace_id": trace_id,
            "metadata": {
                "page": "dashboard",
                "source": "web1"
            }
        })

    return render_template_string(
        dashboard_page,
        user_id=user_id,
        session_id=session_id
    )


# =========================
# CLICK
# =========================
@app.route("/click", methods=["POST"])
def click():
    trace_id = request.headers.get("X-TRACE-ID")
    if not trace_id:
        return "trace_id required", 400

    requests.post(MONITOR_URL, json={
        "user_id": request.form.get("user_id"),
        "event_type": "interaction_click",
        "timestamp": int(time.time()),
        "session_id": request.form.get("session_id"),
        "trace_id": trace_id,
        "metadata": {
            "page": "dashboard",
            "source": "web1"
        }
    })

    print(f"[WEB1 CLICK] trace_id={trace_id}", flush=True)

    return "clicked"


# =========================
# LOGOUT
# =========================
@app.route("/logout", methods=["POST"])
def logout():
    trace_id = request.headers.get("X-TRACE-ID")
    if not trace_id:
        return "trace_id required", 400

    requests.post(MONITOR_URL, json={
        "user_id": request.form.get("user_id"),
        "event_type": "session_end",
        "timestamp": int(time.time()),
        "session_id": request.form.get("session_id"),
        "trace_id": trace_id,
        "metadata": {
            "source": "web1"
        }
    })

    return "logout"


@app.route("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)