from backend.app.domain.errors import ErrorCode
from backend.app.services.validation_service import validate_upload
from pathlib import Path


def _fixture_bytes(name: str) -> bytes:
    return (Path(__file__).resolve().parents[1] / "fixtures" / name).read_bytes()


def test_rejects_missing_name():
    result = validate_upload(name="   ", file_name="avatar.png", file_bytes=b"abc", content_type="image/png")
    assert result.is_valid is False
    assert result.failure == ErrorCode.missing_file


def test_rejects_missing_file_data():
    result = validate_upload(name="민수", file_name="avatar.png", file_bytes=b"", content_type="image/png")
    assert result.is_valid is False
    assert result.failure == ErrorCode.missing_file


def test_rejects_face_not_detected():
    result = validate_upload(name="민수", file_name="avatar.png", file_bytes=_fixture_bytes("face_none.png"), content_type="image/png")
    assert result.is_valid is False
    assert result.failure == ErrorCode.no_face


def test_rejects_multiple_faces():
    result = validate_upload(name="민수", file_name="avatar.png", file_bytes=_fixture_bytes("face_multi.png"), content_type="image/png")
    assert result.is_valid is False
    assert result.failure == ErrorCode.multiple_faces


def test_accepts_single_face():
    result = validate_upload(name="민수", file_name="avatar.png", file_bytes=_fixture_bytes("face_single.png"), content_type="image/png")
    assert result.is_valid is True
    assert result.failure is None


def test_rejects_too_large_file():
    result = validate_upload(
        name="민수",
        file_name="avatar.png",
        file_bytes=b"a" * (10 * 1024 * 1024 + 1),
        content_type="image/png",
    )
    assert result.is_valid is False
    assert result.failure == ErrorCode.file_too_large


def test_rejects_unsupported_extension_when_no_content_type():
    result = validate_upload(name="민수", file_name="avatar.gif", file_bytes=b"abc", content_type=None)
    assert result.is_valid is False
    assert result.failure == ErrorCode.unsupported_format
