from backend.app.domain.errors import ErrorCode
from backend.app.services.validation_service import validate_upload


def test_rejects_missing_name():
    result = validate_upload(name="   ", file_name="avatar.png", file_bytes=b"abc", content_type="image/png")
    assert result.is_valid is False
    assert result.failure == ErrorCode.missing_file


def test_rejects_missing_file_data():
    result = validate_upload(name="민수", file_name="avatar.png", file_bytes=b"", content_type="image/png")
    assert result.is_valid is False
    assert result.failure == ErrorCode.missing_file


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
