"""
bucket.py — Append-Only Trace Logger (Truth Layer)
Every stage of every action is logged here with its trace_id.
Stages: proposal_created → proposal_scored → sarathi_decision →
        execution_result → outcome
"""

import json
import sys
from datetime import datetime


def log_event(trace_id, stage, data):
    """
    Write a single trace log entry to stdout.
    flush=True ensures it appears immediately in kubectl logs.
    """
    entry = {
        "trace_id": trace_id,
        "stage":    stage,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "data":     data
    }
    print(json.dumps(entry), flush=True)