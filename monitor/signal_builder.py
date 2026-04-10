import time
from severity_engine import classify_signal
from validator import validate_signal


def build_signal(signal_type, service, metric, value, trace_id):
    signal = {
        "signal_type": signal_type,
        "severity": classify_signal(metric, value),
        "service": service,
        "metric": metric,
        "value": value,
        "timestamp": int(time.time()),
        "trace_id": trace_id if trace_id else None
    }

    # 🔥 STRICT VALIDATION (WILL FAIL IF INVALID)
    validate_signal(signal)

    print({
        "event": "SIGNAL_EMITTED",
        "signal": signal
    }, flush=True)

    return signal