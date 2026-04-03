from flask import Blueprint, jsonify
from datetime import datetime

deployment_bp = Blueprint("deployment", __name__)

STATUS = {
    "status": "success",
    "version": "latest",
    "timestamp": datetime.utcnow().isoformat() + "Z",
    "rollback": False
}

@deployment_bp.route("/deployment-status", methods=["GET"])
def deployment_status():
    return jsonify(STATUS)