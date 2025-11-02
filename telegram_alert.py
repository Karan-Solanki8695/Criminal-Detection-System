import os
import threading
import requests
import io

# Optional: load .env if python-dotenv is installed
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

BOT_TOKEN = os.getenv("TELEGRAM_TOKEN") or os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
API_BASE = f"https://api.telegram.org/bot{BOT_TOKEN}" if BOT_TOKEN else None

def _post_message(text):
    if not API_BASE or not CHAT_ID:
        return
    try:
        requests.post(f"{API_BASE}/sendMessage", data={"chat_id": CHAT_ID, "text": text}, timeout=6)
    except Exception:
        pass

def _post_photo(image_bytes, caption=""):
    if not API_BASE or not CHAT_ID:
        return
    try:
        requests.post(f"{API_BASE}/sendPhoto",
                      data={"chat_id": CHAT_ID, "caption": caption},
                      files={"photo": ("image.jpg", image_bytes, "image/jpeg")},
                      timeout=12)
    except Exception:
        pass

def send_alert(name, image=None, caption=None):
    """
    Non-blocking. image may be OpenCV BGR ndarray, bytes, or filepath string.
    """
    if not BOT_TOKEN or not CHAT_ID:
        return

    text = f"Recognized: {name}"
    if caption:
        text = f"{text}\n{caption}"

    def worker():
        img_bytes = None
        try:
            import cv2
            if hasattr(image, "shape"):
                ok, buf = cv2.imencode(".jpg", image)
                if ok:
                    img_bytes = io.BytesIO(buf.tobytes()).getvalue()
        except Exception:
            img_bytes = None

        if img_bytes is None and isinstance(image, str) and os.path.isfile(image):
            try:
                with open(image, "rb") as f:
                    img_bytes = f.read()
            except Exception:
                img_bytes = None

        if img_bytes is None and isinstance(image, (bytes, bytearray)):
            img_bytes = bytes(image)

        if img_bytes:
            _post_photo(img_bytes, caption=text)
            return
        _post_message(text)

    t = threading.Thread(target=worker, daemon=True)
    t.start()
