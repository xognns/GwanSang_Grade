# Data Model: 얼굴 성적기 MVP

## Overview

이 MVP는 영구 저장소 없이 요청 단위의 분석 흐름을 처리한다. 데이터 모델은 업로드 검증,
분석 산출, 결과 렌더링, 다운로드/공유 흐름을 명확히 분리하는 데 초점을 둔다.

## Entity: AnalysisRequest

**Purpose**: 사용자가 제출한 이름과 이미지, 그리고 처리 상태를 표현한다.

| Field | Type | Required | Rules |
| --- | --- | --- | --- |
| `requestId` | UUID | Yes | 요청 생성 시 서버가 발급 |
| `displayName` | string | Yes | trim 후 1~20자, 빈 문자열 불가 |
| `imageFileName` | string | Yes | 원본 파일명 유지, UI 표시에는 직접 사용하지 않음 |
| `imageMimeType` | enum | Yes | `image/jpeg`, `image/png`만 허용 |
| `imageSizeBytes` | integer | Yes | 1 byte 이상, 10MB 이하 |
| `status` | enum | Yes | `received`, `validated`, `analyzing`, `completed`, `failed` |
| `submittedAt` | datetime | Yes | UTC timestamp |

**Relationships**:

- 성공 시 하나의 `AnalysisResult`를 생성한다.
- 실패 시 하나의 `ValidationError` 또는 `AnalysisFailure`를 남긴다.

**State transitions**:

`received` → `validated` → `analyzing` → `completed`
`received` → `failed`
`validated` → `failed`
`analyzing` → `failed`

## Entity: FaceValidationResult

**Purpose**: 입력 이미지가 분석 가능한지 판정한 중간 결과다.

| Field | Type | Required | Rules |
| --- | --- | --- | --- |
| `faceCount` | integer | Yes | 0 이상 |
| `isSupportedFormat` | boolean | Yes | MIME/type 검증 결과 |
| `isSizeAllowed` | boolean | Yes | 10MB 이하 여부 |
| `isSingleFace` | boolean | Yes | 얼굴 1개만 허용 |
| `failureCode` | enum | No | `missing_file`, `unsupported_format`, `file_too_large`, `no_face`, `multiple_faces` |

## Entity: StatBreakdown

**Purpose**: 결과 화면의 세부 스탯 바와 점수 계산 근거를 표현한다.

| Field | Type | Required | Rules |
| --- | --- | --- | --- |
| `focus` | number | Yes | 0~100 |
| `diligence` | number | Yes | 0~100 |
| `execution` | number | Yes | 0~100 |
| `cramming` | number | Yes | 0~100 |
| `luck` | number | Yes | 0~100 |

## Entity: GradeBand

**Purpose**: 정규화 점수를 고정 등급 문자열로 변환한다.

| Field | Type | Required | Rules |
| --- | --- | --- | --- |
| `grade` | enum | Yes | `A+`, `A0`, `B+`, `B0`, `C+`, `C0`, `D+`, `D0`, `F` |
| `minInclusive` | number | Yes | 0.0~4.5 |
| `maxExclusive` | number | No | 최상단 등급 외에는 상한 정의 |

**Canonical bands**:

- `A+`: 4.3 이상
- `A0`: 4.0 이상 4.3 미만
- `B+`: 3.5 이상 4.0 미만
- `B0`: 3.0 이상 3.5 미만
- `C+`: 2.5 이상 3.0 미만
- `C0`: 2.0 이상 2.5 미만
- `D+`: 1.5 이상 2.0 미만
- `D0`: 1.0 이상 1.5 미만
- `F`: 1.0 미만

## Entity: TitleRule

**Purpose**: 스탯 조합 또는 보너스 규칙으로 결과 칭호를 결정한다.

| Field | Type | Required | Rules |
| --- | --- | --- | --- |
| `titleKey` | string | Yes | 내부 식별자 |
| `titleLabel` | string | Yes | 사용자 노출 텍스트 |
| `priority` | integer | Yes | 대표 칭호 결정용 우선순위 |
| `matchCondition` | object | Yes | 임계값 또는 최고 스탯 조건 |
| `bonusScore` | number | No | 추가 raw score 보정치 |

## Entity: CommentPool

**Purpose**: 대표 칭호별 랜덤 코멘트 후보군을 제공한다.

| Field | Type | Required | Rules |
| --- | --- | --- | --- |
| `titleKey` | string | Yes | `TitleRule.titleKey`와 연결 |
| `comments` | string[] | Yes | 최소 2개 이상 후보 |
| `selectionStrategy` | enum | Yes | MVP는 `random_uniform` 고정 |

## Entity: AnalysisResult

**Purpose**: 사용자에게 반환되는 최종 분석 결과다.

| Field | Type | Required | Rules |
| --- | --- | --- | --- |
| `requestId` | UUID | Yes | `AnalysisRequest.requestId` 참조 |
| `displayName` | string | Yes | 요청 이름 그대로 사용 |
| `score` | number | Yes | 0.0~4.5, 소수 1자리 |
| `maxScore` | number | Yes | 4.5 고정 |
| `grade` | enum | Yes | `GradeBand.grade` 중 하나 |
| `primaryTitle` | string | Yes | 대표 칭호 1개 |
| `titles` | string[] | Yes | 2~3개 노출 |
| `comment` | string | Yes | `CommentPool`에서 선택된 텍스트 |
| `stats` | `StatBreakdown` | Yes | 세부 스탯 |
| `disclaimer` | string | Yes | 재미용 안내 문구 |
| `sharePayload` | `SharePayload` | Yes | 다운로드/공유에 필요한 메타데이터 |

## Entity: SharePayload

**Purpose**: 프론트엔드가 결과 카드를 렌더링하고 다운로드/공유를 수행할 때 사용하는 메타데이터다.

| Field | Type | Required | Rules |
| --- | --- | --- | --- |
| `suggestedFileName` | string | Yes | `.png` 확장자 포함 |
| `shareTitle` | string | Yes | 모바일 공유 시트 제목 |
| `shareText` | string | Yes | 공유 본문 텍스트 |
| `imageAlt` | string | Yes | 접근성 설명 |

**State transitions**:

`pending_render` → `rendered`
`rendered` → `downloaded`
`rendered` → `shared`
`rendered` → `share_unavailable`

## Entity: ValidationError

**Purpose**: 사용자가 수정 가능한 실패 상황을 표준화한다.

| Field | Type | Required | Rules |
| --- | --- | --- | --- |
| `code` | enum | Yes | `missing_file`, `unsupported_format`, `file_too_large`, `no_face`, `multiple_faces`, `share_unavailable` |
| `message` | string | Yes | 사용자 안내 문구 |
| `recoverable` | boolean | Yes | MVP에서는 모두 `true` |

## Entity: ReferenceBaseline

**Purpose**: 0.0 기준점과 튜닝 상한을 정의한다.

| Field | Type | Required | Rules |
| --- | --- | --- | --- |
| `baselineId` | string | Yes | 활성 기준 이미지 식별자 |
| `rawScore` | number | Yes | 0 이상 100 이하 |
| `assetPath` | string | Yes | repo or runtime asset path |
| `isActive` | boolean | Yes | 단일 활성 기준만 허용 |

## Validation Summary

- 이름, 파일 형식, 파일 크기, 얼굴 개수 검증은 API 진입점에서 수행한다.
- 등급 변환과 코멘트 선택은 항상 `AnalysisResult` 생성 전에 완료한다.
- 다운로드/공유는 `AnalysisResult.sharePayload`가 존재할 때만 활성화된다.
