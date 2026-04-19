# Implementation Plan: 얼굴 성적기 MVP

**Feature ID**: `001-face-grade-mvp` | **Working Branch**: `main` | **Date**: 2026-04-19 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-face-grade-mvp/spec.md`

**Note**: This plan covers Phase 0 research and Phase 1 design artifacts for the mobile-first face grade web MVP.

## Summary

모바일 퍼스트 React 웹앱이 이름과 얼굴 이미지를 수집하고, FastAPI 분석 서비스가 단일 얼굴 검증,
랜드마크 추출, 점수 계산, 9단계 등급 변환, 칭호 기반 코멘트 선택을 수행한다. 결과 화면은 모바일
한 화면 흐름 안에서 점수, 등급, 코멘트, 칭호를 보여주고, 프론트엔드가 결과 카드 이미지를
클라이언트에서 렌더링해 다운로드와 모바일 공유를 처리한다.

## Technical Context

**Language/Version**: Front-end: TypeScript 5.x + React 19; Back-end: Python 3.12 + FastAPI
**Primary Dependencies**: React, Vite, React Testing Library, Vitest, Playwright, FastAPI, Pydantic v2, MediaPipe Face Mesh, OpenCV, NumPy, pytest, httpx
**Storage**: Persistent database 없음; 기준 이미지 메타데이터와 임시 업로드 처리만 사용하는 ephemeral filesystem
**Testing**: Front-end unit/integration tests with Vitest + React Testing Library, mobile viewport smoke with Playwright, Back-end unit/integration/contract tests with pytest + httpx
**Target Platform**: HTTPS 기반 모바일 퍼스트 웹 UI + Linux-hosted FastAPI service
**Project Type**: Web application with strict React/FastAPI separation
**Performance Goals**: 단일 10MB 이하 이미지 기준 분석 요청 p95 5초 이내, 모바일 사용자가 확대나 가로 스크롤 없이 핵심 흐름 완료
**Constraints**: jpg/jpeg/png only, max 10MB, single-face only, no persistent biometric storage, `Docs/` contract-first workflow, mobile share requires HTTPS + user activation + capability detection fallback
**Scale/Scope**: MVP 1개 핵심 제출 흐름, 동시 대량 처리 없음, 초기 운영 기준 일 1천건 이하 분석 트래픽

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Pre-design gate:

- [x] Working branch is `main`, `front-end`, or `back-end`; no feature branch is required or created
- [x] Impacted area is identified as `Both`
- [x] Front-end and Back-end responsibilities remain separated by HTTP/API contracts only
- [x] Any contract change is documented in `Docs/` before or with implementation
- [x] Tests are defined first for every affected layer and included in the plan
- [x] CI verification commands for lint, test, and build are listed explicitly

Post-design re-check:

- [x] `research.md`, `data-model.md`, `contracts/`, `quickstart.md` all preserve `Docs/`-first contract management
- [x] Result rendering/share asset ownership stays in `frontend/`; image analysis and scoring stay in `backend/`
- [x] Design artifacts define TDD and CI gates for both layers without constitutional violations

## Project Structure

### Documentation (this feature)

```text
specs/001-face-grade-mvp/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   ├── analysis-api.openapi.yaml
│   └── result-card-view-model.schema.json
└── tasks.md
```

### Source Code (repository root)

```text
Docs/
├── api/
├── schemas/
└── flows/

backend/
├── app/
│   ├── api/
│   ├── services/
│   ├── domain/
│   └── infrastructure/
└── tests/
    ├── contract/
    ├── integration/
    └── unit/

frontend/
├── src/
│   ├── components/
│   ├── features/
│   ├── pages/
│   └── services/
└── tests/
    ├── integration/
    ├── unit/
    └── e2e/
```

**Structure Decision**: 현재 저장소는 명세와 스펙만 존재하므로 이번 구현에서 `frontend/`와 `backend/`
를 새로 만든다. `backend/app`은 업로드 검증, 얼굴 분석, 점수 계산, 코멘트 선택, 계약 응답 생성을
소유하고, `frontend/src`는 모바일 입력/결과 UI와 결과 카드 렌더링, 다운로드/공유를 소유한다.
`Docs/`는 구현 단계에서 승격될 공식 계약 문서 위치이며, `specs/.../contracts/`는 그 선행 설계
아티팩트다.

## Complexity Tracking

No constitutional violations identified in this plan.
