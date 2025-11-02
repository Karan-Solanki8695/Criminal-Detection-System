import os
import datetime
import cv2

SNAP_DIR = "snapshots"
os.makedirs(SNAP_DIR, exist_ok=True)

def save_snapshot(name, image):
    """Save image (BGR numpy) to snapshots/<name>_<timestamp>.jpg"""
    if image is None:
        return
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    safe = "".join(c if c.isalnum() or c in "-_." else "_" for c in name)[:64]
    filename = os.path.join(SNAP_DIR, f"{safe}_{ts}.jpg")
    try:
        cv2.imwrite(filename, image)
    except Exception:
        pass
