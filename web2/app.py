from flask import Flask, request, render_template_string, redirect
import requests
import time

app = Flask(__name__)

MONITOR_URL = "http://monitor-service:5004/track-event"

current_user = {"user_id": None, "session_id": None}


def get_device():
    ua = request.headers.get("User-Agent", "").lower()
    if "mobile" in ua:
        return "mobile"
    elif "windows" in ua or "linux" in ua:
        return "desktop"
    return "unknown"


def get_region():
    ip = request.remote_addr
    if ip.startswith(("192.", "172.", "127.")):
        return "local"
    return "external"


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

    current_user["user_id"] = user_id
    current_user["session_id"] = session_id

    meta = {
        "page": "dashboard",
        "device": get_device(),
        "region": get_region(),
        "source": "web1"  # change to web2 in web2
    }

    # 🔥 SESSION START
    requests.post(MONITOR_URL, json={
        "user_id": user_id,
        "event_type": "session_start",
        "timestamp": int(time.time()),
        "session_id": session_id,
        "metadata": meta
    })

    # LOGIN
    requests.post(MONITOR_URL, json={
        "user_id": user_id,
        "event_type": "user_login",
        "timestamp": int(time.time()),
        "session_id": session_id,
        "metadata": meta
    })

    # PAGE VIEW
    requests.post(MONITOR_URL, json={
        "user_id": user_id,
        "event_type": "page_view",
        "timestamp": int(time.time()),
        "session_id": session_id,
        "metadata": meta
    })

    return render_template_string(dashboard_page, user_id=user_id)


@app.route("/click", methods=["POST"])
def click():
    if current_user["user_id"]:
        meta = {
            "page": "dashboard",
            "device": get_device(),
            "region": get_region(),
            "source": "web1",
            "button": "main"
        }

        requests.post(MONITOR_URL, json={
            "user_id": current_user["user_id"],
            "event_type": "interaction_click",
            "timestamp": int(time.time()),
            "session_id": current_user["session_id"],
            "metadata": meta
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
            "metadata": {}
        })

    current_user["user_id"] = None
    current_user["session_id"] = None

    return redirect("/")


@app.route("/health")
def health():
    return "ok"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)  # web2 → 5002