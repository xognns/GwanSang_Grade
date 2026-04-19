from dataclasses import dataclass
from enum import Enum
from typing import Optional


class ErrorCode(str, Enum):
    missing_file = "missing_file"
    unsupported_format = "unsupported_format"
    file_too_large = "file_too_large"
    no_face = "no_face"
    multiple_faces = "multiple_faces"
    share_unavailable = "share_unavailable"
    analysis_failed = "analysis_failed"


@dataclass(frozen=True)
class ErrorDescriptor:
    code: ErrorCode
    message: str
    recoverable: bool = True


ERROR_MESSAGES = {
    ErrorCode.missing_file: "사진 파일이 없습니다.",
    ErrorCode.unsupported_format: "지원하지 않는 파일 형식입니다. jpg/jpeg 또는 png만 업로드 가능합니다.",
    ErrorCode.file_too_large: "사진 파일이 너무 큽니다. 10MB 이하를 업로드하세요.",
    ErrorCode.no_face: "얼굴이 감지되지 않았습니다. 얼굴이 선명하게 보이는 이미지를 다시 업로드하세요.",
    ErrorCode.multiple_faces: "한 장면에 한 사람만 있어야 합니다. 얼굴이 하나만 보이도록 촬영/크롭해주세요.",
    ErrorCode.share_unavailable: "현재 환경에서는 공유 기능을 지원하지 않습니다.",
    ErrorCode.analysis_failed: "분석 과정에서 오류가 발생했습니다. 잠시 후 다시 시도하세요.",
}


def describe_error(code: ErrorCode) -> ErrorDescriptor:
    return ErrorDescriptor(code=code, message=ERROR_MESSAGES[code], recoverable=True)
