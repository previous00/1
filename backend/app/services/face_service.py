import os
import pickle
import time
import numpy as np
import cv2
from flask import current_app
from ..models.face import FaceEncoding
from ..extensions import db

_encoding_cache = None
_cache_timestamp = 0


def get_face_detector():
    return cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')


def detect_face(image_array):
    gray = cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY)
    detector = get_face_detector()
    faces = detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(80, 80))
    return faces


def extract_face_encoding(image_array, face_rect):
    x, y, w, h = face_rect
    face_roi = image_array[y:y+h, x:x+w]
    face_resized = cv2.resize(face_roi, (160, 160))
    face_normalized = face_resized.astype(np.float32) / 255.0
    encoding = face_normalized.flatten()
    norm = np.linalg.norm(encoding)
    if norm > 0:
        encoding = encoding / norm
    return encoding


def compute_distance(encoding1, encoding2):
    return np.linalg.norm(encoding1 - encoding2)


def get_all_encodings():
    global _encoding_cache, _cache_timestamp

    latest = db.session.query(db.func.count(FaceEncoding.id)).scalar()
    if _encoding_cache is None or latest != _cache_timestamp:
        records = FaceEncoding.query.filter_by(is_primary=True).all()
        _encoding_cache = {
            'encodings': [pickle.loads(r.encoding) for r in records],
            'user_ids': [r.user_id for r in records],
        }
        _cache_timestamp = latest
    return _encoding_cache


def invalidate_cache():
    global _encoding_cache, _cache_timestamp
    _encoding_cache = None
    _cache_timestamp = 0


def enroll_face(user_id, image_path):
    image = cv2.imread(image_path)
    if image is None:
        return None, '无法读取图片文件'

    faces = detect_face(image)
    if len(faces) == 0:
        return None, '未检测到人脸，请确保光线充足且正对摄像头'
    if len(faces) > 1:
        return None, '检测到多张人脸，请确保画面中只有一个人'

    encoding = extract_face_encoding(image, faces[0])
    encoding_blob = pickle.dumps(encoding)

    existing = FaceEncoding.query.filter_by(user_id=user_id, is_primary=True).first()
    if existing:
        existing.is_primary = False

    face_record = FaceEncoding(
        user_id=user_id,
        encoding=encoding_blob,
        image_path=image_path,
        is_primary=True,
    )
    db.session.add(face_record)
    db.session.commit()
    invalidate_cache()

    return face_record, None


def verify_face(image_path, tolerance=None):
    if tolerance is None:
        tolerance = current_app.config.get('FACE_TOLERANCE', 0.6)

    image = cv2.imread(image_path)
    if image is None:
        return None, 0, '无法读取图片文件'

    faces = detect_face(image)
    if len(faces) == 0:
        return None, 0, '未检测到人脸'

    encoding = extract_face_encoding(image, faces[0])
    cache = get_all_encodings()

    if not cache['encodings']:
        return None, 0, '系统中尚无已注册人脸'

    min_distance = float('inf')
    matched_user_id = None

    for i, stored_encoding in enumerate(cache['encodings']):
        distance = compute_distance(encoding, stored_encoding)
        if distance < min_distance:
            min_distance = distance
            matched_user_id = cache['user_ids'][i]

    confidence = max(0, 1 - min_distance)

    if min_distance < tolerance:
        return matched_user_id, confidence, None
    else:
        return None, confidence, '未匹配到已注册人员'
