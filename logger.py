import os
import datetime

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "detections.log")

def _ensure_dir():
    if not os.path.isdir(LOG_DIR):
        os.makedirs(LOG_DIR, exist_ok=True)

def log_detection(name):
    """Append a simple detection log entry."""
    _ensure_dir()
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"{ts} - {name}\n"
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line)
    except Exception:
        pass
