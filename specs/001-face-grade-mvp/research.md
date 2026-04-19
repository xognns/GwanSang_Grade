# Research: 얼굴 성적기 MVP

## Decision 1: 프론트엔드는 React + TypeScript + Vite 기반 모바일 퍼스트 SPA로 구현한다

- **Decision**: `frontend/`는 React + TypeScript + Vite 조합으로 시작하고, 모바일 퍼스트 단일 페이지 흐름을 우선한다.
- **Rationale**: 저장소에 기존 웹앱 골격이 없고, 입력 → 결과 → 다운로드/공유까지의 짧은 흐름이므로 빠른 개발/테스트 루프와 모바일 레이아웃 제어가 쉬운 SPA 구성이 적합하다.
- **Alternatives considered**:
  - Next.js: 라우팅과 배포 옵션은 강하지만 현재 MVP는 서버 렌더링 요구가 없고 초기 복잡도가 증가한다.
  - 순수 React without Vite: 가능하지만 개발 서버와 번들 설정 비용이 늘어난다.

## Decision 2: 백엔드는 FastAPI 단일 서비스에서 동기식 분석 파이프라인을 제공한다

- **Decision**: `backend/`는 FastAPI 단일 프로세스 서비스로 시작하고, 한 요청 안에서 업로드 검증 → 얼굴 검출 → 랜드마크 추출 → 점수/등급/코멘트 산출을 완료한다.
- **Rationale**: MVP 범위는 단일 이미지 1장 처리와 즉시 결과 반환이며, 별도 큐나 워커를 도입할 만큼 트래픽 요구가 크지 않다. 동기식 파이프라인이 계약과 테스트를 단순하게 만든다.
- **Alternatives considered**:
  - Celery/RQ 비동기 큐: 대량 처리에는 유리하지만 MVP에서는 인프라와 상태 복잡도가 과도하다.
  - 서버리스 분석 함수: 배포는 단순할 수 있으나 MediaPipe/OpenCV 런타임 제약과 cold start 리스크가 있다.

## Decision 3: 모바일 공유는 Web Share API를 우선 사용하고 다운로드를 확실한 fallback으로 둔다

- **Decision**: 결과 이미지는 프론트엔드에서 PNG 파일로 렌더링하고, 모바일 브라우저에서 `navigator.canShare({ files })`가 가능할 때 `navigator.share()`를 사용한다. 불가능한 환경에서는 다운로드를 기본 fallback으로 제공한다.
- **Rationale**: 모바일 웹에서 사용자 기대 동선은 결과를 즉시 저장하거나 OS 공유 시트로 넘기는 것이다. Web Share API는 텍스트, URL, 파일 공유를 지원하지만, 지원 범위가 완전하지 않고 HTTPS, user activation, capability detection이 필요하므로 fallback이 필수다.
- **Alternatives considered**:
  - 인스타그램 전용 웹 딥링크: 플랫폼 의존성이 높고 웹 환경에서 안정성이 낮다.
  - 서버가 결과 이미지를 생성/보관 후 URL 공유: 임시 파일 관리와 개인정보 보관 리스크가 커진다.
  - 공유 기능 없이 다운로드만 제공: 사용자 요구인 인스타그램 스토리 공유를 직접 충족하지 못한다.
- **References**:
  - Web Share API: <https://developer.mozilla.org/en-US/docs/Web/API/Web_Share_API>
  - Navigator.share(): <https://developer.mozilla.org/en-US/docs/Web/API/Navigator/share>

## Decision 4: MVP에서는 영구 저장소를 두지 않고 기준 이미지와 임시 처리만 사용한다

- **Decision**: DB는 도입하지 않고, 기준 이미지 설정값과 임시 업로드/처리 결과만 메모리 또는 ephemeral filesystem 범위에서 관리한다.
- **Rationale**: 현재 범위는 로그인, 히스토리, 랭킹이 없고 얼굴 이미지를 영구 저장하지 않는 것이 핵심 원칙이므로 영구 저장소가 필요하지 않다.
- **Alternatives considered**:
  - PostgreSQL 도입: 후속 확장에는 유용하지만 MVP 요구사항에 비해 과하다.
  - S3/Object storage 영구 저장: 공유 URL 관리에는 도움이 되지만 얼굴 이미지 보관 정책과 충돌한다.

## Decision 5: 코멘트는 대표 칭호별 코멘트 풀에서 무작위 선택한다

- **Decision**: 분석 결과에서 대표 칭호를 정하고, 해당 칭호에 연결된 코멘트 후보군에서 하나를 무작위 선택한다.
- **Rationale**: 동일 점수대 결과라도 반복 경험의 재미를 유지할 수 있고, 프론트엔드는 단일 `comment` 문자열만 렌더링하면 된다.
- **Alternatives considered**:
  - 점수 기반 단일 템플릿: 구현은 단순하지만 결과가 빠르게 반복적으로 느껴진다.
  - LLM 기반 실시간 코멘트 생성: 비용, 지연, 품질 일관성 리스크가 MVP에 비해 크다.

## Decision 6: 계약 아티팩트는 OpenAPI + 결과 카드 스키마 두 층으로 정의한다

- **Decision**: 백엔드 외부 계약은 OpenAPI로, 프론트 결과 카드 렌더링 입력은 JSON Schema로 별도 정의한다.
- **Rationale**: React/FastAPI 분리 원칙상 HTTP 계약과 UI 렌더링 계약을 분리하면 테스트 범위와 책임이 명확해진다.
- **Alternatives considered**:
  - OpenAPI 하나로 모든 UI 요구까지 표현: 가능하지만 결과 카드의 렌더링 규칙과 공유 메타데이터가 흐려진다.
  - 문서 없는 암묵적 JSON 응답: 프론트/백엔드 협업 비용과 회귀 리스크가 커진다.

## Decision 7: CI는 프론트엔드와 백엔드 검증을 분리하고 문서 동기화 체크를 포함한다

- **Decision**: CI는 `frontend`와 `backend`를 별도 job으로 테스트하고, 계약/문서 변경 시 `Docs/` 동기화 여부를 같이 확인한다.
- **Rationale**: 헌법의 FE/BE 분리와 Docs 우선 원칙을 자동화된 게이트로 보장해야 한다.
- **Alternatives considered**:
  - 단일 통합 job: 초기 설정은 단순하지만 실패 원인 분리가 어렵다.
  - 수동 문서 확인: 누락이 발생하기 쉽고 협업 규칙을 강제하지 못한다.
