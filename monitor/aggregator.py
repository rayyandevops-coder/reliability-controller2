import time
from collections import defaultdict


def aggregate_signals(*signal_lists):
    all_signals = []

    # merge all sources
    for signals in signal_lists:
        all_signals.extend(signals)

    # 🔥 remove duplicates
    unique = []
    seen = set()

    for s in all_signals:
        key = (s["signal_type"], s["metric"], s["timestamp"], s["trace_id"])
        if key not in seen:
            seen.add(key)
            unique.append(s)

    # 🔥 sort by timestamp
    unique.sort(key=lambda x: x["timestamp"])

    # 🔥 group by trace_id
    grouped = defaultdict(list)
    for s in unique:
        grouped[s["trace_id"]].append(s)

    return dict(grouped)