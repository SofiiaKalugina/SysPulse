import os
from dotenv import load_dotenv

load_dotenv()

AGENT_VERSION = "0.1.0"

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
SEND_INTERVAL_SECONDS = int(os.getenv("SEND_INTERVAL_SECONDS", "5"))