# Implementation Plan: [FEATURE]

**Feature ID**: `[###-feature-name]` | **Working Branch**: `[main|front-end|back-end]` | **Date**: [DATE] | **Spec**: [link]
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/plan-template.md` for the execution workflow.

## Summary

[Extract from feature spec: primary requirement + technical approach from research]

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: [e.g., Front-end: TypeScript/React, Back-end: Python/FastAPI or NEEDS CLARIFICATION]
**Primary Dependencies**: [e.g., React, FastAPI, pytest, frontend test runner or NEEDS CLARIFICATION]
**Storage**: [if applicable, e.g., PostgreSQL, CoreData, files or N/A]
**Testing**: [e.g., Front-end interaction tests, Back-end pytest, contract tests or NEEDS CLARIFICATION]
**Target Platform**: [e.g., Linux server, iOS 15+, WASM or NEEDS CLARIFICATION]
**Project Type**: [Web application with strict React/FastAPI separation]
**Performance Goals**: [domain-specific, e.g., 1000 req/s, 10k lines/sec, 60 fps or NEEDS CLARIFICATION]
**Constraints**: [domain-specific, e.g., <200ms p95, <100MB memory, offline-capable or NEEDS CLARIFICATION]
**Scale/Scope**: [domain-specific, e.g., 10k users, 1M LOC, 50 screens or NEEDS CLARIFICATION]

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [ ] Working branch is `main`, `front-end`, or `back-end`; no feature branch is required or created
- [ ] Impacted area is identified as `Front-end`, `Back-end`, or `Both`
- [ ] Front-end and Back-end responsibilities remain separated by HTTP/API contracts only
- [ ] Any contract change is documented in `Docs/` before or with implementation
- [ ] Tests are defined first for every affected layer and included in the plan
- [ ] CI verification commands for lint, test, and build are listed explicitly

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)
```text
Docs/
├── api/
├── schemas/
└── flows/

backend/
├── src/ or app/
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
    └── unit/
```

**Structure Decision**: [Document the selected directories above, identify the
affected area, and explain how `Docs/`, `frontend/`, and `backend/` stay
decoupled]

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
