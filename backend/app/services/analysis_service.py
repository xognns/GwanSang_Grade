from hashlib import sha256
from uuid import uuid4

from backend.app.domain.grade_service import build_result
from backend.app.domain.models import AnalysisRequest, AnalysisResult, SharePayload
from backend.app.domain.errors import ErrorCode
from backend.app.services.validation_service import validate_upload


class AnalysisService:
    DISCLAIMER = "본 결과는 재미를 위한 지수이며 실제 학업 성과를 평가하지 않습니다."

    def run(self, name: str, file_name: str, file_bytes: bytes, content_type: str | None) -> tuple[AnalysisResult | None, ErrorCode | None]:
        validation = validate_upload(name=name, file_name=file_name, file_bytes=file_bytes, content_type=content_type)
        if not validation.is_valid:
            return None, validation.failure

        try:
            request_id = str(uuid4())
            request = AnalysisRequest(
                request_id=request_id,
                display_name=name.strip(),
                image_file_name=file_name,
                image_mime_type=(content_type or "image/jpeg"),
                image_size_bytes=len(file_bytes),
            )

            seed = int(sha256(file_bytes).hexdigest()[:8], 16)
            grade_result = build_result(seed)
            safe_name = request.display_name[:20]

            share_payload = SharePayload(
                suggested_file_name=f"{safe_name}_{request.request_id[:8]}.png",
                share_title=f"{safe_name} 성적표",
                share_text=f"{safe_name}님의 성적은 {grade_result.grade}입니다.",
                image_alt=f"{safe_name}의 결과 카드 이미지",
            )

            result = AnalysisResult(
                request_id=request_id,
                name=safe_name,
                score=grade_result.score,
                max_score=4.5,
                grade=grade_result.grade,
                primary_title=grade_result.titles[0],
                titles=grade_result.titles,
                comment=grade_result.comment,
                disclaimer=self.DISCLAIMER,
                stats=grade_result.stats,
                share_payload=share_payload,
            )
            return result, None
        except Exception:
            return None, ErrorCode.analysis_failed
