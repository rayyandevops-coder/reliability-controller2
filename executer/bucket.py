import json
from datetime import datetime

def log_event(trace_id, event, data):
    entry = {
        "trace_id": trace_id,
        "event": event,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "data": data
    }
    print(json.dumps(entry), flush=True)