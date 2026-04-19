from dataclasses import dataclass
from typing import List

from .errors import ErrorDescriptor, ErrorCode


GRADE_LABELS = ("A+", "A0", "B+", "B0", "C+", "C0", "D+", "D0", "F")


@dataclass(frozen=True)
class AnalysisRequest:
    request_id: str
    display_name: str
    image_file_name: str
    image_mime_type: str
    image_size_bytes: int


@dataclass(frozen=True)
class StatBreakdown:
    focus: int
    diligence: int
    execution: int
    cramming: int
    luck: int


@dataclass(frozen=True)
class SharePayload:
    suggested_file_name: str
    share_title: str
    share_text: str
    image_alt: str


@dataclass(frozen=True)
class AnalysisResult:
    request_id: str
    name: str
    score: float
    max_score: float
    grade: str
    primary_title: str
    titles: List[str]
    comment: str
    disclaimer: str
    stats: StatBreakdown
    share_payload: SharePayload


@dataclass(frozen=True)
class ValidationResult:
    is_valid: bool
    failure: ErrorDescriptor | None = None


@dataclass(frozen=True)
class ValidationOutput:
    face_count: int


def as_error_response(error_code: ErrorCode) -> ErrorDescriptor:
    from .errors import describe_error

    return describe_error(error_code)
