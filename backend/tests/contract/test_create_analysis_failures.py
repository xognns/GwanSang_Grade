from backend.app.domain.errors import ErrorCode


def test_unsupported_format_is_rejected(client):
    payload = b"hello-world"
    files = {"file": ("avatar.gif", payload, "image/gif")}
    response = client.post("/api/v1/analyses", data={"name": "하루"}, files=files)
    assert response.status_code == 400
    assert response.json()["code"] == ErrorCode.unsupported_format.value


def test_missing_face_is_rejected(client):
    payload = b"\x89PNG\r\n\x1a\nNO_FACE"
    files = {"file": ("avatar.png", payload, "image/png")}
    response = client.post("/api/v1/analyses", data={"name": "하루"}, files=files)
    assert response.status_code == 422
    assert response.json()["code"] == ErrorCode.no_face.value


def test_missing_name_is_rejected(client):
    payload = b"\x89PNG\r\n\x1a\nvalid-image-content"
    files = {"file": ("avatar.png", payload, "image/png")}
    response = client.post("/api/v1/analyses", data={"name": "   "}, files=files)
    assert response.status_code == 400
    assert response.json()["code"] == ErrorCode.missing_file.value
