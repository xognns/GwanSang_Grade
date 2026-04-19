# Tasks: 얼굴 성적기 MVP

**Input**: Design documents from `/specs/001-face-grade-mvp/`
**Prerequisites**: [plan.md](/Users/wonny/src/Project/Team/AnimalLeague/GwanSang_Grade/specs/001-face-grade-mvp/plan.md), [spec.md](/Users/wonny/src/Project/Team/AnimalLeague/GwanSang_Grade/specs/001-face-grade-mvp/spec.md)
**Tests**: Tests are MANDATORY. Every user story starts with failing tests for the affected layer(s).

## Phase 1: Setup (Shared Infrastructure)

- [x] [T001] Create folder scaffolding `backend/app/` and `frontend/src/` structure from implementation plan
- [x] [T002] Add shared `.gitignore` and temp artifact ignore rules for upload/result artifacts in repo root
- [x] [T003] Add backend packaging and dependency baseline in `backend/requirements-dev.txt`
- [ ] [T004] Add frontend dependencies and scripts in `frontend/package.json` for React 19/Vite/Vitest/Playwright
- [ ] [T005] [P] Configure `backend/` and `frontend/` test runners (`pytest` and `vitest`) in local config files
- [ ] [T006] [P] Configure `frontend/.env.example` and `backend/.env.example` with API base url and media limits

## Phase 2: Foundational (Blocking Prerequisites)

- [x] [T007] Add docs-first API contract files in `Docs/api/analysis-api.openapi.yaml` and `Docs/schemas/result-card-view-model.schema.json`
- [x] [T008] [P] Add canonical example payload and error fixtures in `backend/tests/fixtures/`
- [x] [T009] [P] Add API boundary DTOs and validation models in `backend/app/domain/models.py`
- [x] [T010] [P] Add shared error response contract in `backend/app/domain/errors.py`
- [ ] [T011] [P] Establish frontend API client contracts in `frontend/src/services/api/contracts.ts`
- [ ] [T012] [P] Create reusable parser/formatter for result-card view model in `frontend/src/services/result/model.ts`
- [x] [T013] Configure integration test harness for API route tests in `backend/tests/conftest.py`
- [x] [T014] Configure contract-focused Playwright test setup in `frontend/tests/playwright.config.ts`

## Phase 3: User Story 1 - 사진으로 성적 조회 (Priority: P1) 🎯 MVP

**Goal**: 이름과 단일 얼굴 사진 제출 후 결과 화면을 성공적으로 렌더링

**Independent Test**: 이름과 jpg/png(10MB 이하) 단일 얼굴 이미지를 제출했을 때 결과 화면에 점수, 등급, 칭호, 코멘트가 노출되면 검증 완료

### Tests for User Story 1 (MANDATORY)

- [x] [T015] [P] [US1] Add API contract test in `backend/tests/contract/test_create_analysis_success.py`
- [x] [T016] [P] [US1] Add backend unit test for valid input + baseline scoring in `backend/tests/unit/test_analysis_scoring.py`
- [x] [T017] [P] [US1] Add frontend happy-path component test in `frontend/tests/unit/ResultView.test.tsx`

### Implementation for User Story 1

- [x] [T018] Update docs for success contract examples in `Docs/api/analysis-api.openapi.yaml`
- [x] [T019] [P] [US1] Implement multipart request schema validation in `backend/app/api/schemas.py`
- [x] [T020] [P] [US1] Add request handling endpoint `POST /api/v1/analyses` in `backend/app/api/analyses.py`
- [x] [T021] [P] [US1] Implement analysis pipeline orchestration in `backend/app/services/analysis_service.py`
- [x] [T022] [US1] Implement deterministic score/grade/comment synthesis in `backend/app/domain/grade_service.py`
- [x] [T023] [US1] Add result card API response mapper in `backend/app/services/result_mapper.py`
- [ ] [T024] [US1] Build desktop/mobile input UI flow in `frontend/src/pages/MainPage.tsx`
- [ ] [T025] [P] [US1] Add result view card render and state handling in `frontend/src/pages/ResultPage.tsx`
- [ ] [T026] [US1] Wire API client request from UI in `frontend/src/services/api/analysisClient.ts`
- [ ] [T027] [US1] Run `frontend/tests/e2e/us1-result-success.spec.ts` against mobile viewport smoke flow in `frontend/tests/e2e/`

## Phase 4: User Story 2 - 잘못된 사진에 대한 안내 (Priority: P2)

**Goal**: 비정상 입력 제출 시 사용자 이해 가능한 실패 메시지와 재시도 경로 제공

**Independent Test**: 얼굴 없음/복수 얼굴/지원 형식 오류 입력에서 오류 메시지가 노출되고 재시도 유도가 되면 검증 완료

### Tests for User Story 2 (MANDATORY)

- [x] [T028] [P] [US2] Add backend API test for invalid formats and face-count failures in `backend/tests/contract/test_create_analysis_failures.py`
- [ ] [T029] [P] [US2] Add frontend error-banner/component tests in `frontend/tests/unit/ErrorState.test.tsx`
- [ ] [T030] [US2] Add edge-case e2e test for missing name/photo in `frontend/tests/e2e/us2-invalid-input.spec.ts`

