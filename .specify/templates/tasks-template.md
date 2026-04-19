---

description: "Task list template for feature implementation"
---

# Tasks: [FEATURE NAME]

**Input**: Design documents from `/specs/[###-feature-name]/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are MANDATORY. Every user story MUST start with failing tests for the affected layer(s) before implementation tasks are listed.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Front-end**: `frontend/src/`, `frontend/tests/`
- **Back-end**: `backend/src/` or `backend/app/`, `backend/tests/`
- **Contracts & Specs**: `Docs/`
- Paths shown below assume the React/FastAPI split mandated by the constitution

<!-- 
  ============================================================================
  IMPORTANT: The tasks below are SAMPLE TASKS for illustration purposes only.
  
  The /speckit.tasks command MUST replace these with actual tasks based on:
  - User stories from spec.md (with their priorities P1, P2, P3...)
  - Feature requirements from plan.md
  - Entities from data-model.md
  - Endpoints from contracts/
  
  Tasks MUST be organized by user story so each story can be:
  - Implemented independently
  - Tested independently
  - Delivered as an MVP increment
  
  DO NOT keep these sample tasks in the generated tasks.md file.
  ============================================================================
-->

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create or align `frontend/`, `backend/`, and `Docs/` structure per implementation plan
- [ ] T002 Initialize front-end and back-end dependencies for the chosen scope
- [ ] T003 [P] Configure linting, formatting, and test runners for each affected layer
- [ ] T004 [P] Configure CI jobs for lint, test, build, and documentation sync checks

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

Examples of foundational tasks (adjust based on your project):

- [ ] T005 Define or update API contracts and schemas in `Docs/`
- [ ] T006 [P] Establish frontend API boundary and request client structure in `frontend/src/`
- [ ] T007 [P] Establish FastAPI routing, service, and test harness structure in `backend/`
- [ ] T008 [P] Create shared fixtures or mock payloads derived from `Docs/`
- [ ] T009 Configure error handling, logging, and environment management for the affected layer(s)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - [Title] (Priority: P1) 🎯 MVP

**Goal**: [Brief description of what this story delivers]

**Independent Test**: [How to verify this story works on its own]

### Tests for User Story 1 (MANDATORY) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T010 [P] [US1] Add backend contract or API test in `backend/tests/contract/`
- [ ] T011 [P] [US1] Add frontend user-flow test in `frontend/tests/`

### Implementation for User Story 1

- [ ] T012 [US1] Update `Docs/` contract files, examples, and error cases for the story
- [ ] T013 [P] [US1] Implement frontend changes in `frontend/src/`
- [ ] T014 [P] [US1] Implement backend changes in `backend/src/` or `backend/app/`
- [ ] T015 [US1] Wire documented request/response handling across the boundary
- [ ] T016 [US1] Add validation and error handling
- [ ] T017 [US1] Verify CI commands for this story's scope

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - [Title] (Priority: P2)

**Goal**: [Brief description of what this story delivers]

**Independent Test**: [How to verify this story works on its own]

### Tests for User Story 2 (MANDATORY) ⚠️

- [ ] T018 [P] [US2] Add backend contract or API test in `backend/tests/contract/`
- [ ] T019 [P] [US2] Add frontend user-flow test in `frontend/tests/`

### Implementation for User Story 2

- [ ] T020 [US2] Update `Docs/` contract files, examples, and edge cases for the story
- [ ] T021 [P] [US2] Implement frontend changes in `frontend/src/`
- [ ] T022 [P] [US2] Implement backend changes in `backend/src/` or `backend/app/`
- [ ] T023 [US2] Integrate only through documented contracts and shared fixtures

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - [Title] (Priority: P3)

**Goal**: [Brief description of what this story delivers]

**Independent Test**: [How to verify this story works on its own]

### Tests for User Story 3 (MANDATORY) ⚠️

- [ ] T024 [P] [US3] Add backend contract or API test in `backend/tests/contract/`
- [ ] T025 [P] [US3] Add frontend user-flow test in `frontend/tests/`

### Implementation for User Story 3

- [ ] T026 [US3] Update `Docs/` contract files, examples, and edge cases for the story
- [ ] T027 [P] [US3] Implement frontend changes in `frontend/src/`
- [ ] T028 [P] [US3] Implement backend changes in `backend/src/` or `backend/app/`
- [ ] T029 [US3] Verify CI commands and documented boundary behavior

**Checkpoint**: All user stories should now be independently functional

---

[Add more user story phases as needed, following the same pattern]

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] TXXX [P] Documentation updates in `Docs/`
- [ ] TXXX Code cleanup and refactoring
- [ ] TXXX Performance optimization across all stories
- [ ] TXXX [P] Additional unit tests in `frontend/tests/` or `backend/tests/`
- [ ] TXXX Security hardening
- [ ] TXXX Run quickstart.md validation

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable

### Within Each User Story

- Tests MUST be written and FAIL before implementation
- `Docs/` contract updates MUST happen before cross-layer integration work
- Front-end and Back-end tasks MUST stay in their own file sets
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, user stories can start in parallel if file ownership and contract changes do not conflict
- All tests for a user story marked [P] can run in parallel
- Front-end and Back-end implementation within a story can run in parallel after `Docs/` updates land
- Different user stories can be worked on in parallel by different team members on the allowed collaborative branches

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together (if tests requested):
Task: "Add backend contract or API test in backend/tests/contract/"
Task: "Add frontend user-flow test in frontend/tests/"

# Once Docs updates are done, implement both sides in parallel:
Task: "Implement frontend changes in frontend/src/"
Task: "Implement backend changes in backend/src/ or backend/app/"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: Front-end scope for User Story 1
   - Developer B: Back-end scope for User Story 1
   - Developer C: Next prioritized story after contract alignment
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
