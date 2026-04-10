def generate_infra_signals(trace_id, latency):
    signals = []

    # 🔴 Critical crash
    if latency > 900:
        signals.append(("pod_crash", "kubernetes", "latency", latency))

    # 🟠 Restart loop
    elif latency > 750:
        signals.append(("restart_loop", "kubernetes", "latency", latency))

    # 🟡 Scaling event
    elif latency > 600:
        signals.append(("scaling_event", "kubernetes", "latency", latency))

    return signals