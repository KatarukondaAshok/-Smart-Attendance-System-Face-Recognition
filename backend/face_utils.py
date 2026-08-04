import os
import cv2
import numpy as np

EMBEDDING_DIR = "data/embeddings"
os.makedirs(EMBEDDING_DIR, exist_ok=True)

TARGET_SIZE = (160, 160)

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)


def preprocess_face(gray_face):
    face = cv2.resize(gray_face, TARGET_SIZE)
    face = cv2.equalizeHist(face)
    face = cv2.GaussianBlur(face, (3, 3), 0)
    return face


def detect_largest_face(image_bgr):
    if image_bgr is None:
        raise ValueError("Unable to read image")

    gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(60, 60)
    )

    if len(faces) == 0:
        raise ValueError("No face detected")

    x, y, w, h = max(faces, key=lambda f: f[2] * f[3])

    pad = 15
    x1 = max(x - pad, 0)
    y1 = max(y - pad, 0)
    x2 = min(x + w + pad, image_bgr.shape[1])
    y2 = min(y + h + pad, image_bgr.shape[0])

    return x1, y1, x2, y2


def save_cropped_face_image(input_path: str, output_path: str):
    image = cv2.imread(input_path)
    x1, y1, x2, y2 = detect_largest_face(image)
    face_crop = image[y1:y2, x1:x2]
    cv2.imwrite(output_path, face_crop)
    return output_path


def generate_face_embedding_from_image(image_path: str, student_id: int):
    image = cv2.imread(image_path)
    x1, y1, x2, y2 = detect_largest_face(image)

    face_crop = image[y1:y2, x1:x2]
    gray_face = cv2.cvtColor(face_crop, cv2.COLOR_BGR2GRAY)
    processed_face = preprocess_face(gray_face)

    embedding_path = os.path.join(EMBEDDING_DIR, f"student_{student_id}.npy")
    np.save(embedding_path, processed_face)
    return embedding_path


def _normalize_embedding_shape(embedding: np.ndarray) -> np.ndarray:
    if embedding is None:
        raise ValueError("Invalid embedding")

    if len(embedding.shape) != 2:
        raise ValueError("Embedding must be a 2D grayscale array")

    if embedding.shape != TARGET_SIZE:
        embedding = cv2.resize(embedding, TARGET_SIZE)

    embedding = embedding.astype("uint8")
    embedding = cv2.equalizeHist(embedding)
    embedding = cv2.GaussianBlur(embedding, (3, 3), 0)
    return embedding


def load_known_embeddings(students):
    known_embeddings = []
    known_students = []

    for student in students:
        if student.embedding_path and os.path.exists(student.embedding_path):
            try:
                embedding = np.load(student.embedding_path)
                embedding = _normalize_embedding_shape(embedding)
                known_embeddings.append(embedding)
                known_students.append(student)
            except Exception:
                continue

    return known_embeddings, known_students


def recognize_face(test_image_path, known_embeddings, known_students):
    image = cv2.imread(test_image_path)
    x1, y1, x2, y2 = detect_largest_face(image)

    face_crop = image[y1:y2, x1:x2]
    gray_face = cv2.cvtColor(face_crop, cv2.COLOR_BGR2GRAY)
    test_face = preprocess_face(gray_face)

    best_score = None
    best_student = None

    for i, embedding in enumerate(known_embeddings):
        try:
            embedding = _normalize_embedding_shape(embedding)
            diff = float(np.mean(np.abs(test_face.astype("float32") - embedding.astype("float32"))))
        except Exception:
            continue

        if best_score is None or diff < best_score:
            best_score = diff
            best_student = known_students[i]

    print("Best match score:", best_score)

    if best_score is not None and best_score < 72:
        confidence = float(round(max(0, 100 - best_score), 2))
        return best_student, confidence

    return None, None