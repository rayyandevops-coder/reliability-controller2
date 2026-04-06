# ONLY CHANGE: removed execution trigger

def check_services():
    cpu    = round(psutil.cpu_percent(interval=1) / 100, 2)
    memory = round(psutil.virtual_memory().percent / 100, 2)

    for service_id, url in services.items():
        status     = "healthy"
        error_rate = 0.0
        action     = "noop"

        try:
            start   = time.time()
            res     = requests.get(url, timeout=2)
            latency = int((time.time() - start) * 1000)

            if res.status_code != 200:
                status = "critical"; error_rate = 1.0; action = "restart"
            elif latency > 500:
                status = "degraded"; action = "scale_up"

        except Exception:
            status = "critical"; error_rate = 1.0; action = "restart"

        log("DETECTION", service=service_id, status=status, action=action,
            cpu=cpu, memory=memory, error_rate=error_rate)

        if action == "noop":
            continue

        # ✅ BHIV CORRECT — SIGNAL ONLY
        log("SIGNAL_EMITTED",
            service=service_id,
            suggested_action=action,
            metrics={
                "cpu": cpu,
                "memory": memory,
                "error_rate": error_rate
            })