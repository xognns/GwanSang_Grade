from backend.app.domain.errors import ErrorCode
from pathlib import Path
from backend.app.services.analysis_service import AnalysisService
from backend.app.services.validation_service import MAX_SIZE_BYTES


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


def test_missing_file_is_rejected(client):
    response = client.post("/api/v1/analyses", data={"name": "하루"})
    assert response.status_code == 400
    assert response.json()["code"] == ErrorCode.missing_file.value


def test_analysis_failed_is_500(monkeypatch, client):
    class FailingAnalysisService(AnalysisService):
        def run(self, name: str, file_name: str, file_bytes: bytes, content_type: str | None):
            return None, ErrorCode.analysis_failed

    monkeypatch.setattr("backend.app.api.analyses.AnalysisService", FailingAnalysisService)

    payload = _fixture_bytes("face_single.png")
    files = {"file": ("avatar.png", payload, "image/png")}
    response = client.post("/api/v1/analyses", data={"name": "하루"}, files=files)
    assert response.status_code == 500
    assert response.json()["code"] == ErrorCode.analysis_failed.value


def test_oversize_file_is_rejected_before_analysis(monkeypatch, client):
    state = {"called": False}

    class FailingAnalysisService(AnalysisService):
        def run(self, name: str, file_name: str, file_bytes: bytes, content_type: str | None):
            state["called"] = True
            return None, ErrorCode.analysis_failed

    monkeypatch.setattr("backend.app.api.analyses.AnalysisService", FailingAnalysisService)

    payload = b"a" * (MAX_SIZE_BYTES + 1)
    files = {"file": ("avatar.png", payload, "image/png")}
    response = client.post("/api/v1/analyses", data={"name": "하루"}, files=files)

    assert response.status_code == 400
    assert response.json()["code"] == ErrorCode.file_too_large.value
    assert state["called"] is False
