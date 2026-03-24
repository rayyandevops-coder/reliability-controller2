from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "Executer Service Running"

@app.route("/health")
def health():
    return {"status": "healthy"}, 200

@app.route("/restart", methods=["POST"])
def restart():
    data = request.json
    service = data.get("service")

    if service:
        print(f"Restarting {service}...")
        os.system(f"docker restart {service}")
        return jsonify({"message": f"{service} restarted"}), 200

    return jsonify({"error": "No service provided"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003)