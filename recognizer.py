import os
import numpy as np
import cv2
import face_recognition

def load_known_faces(folder_path, extensions=('.jpg', '.jpeg', '.png')): #replace folder with the path of folder of images of criminals(testing).
    """
    Load encodings: each subfolder = person name. Also accepts top-level images.
    Returns: (known_encodings (np.array or empty), known_names (list))
    """
    known_encodings = []
    known_names = []

    if not os.path.isdir(folder_path):
        print(f"[recognizer] folder not found: {folder_path}")
        return np.array([]), []

    entries = sorted(os.listdir(folder_path))

    # Subfolders -> person names
    for entry in entries:
        entry_path = os.path.join(folder_path, entry)
        if not os.path.isdir(entry_path):
            continue
        files = sorted([f for f in os.listdir(entry_path) if f.lower().endswith(extensions)])
        if not files:
            print(f"[recognizer] no images in subfolder: {entry_path}")
        for fname in files:
            path = os.path.join(entry_path, fname)
            try:
                img = face_recognition.load_image_file(path)
                encs = face_recognition.face_encodings(img)
                if not encs:
                    print(f"[recognizer] no face found in: {path}")
                    continue
                for enc in encs:
                    known_encodings.append(enc)
                    known_names.append(entry)
                    print(f"[recognizer] loaded: {entry} <- {fname}")
            except Exception as e:
                print(f"[recognizer] error reading {path}: {e}")

    # Top-level images (use filename as name)
    top_images = sorted([f for f in entries if f.lower().endswith(extensions) and os.path.isfile(os.path.join(folder_path, f))])
    for fname in top_images:
        path = os.path.join(folder_path, fname)
        person_name = os.path.splitext(fname)[0]
        try:
            img = face_recognition.load_image_file(path)
            encs = face_recognition.face_encodings(img)
            if not encs:
                print(f"[recognizer] no face found in top-level image: {path}")
                continue
            for enc in encs:
                known_encodings.append(enc)
                known_names.append(person_name)
                print(f"[recognizer] loaded top-level: {person_name} <- {fname}")
        except Exception as e:
            print(f"[recognizer] error reading {path}: {e}")

    if known_encodings:
        known_encodings = np.stack(known_encodings)
    else:
        known_encodings = np.array([])

    print(f"[recognizer] summary: loaded {len(known_encodings) if getattr(known_encodings,'size',0) else 0} encodings for {len(set(known_names))} people")
    return known_encodings, known_names

def recognize_faces(frame, known_encodings, known_names, scale=0.25, model='hog', tolerance=0.5):
    """
    Detect & recognize faces in BGR frame.
    Returns (face_locations, face_names) with locations in original frame coords.
    """
    if frame is None:
        return [], []

    # Resize for speed
    small = cv2.resize(frame, (0, 0), fx=scale, fy=scale)
    rgb_small = cv2.cvtColor(small, cv2.COLOR_BGR2RGB)

    locs_small = face_recognition.face_locations(rgb_small, model=model)
    encs_small = face_recognition.face_encodings(rgb_small, locs_small)

    face_locations = []
    face_names = []

    for enc, loc in zip(encs_small, locs_small):
        name = "Unknown"
        if getattr(known_encodings, "size", 0) != 0:
            distances = face_recognition.face_distance(known_encodings, enc)
            best_idx = np.argmin(distances)
            if distances[best_idx] <= tolerance:
                name = known_names[int(best_idx)]

        top, right, bottom, left = loc
        top = int(top / scale)
        right = int(right / scale)
        bottom = int(bottom / scale)
        left = int(left / scale)

        face_locations.append((top, right, bottom, left))
        face_names.append(name)

    return face_locations, face_names
