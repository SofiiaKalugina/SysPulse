import json
import time

from collector import collect_system_metrics
from config import BACKEND_URL, SEND_INTERVAL_SECONDS
from sender import send_metrics


def main() -> None:
    print("SysPulse Agent started...")
    print(f"Backend URL: {BACKEND_URL}")
    print(f"Collecting system metrics every {SEND_INTERVAL_SECONDS} seconds.")
    print("Press Ctrl+C to stop.\n")

    while True:
        try:
            metrics = collect_system_metrics()

            print(json.dumps(metrics, indent=4))

            sent = send_metrics(BACKEND_URL, metrics)

            if sent:
                print("Metrics sent successfully.\n")
            else:
                print("Metrics stored locally only for now.\n")

            time.sleep(SEND_INTERVAL_SECONDS)

        except KeyboardInterrupt:
            print("\nSysPulse Agent stopped.")
            break

        except Exception as error:
            print(f"Agent error: {error}")
            time.sleep(SEND_INTERVAL_SECONDS)


if __name__ == "__main__":
    main()