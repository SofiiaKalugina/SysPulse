import requests


def send_metrics(backend_url: str, metrics: dict) -> bool:
    """
    Send collected metrics to the SysPulse backend.
    Returns True if backend accepted the data.
    """

    url = f"{backend_url}/api/metrics"

    try:
        response = requests.post(url, json=metrics, timeout=5)

        if response.status_code in (200, 201):
            return True

        print(f"Backend rejected metrics: {response.status_code} {response.text}")
        return False

    except requests.exceptions.ConnectionError:
        print("Backend is not available yet. Metrics were not sent.")
        return False

    except requests.exceptions.Timeout:
        print("Backend request timed out.")
        return False

    except requests.exceptions.RequestException as error:
        print(f"Request error: {error}")
        return False