from pathlib import Path


def _fixture_bytes(name: str) -> bytes:
    return (Path(__file__).resolve().parents[1] / "fixtures" / name).read_bytes()


def test_success_response_includes_share_payload_fields(client):
    payload = _fixture_bytes("face_single.png")
    files = {"file": ("avatar.png", payload, "image/png")}
    response = client.post("/api/v1/analyses", data={"name": "하루"}, files=files)

    assert response.status_code == 200
    share_payload = response.json()["sharePayload"]

    assert set(share_payload.keys()) == {"suggestedFileName", "shareTitle", "shareText", "imageAlt"}
    assert share_payload["suggestedFileName"].endswith(".png")
    assert share_payload["shareTitle"] != ""
    assert share_payload["shareText"] != ""
    assert share_payload["imageAlt"] != ""
