from pathlib import Path


def _fixture_bytes(name: str) -> bytes:
    return (Path(__file__).resolve().parents[1] / "fixtures" / name).read_bytes()


def test_end_to_end_success_flow_returns_contract_payload(client):
    payload = _fixture_bytes("face_single.png")
    files = {"file": ("avatar.png", payload, "image/png")}
    response = client.post("/api/v1/analyses", data={"name": "혜빈"}, files=files)

    assert response.status_code == 200

    body = response.json()
    assert body["name"] == "혜빈"
    assert body["score"] <= 4.5
    assert body["score"] >= 0.0
    assert body["grade"] in {"A+", "A0", "B+", "B0", "C+", "C0", "D+", "D0", "F"}
    assert body["disclaimer"].startswith("본 결과는")
    assert len(body["titles"]) in (2, 3)


def test_end_to_end_face_error_is_422_and_share_unavailable_not_default(client):
    payload = _fixture_bytes("face_none.png")
    files = {"file": ("avatar.png", payload, "image/png")}
    response = client.post("/api/v1/analyses", data={"name": "혜빈"}, files=files)

    assert response.status_code == 422
    assert response.json()["recoverable"] is True
