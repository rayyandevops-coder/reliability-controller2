def validate_deployment_request(service_id, action):
    # deterministic rules
    if not service_id:
        return "BLOCK"

    if action == "scale_up" and service_id == "critical-service":
        return "BLOCK"

    return "ALLOW"