from dataclasses import dataclass
from typing import Optional

import cv2
import numpy as np

from backend.app.domain.errors import ErrorCode


SUPPORTED_MEDIA_TYPES = {"image/jpeg", "image/png", "image/jpg"}
MAX_SIZE_BYTES = 10 * 1024 * 1024


@dataclass(frozen=True)
class ValidationFailure:
    is_valid: bool
    failure: Optional[ErrorCode]


def _normalize_mime(content_type: Optional[str], file_name: str) -> str:
    if content_type:
        return content_type.lower()
    lowered = file_name.lower()
    if lowered.endswith(".jpg") or lowered.endswith(".jpeg"):
        return "image/jpeg"
    if lowered.endswith(".png"):
        return "image/png"
    return lowered.rsplit(".", 1)[-1] if "." in lowered else ""


def _estimate_face_count(file_bytes: bytes) -> Optional[int]:
    image_data = np.frombuffer(file_bytes, dtype=np.uint8)
    decoded = cv2.imdecode(image_data, cv2.IMREAD_COLOR)
    if decoded is None:
        return None

    grayscale = cv2.cvtColor(decoded, cv2.COLOR_BGR2GRAY)
    cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = cascade.detectMultiScale(
        grayscale,
        scaleFactor=1.1,
        minNeighbors=4,
        minSize=(30, 30),
    )
    return len(faces)


def validate_upload(name: str, file_name: str, file_bytes: bytes, content_type: str | None) -> ValidationFailure:
    normalized_type = _normalize_mime(content_type, file_name)
    if not name.strip():
        return ValidationFailure(False, ErrorCode.missing_file)

    if not file_bytes:
        return ValidationFailure(False, ErrorCode.missing_file)

    if normalized_type not in SUPPORTED_MEDIA_TYPES:
        return ValidationFailure(False, ErrorCode.unsupported_format)

    if len(file_bytes) > MAX_SIZE_BYTES:
        return ValidationFailure(False, ErrorCode.file_too_large)

    face_count = _estimate_face_count(file_bytes)
    if face_count is None:
        return ValidationFailure(False, ErrorCode.unsupported_format)

    if face_count == 0:
        return ValidationFailure(False, ErrorCode.no_face)
    if face_count > 1:
        return ValidationFailure(False, ErrorCode.multiple_faces)

    return ValidationFailure(True, None)
