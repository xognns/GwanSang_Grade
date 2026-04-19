def test_success_response_includes_share_payload_fields(client):
    payload = b"\x89PNG\r\n\x1a\nvalid-image-content"
    files = {"file": ("avatar.png", payload, "image/png")}
    response = client.post("/api/v1/analyses", data={"name": "하루"}, files=files)

    assert response.status_code == 200
    share_payload = response.json()["sharePayload"]

    assert set(share_payload.keys()) == {"suggestedFileName", "shareTitle", "shareText", "imageAlt"}
    assert share_payload["suggestedFileName"].endswith(".png")
    assert share_payload["shareTitle"] != ""
    assert share_payload["shareText"] != ""
    assert share_payload["imageAlt"] != ""
