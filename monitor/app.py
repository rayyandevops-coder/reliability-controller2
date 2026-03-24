import requests
import time

# ✅ Correct Kubernetes Service URLs
services = {
    "detector": "http://detector-service:5001/health",
    "decision": "http://decision-service:5002/health",
    "executer": "http://executer-service:5003/health"
}

# ✅ Correct Executer API
EXECUTER_API = "http://executer-service:5003/restart"


def restart_service(service):
    try:
        print(f"[ACTION] Requesting restart for {service}")
        response = requests.post(
            EXECUTER_API,
            json={"service": service},
            timeout=3
        )
        print(f"[EXECUTER RESPONSE] {response.status_code} - {response.text}")
    except Exception as e:
        print(f"[ERROR] Executer not reachable: {e}")


def check_service(name, url):
    try:
        response = requests.get(url, timeout=3)

        if response.status_code == 200:
            print(f"[OK] {name} is healthy")
        else:
            print(f"[WARNING] {name} unhealthy (status {response.status_code})")
            restart_service(name)

    except Exception as e:
        print(f"[DOWN] {name} is not reachable: {e}")
        restart_service(name)


def monitor_loop():
    print("🚀 Monitor service started...")

    while True:
        print("\n--- Checking Services ---")

        for name, url in services.items():
            check_service(name, url)

        print("--- Waiting 5 seconds ---\n")
        time.sleep(5)


if __name__ == "__main__":
    try:
        monitor_loop()
    except KeyboardInterrupt:
        print("Monitor stopped manually")
    except Exception as e:
        print(f"[FATAL ERROR] {e}")