from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from backend.app.domain.errors import ErrorCode, describe_error
from backend.app.services.analysis_service import AnalysisService
from backend.app.api.schemas import AnalysisResponseModel, analysis_form
from backend.app.services.validation_service import MAX_SIZE_BYTES
from backend.app.services.result_mapper import to_api_response

router = APIRouter()


@router.post("/api/v1/analyses")
async def create_analysis(
    form: tuple[str, object] = Depends(analysis_form),
):
    name, file = form
    if file is None:
        descriptor = describe_error(ErrorCode.missing_file)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"code": descriptor.code, "message": descriptor.message, "recoverable": descriptor.recoverable},
        )

    content = await file.read(MAX_SIZE_BYTES + 1)
    if len(content) > MAX_SIZE_BYTES:
        descriptor = describe_error(ErrorCode.file_too_large)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"code": descriptor.code, "message": descriptor.message, "recoverable": descriptor.recoverable},
        )

    service = AnalysisService()
    result, error_code = service.run(
        name=name,
        file_name=file.filename or "",
        file_bytes=content,
        content_type=file.content_type,
    )
    if error_code:
        http_status = (
            status.HTTP_400_BAD_REQUEST
            if error_code in {ErrorCode.missing_file, ErrorCode.unsupported_format, ErrorCode.file_too_large}
            else status.HTTP_422_UNPROCESSABLE_ENTITY
            if error_code in {ErrorCode.no_face, ErrorCode.multiple_faces}
            else status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        descriptor = describe_error(error_code)
        return JSONResponse(
            status_code=http_status,
            content={"code": descriptor.code, "message": descriptor.message, "recoverable": descriptor.recoverable},
        )

    response = to_api_response(result)
    return AnalysisResponseModel(**response)
