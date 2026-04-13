def generate_cicd_signals(trace_id, deployment_status):
    if deployment_status == "failed":
        return [
            ("deployment_failure", "cicd", "status", "FAILURE")
        ]
    else:
        return [
            ("deployment_success", "cicd", "status", "SUCCESS")
        ]