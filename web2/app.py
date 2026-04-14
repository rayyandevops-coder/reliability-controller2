from flask import Flask, request, render_template_string
import requests
import time

app = Flask(__name__)

MONITOR_URL = "http://monitor-service:5004/track-event"

current_user = {
    "user_id": None,
    "session_id": None
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
  <button type="submit">Click Me</button>
</form>
"""


@app.route("/")
def home():
    return login_page


@app.route("/login", methods=["POST"])
def login():
    user_id = request.form["user_id"]
    session_id = f"s_{int(time.time())}"

    current_user["user_id"] = user_id
    current_user["session_id"] = session_id

    try:
        requests.post(MONITOR_URL, json={
            "user_id": user_id,
            "event_type": "user_login",
            "timestamp": int(time.time()),
            "session_id": session_id,
            "metadata": {}
        })
    except:
        pass  # prevent crash

    return render_template_string(dashboard_page, user_id=user_id)


@app.route("/click", methods=["POST"])
def click():
    try:
        requests.post(MONITOR_URL, json={
            "user_id": current_user["user_id"],
            "event_type": "interaction_click",
            "timestamp": int(time.time()),
            "session_id": current_user["session_id"],
            "metadata": {"button": "main"}
        })
    except:
        pass

    return "Clicked!"


@app.route("/health")
def health():
    return "ok"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)   # web2 → 5002