### Implementation for User Story 2

- [x] [T031] [US2] Add explicit validation failure branching and error codes in `backend/app/services/validation_service.py`
- [x] [T032] [US2] Extend schema error response to include recoverable messages in `backend/app/domain/errors.py`
- [x] [T033] [US2] Add shared `ErrorResponse` fixture in `backend/tests/fixtures/error_cases.json`
- [ ] [T034] [US2] Add reusable error mapping utility in `frontend/src/services/error/errorMapper.ts`
- [ ] [T035] [US2] Implement invalid input precheck and disabled submit control in `frontend/src/components/SubmissionForm.tsx`
- [ ] [T036] [US2] Add recoverable retry CTA and copy in `frontend/src/components/RetryPrompt.tsx`
- [x] [T037] [US2] Sync failure contract references in `Docs/api/analysis-api.openapi.yaml`

## Phase 5: User Story 3 - 결과 저장과 공유 (Priority: P3)

**Goal**: 결과 카드 저장 또는 인스타그램 스토리 공유 동선 완료

**Independent Test**: 결과 화면에서 다운로드 또는 인스타그램 스토리 공유 버튼을 실행해 저장/공유 흐름이 시작되면 검증 완료

### Tests for User Story 3 (MANDATORY)

- [ ] [T038] [P] [US3] Add frontend unit test for result actions in `frontend/tests/unit/ResultActions.test.tsx`
- [x] [T039] [P] [US3] Add backend contract test for share payload field presence in `backend/tests/contract/test_share_payload.py`
- [ ] [T040] [US3] Add mobile-share e2e smoke for fallback behavior in `frontend/tests/e2e/us3-share-fallback.spec.ts`

### Implementation for User Story 3

- [x] [T041] [US3] Generate share payload metadata in `backend/app/domain/models.py` and `backend/app/services/result_mapper.py`
- [ ] [T042] [US3] Add result-card export utility in `frontend/src/services/result/cardRenderer.ts`
- [ ] [T043] [US3] Add download action and file name policy in `frontend/src/services/result/actions.ts`
- [ ] [T044] [US3] Add Web Share API + capability detection fallback in `frontend/src/hooks/useShareResult.ts`
- [ ] [T045] [US3] Add Instagram story deep-link helper in `frontend/src/services/share/instagram.ts`
- [ ] [T046] [US3] Add user-facing fallback messaging for unsupported environments in `frontend/src/components/ShareFallback.tsx`

## Phase 6: Polish & Cross-Cutting Concerns

- [ ] [T047] [P] Add mobile a11y checks and focus flow in `frontend/tests/accessibility.spec.ts`
- [ ] [T048] Add docs alignment for `docs/mvp-spec.md` and `Docs/mvp-spec.md` from finalized contract artifacts
- [x] [T049] Add CI validation script in `.github/workflows/ci.yml` for lint/test/build + docs sync
- [x] [T050] [P] Add `backend/tests/integration/test_end_to_end_analysis_flow.py`
- [ ] [T051] [P] Run `frontend/tests/e2e` and `backend/tests` with mobile-focused smoke cases
- [ ] [T052] [P] Final review of constitutional gates in `specs/001-face-grade-mvp/plan.md`

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependency, can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion and blocks all stories
- **User Stories**: Depend on Foundational completion; can run in priority order or in parallel where task ownership differs
- **Polish (Phase 6)**: Depends on all selected stories

### User Story Dependencies

- **US1 (P1)**: Can start after Foundational only
- **US2 (P2)**: Can start after Foundational and can be validated independently
- **US3 (P3)**: Can start after Foundational and can be validated independently

## Parallel Opportunities

- **Phase 1**: T001~T005 are parallel except when directory creation conflicts are resolved by one commit
- **Phase 2**: T007~T013 are parallel except for shared test data fixtures
- **US1**: T014~T016 parallelizable; implementation can split FE/BE after `Docs/api/analysis-api.openapi.yaml` is updated
- **US2**: T026~T028 and T032~T034 are parallel after US1 pipeline validation
- **US3**: T036~T038 and T041~T044 are parallel after share payload is defined

## Parallel Example: User Story 1

```bash
Task: "T014 [P] [US1] Add API contract test in backend/tests/contract/test_create_analysis_success.py"
Task: "T015 [P] [US1] Add backend unit test for valid input + baseline scoring in backend/tests/unit/test_analysis_scoring.py"
Task: "T016 [P] [US1] Add frontend happy-path component test in frontend/tests/unit/ResultView.test.tsx"
```

## Implementation Strategy

### MVP First (User Story 1 Only)

1. 완료: Phase 1 + Phase 2
2. 완료: Phase 3(US1) 테스트 포함
3. 단일 배포 또는 데모로 US1 범위를 검증

### Incremental Delivery

1. Setup + Foundational 완료
2. US1 구현/검증
3. US2 구현/검증
4. US3 구현/검증
5. 각 단계마다 폴리싱 체크포인트 수행
