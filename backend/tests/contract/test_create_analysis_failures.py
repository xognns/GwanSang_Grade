from backend.app.domain.errors import ErrorCode
from pathlib import Path


def _fixture_bytes(name: str) -> bytes:
    return (Path(__file__).resolve().parents[1] / "fixtures" / name).read_bytes()


def test_unsupported_format_is_rejected(client):
    payload = b"hello-world"
    files = {"file": ("avatar.gif", payload, "image/gif")}
    response = client.post("/api/v1/analyses", data={"name": "하루"}, files=files)
    assert response.status_code == 400
    assert response.json()["code"] == ErrorCode.unsupported_format.value


def test_missing_face_is_rejected(client):
    payload = _fixture_bytes("face_none.png")
    files = {"file": ("avatar.png", payload, "image/png")}
    response = client.post("/api/v1/analyses", data={"name": "하루"}, files=files)
    assert response.status_code == 422
    assert response.json()["code"] == ErrorCode.no_face.value


def test_missing_name_is_rejected(client):
    payload = _fixture_bytes("face_single.png")
    files = {"file": ("avatar.png", payload, "image/png")}
    response = client.post("/api/v1/analyses", data={"name": "   "}, files=files)
    assert response.status_code == 400
    assert response.json()["code"] == ErrorCode.missing_file.value
