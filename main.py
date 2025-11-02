import time
import threading
import concurrent.futures
import cv2
import os

from recognizer import load_known_faces, recognize_faces
from logger import log_detection
from snapshot import save_snapshot

try:
    from telegram_alert import send_alert
    TELEGRAM = True
except Exception:
    TELEGRAM = False

ALERT_COOLDOWN = 60  # seconds between alerts per person

class BackgroundCamera:
    """Background thread reading latest frame from camera."""
    def __init__(self, src=0, width=640, height=480):
        self.cap = cv2.VideoCapture(src)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.ret, self.frame = self.cap.read()
        self.lock = threading.Lock()
        self.running = False
        self.thread = None

    def start(self):
        if self.running:
            return
        self.running = True
        self.thread = threading.Thread(target=self._reader, daemon=True)
        self.thread.start()

    def _reader(self):
        while self.running:
            ret, frame = self.cap.read()
            with self.lock:
                self.ret = ret
                self.frame = frame

    def read(self):
        with self.lock:
            if self.frame is None:
                return False, None
            return self.ret, self.frame.copy()

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join(timeout=1.0)
        self.cap.release()

def main():
    CRIMINALS_DIR = r"C:\Users\karan\OneDrive\Pictures\criminals"
    known_encs, known_names = load_known_faces(CRIMINALS_DIR)
    print(f"[main] loaded {len(known_encs) if getattr(known_encs,'size',0) else 0} encodings for {len(set(known_names))} people")

    cam = BackgroundCamera(0)
    cam.start()

    executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
    future = None
    last_result = ([], [])
    scale = 0.5
    model = 'hog'
    tolerance = 0.6

    last_alert = {}

    try:
        while True:
            ret, frame = cam.read()
            if not ret or frame is None:
                time.sleep(0.01)
                continue

            if future is not None and future.done():
                try:
                    last_result = future.result()
                except Exception:
                    last_result = ([], [])
                future = None

            if future is None:
                # send original frame, recognizer will resize internally
                future = executor.submit(recognize_faces, frame.copy(), known_encs, known_names, scale, model, tolerance)

            face_locations, face_names = last_result

            for (top, right, bottom, left), name in zip(face_locations, face_names):
                top = max(0, top)
                left = max(0, left)
                bottom = min(frame.shape[0], bottom)
                right = min(frame.shape[1], right)

                if name != "Unknown":
                    color = (0, 255, 0)
                    try:
                        log_detection(name)
                    except Exception:
                        pass

                    face_crop = frame[top:bottom, left:right]
                    if face_crop is not None and face_crop.size != 0:
                        try:
                            save_snapshot(name, face_crop)
                        except Exception:
                            pass

                    if TELEGRAM:
                        now = time.time()
                        last = last_alert.get(name, 0)
                        if now - last >= ALERT_COOLDOWN:
                            last_alert[name] = now
                            try:
                                send_alert(name, image=face_crop, caption="Detected by demo")
                            except Exception:
                                pass
                else:
                    color = (0, 0, 255)

                cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
                cv2.putText(frame, name, (left, max(15, top - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2, cv2.LINE_AA)

            cv2.imshow("Criminal Detection (q to quit)", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    finally:
        cam.stop()
        executor.shutdown(wait=False)
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
