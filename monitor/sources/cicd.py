def generate_cicd_signals(trace_id, deployment_status):
    if deployment_status == "failed":
        return [("deployment_failure", "cicd", "status", 1)]
    else:
        return [("deployment_success", "cicd", "status", 0)]