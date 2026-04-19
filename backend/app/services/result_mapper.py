from dataclasses import asdict

from backend.app.domain.models import AnalysisResult


def to_api_response(result: AnalysisResult) -> dict:
    payload = {
        "requestId": result.request_id,
        "name": result.name,
        "score": result.score,
        "maxScore": result.max_score,
        "grade": result.grade,
        "primaryTitle": result.primary_title,
        "titles": result.titles,
        "comment": result.comment,
        "disclaimer": result.disclaimer,
        "stats": asdict(result.stats),
        "sharePayload": {
            "suggestedFileName": result.share_payload.suggested_file_name,
            "shareTitle": result.share_payload.share_title,
            "shareText": result.share_payload.share_text,
            "imageAlt": result.share_payload.image_alt,
        },
    }
    return payload
