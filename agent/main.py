import json
import time

from collector import collect_system_metrics


def main() -> None:
    print("SysPulse Agent started...")
    print("Collecting system metrics every 5 seconds.")
    print("Press Ctrl+C to stop.\n")

    while True:
        try:
            metrics = collect_system_metrics()
            print(json.dumps(metrics, indent=4))

            time.sleep(5)

        except KeyboardInterrupt:
            print("\nSysPulse Agent stopped.")
            break

        except Exception as error:
            print(f"Agent error: {error}")
            time.sleep(5)


if __name__ == "__main__":
    main()