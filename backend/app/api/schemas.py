from dataclasses import dataclass
from typing import Annotated, Literal

from fastapi import File, Form, UploadFile
from pydantic import BaseModel, Field


ALLOWED_IMAGE_MIME = ("image/jpeg", "image/png", "image/jpg")


class StatModel(BaseModel):
    focus: int = Field(ge=0, le=100)
    diligence: int = Field(ge=0, le=100)
    execution: int = Field(ge=0, le=100)
    cramming: int = Field(ge=0, le=100)
    luck: int = Field(ge=0, le=100)


class SharePayloadModel(BaseModel):
    suggestedFileName: str
    shareTitle: str
    shareText: str
    imageAlt: str


class AnalysisResponseModel(BaseModel):
    requestId: str
    name: str = Field(min_length=1, max_length=20)
    score: float = Field(ge=0.0, le=4.5)
    maxScore: float = Field(ge=4.5, le=4.5)
    grade: Literal["A+", "A0", "B+", "B0", "C+", "C0", "D+", "D0", "F"]
    primaryTitle: str
    titles: list[str] = Field(min_length=2, max_length=3)
    comment: str
    disclaimer: str
    stats: StatModel
    sharePayload: SharePayloadModel


class ErrorResponseModel(BaseModel):
    code: str
    message: str
    recoverable: bool


def analysis_form(
    name: Annotated[str, Form()] = "",
    file: Annotated[UploadFile | None, File(description="jpg/jpeg 또는 png 파일")] = None,
) -> tuple[str, UploadFile | None]:
    if file is None:
        raise ValueError("missing_file")
    return name, file


@dataclass(frozen=True)
class ErrorEnvelope:
    code: str
    message: str
    recoverable: bool = True
