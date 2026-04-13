def generate_executer_signals(trace_id):
    return [
        ("execution_update", "executer", "status", "RUNNING")
    ]