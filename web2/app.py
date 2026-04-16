from flask import Flask, request, render_template_string, redirect
import requests
import time
import uuid

app = Flask(__name__)

MONITOR_URL = "http://monitor-service:5004/track-event"

current_user = {
    "user_id": None,
    "session_id": None,
    "trace_id": None
}


login_page = """
<h2>Login</h2>
<form method="POST" action="/login">
User ID: <input name="user_id"><br><br>
<button type="submit">Login</button>
</form>
"""

dashboard_page = """
<h2>Dashboard</h2>
<p>Welcome {{user_id}}</p>

<form method="POST" action="/click">
<button type="submit">Click</button>
</form>

<br>
<a href="/logout">Logout</a>
"""


@app.route("/")
def home():
    return login_page


@app.route("/login", methods=["POST"])
def login():
    user_id = request.form["user_id"].strip()

    if not user_id:
        return "Invalid user", 400

    session_id = f"s_{int(time.time())}"
    trace_id = str(uuid.uuid4())

    current_user["user_id"] = user_id
    current_user["session_id"] = session_id
    current_user["trace_id"] = trace_id

    meta = {"page": "dashboard", "source": "web1"}  # change for web2

    # SESSION START
    requests.post(MONITOR_URL, json={
        "user_id": user_id,
        "event_type": "session_start",
        "timestamp": int(time.time()),
        "session_id": session_id,
        "trace_id": trace_id,
        "metadata": meta
    })

    # LOGIN
    requests.post(MONITOR_URL, json={
        "user_id": user_id,
        "event_type": "user_login",
        "timestamp": int(time.time()),
        "session_id": session_id,
        "trace_id": trace_id,
        "metadata": meta
    })

    # PAGE VIEW
    requests.post(MONITOR_URL, json={
        "user_id": user_id,
        "event_type": "page_view",
        "timestamp": int(time.time()),
        "session_id": session_id,
        "trace_id": trace_id,
        "metadata": meta
    })

    return render_template_string(dashboard_page, user_id=user_id)


@app.route("/click", methods=["POST"])
def click():
    if current_user["user_id"]:
        requests.post(MONITOR_URL, json={
            "user_id": current_user["user_id"],
            "event_type": "interaction_click",
            "timestamp": int(time.time()),
            "session_id": current_user["session_id"],
            "trace_id": current_user["trace_id"],
            "metadata": {"page": "dashboard", "source": "web1"}
        })

    return "Clicked!"


@app.route("/logout")
def logout():
    if current_user["user_id"]:
        requests.post(MONITOR_URL, json={
            "user_id": current_user["user_id"],
            "event_type": "session_end",
            "timestamp": int(time.time()),
            "session_id": current_user["session_id"],
            "trace_id": current_user["trace_id"],
            "metadata": {}
        })

    return redirect("/")


@app.route("/health")
def health():
    return "ok"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)