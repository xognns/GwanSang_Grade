from pathlib import Path

from uuid import UUID


def _fixture_bytes(name: str) -> bytes:
    return (Path(__file__).resolve().parents[1] / "fixtures" / name).read_bytes()


def test_create_analysis_success(client):
    payload = _fixture_bytes("face_single.png")
    files = {"file": ("avatar.png", payload, "image/png")}
    response = client.post(
        "/api/v1/analyses",
        data={"name": "민수"},
        files=files,
    )
    assert response.status_code == 200
    body = response.json()
    UUID(body["requestId"])
    assert body["name"] == "민수"
    assert body["score"] >= 0.0
    assert body["score"] <= 4.5
    assert body["grade"] in {"A+", "A0", "B+", "B0", "C+", "C0", "D+", "D0", "F"}
    assert body["maxScore"] == 4.5
    assert isinstance(body["titles"], list)
    assert len(body["titles"]) >= 2
    assert len(body["titles"]) <= 3
    assert isinstance(body["stats"], dict)
    assert body["disclaimer"] != ""
    assert body["sharePayload"] is not None
    assert body["sharePayload"]["suggestedFileName"].endswith(".png")

    assert body["sharePayload"]["shareTitle"].endswith("성적표")
    assert body["sharePayload"]["shareText"] != ""


def test_create_analysis_multiple_faces_is_rejected(client):
    payload = _fixture_bytes("face_multi.png")
    files = {"file": ("avatar.png", payload, "image/png")}
    response = client.post("/api/v1/analyses", data={"name": "윤아"}, files=files)
    assert response.status_code == 422
    assert response.json()["code"] == "multiple_faces"
