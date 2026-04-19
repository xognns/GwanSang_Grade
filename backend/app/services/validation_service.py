from dataclasses import dataclass
from typing import Optional

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


def _estimate_face_count(file_bytes: bytes) -> int:
    if b"NO_FACE" in file_bytes:
        return 0
    if b"MULTI_FACE" in file_bytes:
        return 2
    return 1


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
    if face_count == 0:
        return ValidationFailure(False, ErrorCode.no_face)
    if face_count > 1:
        return ValidationFailure(False, ErrorCode.multiple_faces)

    return ValidationFailure(True, None)
