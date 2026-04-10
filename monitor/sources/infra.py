def generate_infra_signals(trace_id, latency):
    signals = []

    if latency > 800:
        signals.append(("pod_crash", "kubernetes", "latency", latency))

    if latency > 700:
        signals.append(("restart_loop", "kubernetes", "latency", latency))

    return signals