<!--
Sync Impact Report
Version change: template draft -> 1.0.0
Modified principles:
- Template Principle 1 -> I. Frontend-Backend 분리
- Template Principle 2 -> II. Docs 우선 계약 관리
- Template Principle 3 -> III. Test-Driven Development
- Template Principle 4 -> IV. 확장 가능한 모듈 아키텍처
- Template Principle 5 -> V. 제한된 브랜치와 CI 게이트
Added sections:
- Technology & Repository Standards
- Workflow & Quality Gates
Removed sections:
- 없음
Templates requiring updates:
- ✅ .specify/templates/plan-template.md
- ✅ .specify/templates/spec-template.md
- ✅ .specify/templates/tasks-template.md
- ✅ .specify/extensions.yml
- ✅ .specify/extensions/git/commands/speckit.git.feature.md
- ✅ .specify/extensions/git/commands/speckit.git.validate.md
- ✅ .specify/extensions/git/README.md
- ✅ README.md
Follow-up TODOs:
- 없음
-->
# 얼굴 성적기 Constitution

## Core Principles

### I. Frontend-Backend 분리
React 프론트엔드는 `frontend/`에서, FastAPI 백엔드는 `backend/`에서 독립적인
빌드, 테스트, 배포 단위로 유지한다. 프론트엔드는 백엔드 내부 모듈을 직접 import
해서는 안 되며, 백엔드는 프론트엔드 구현 세부사항에 의존해서는 안 된다. 두 영역의
통신은 문서화된 HTTP API 계약만 통해야 한다. 이 원칙은 계층 누수를 막고 병렬 개발
및 독립 배포 가능성을 유지하기 위한 것이다.

### II. Docs 우선 계약 관리
`Docs/`는 API 명세, 요청 및 응답 스키마, 오류 규약, 통합 흐름을 저장하는 단일
출처다. 프론트엔드-백엔드 경계에 영향을 주는 변경은 코드와 함께 `Docs/`를 먼저
혹은 동시에 갱신해야 하며, 문서 없이 인터페이스를 변경해서는 안 된다. 이 원칙은
구현보다 계약을 우선하고 팀 간 오해를 줄이기 위한 것이다.

### III. Test-Driven Development
모든 기능과 버그 수정은 실패하는 테스트를 먼저 작성한 뒤 구현한다. React 영역은
컴포넌트 및 사용자 상호작용 테스트를, FastAPI 영역은 단위 테스트, API 테스트,
통합 테스트를 우선 정의해야 한다. 테스트 없는 기능 추가나 회귀 재현 없는 버그
수정은 허용하지 않는다. 이 원칙은 요구사항을 실행 가능한 명세로 만들고 회귀를
최소화하기 위한 것이다.

### IV. 확장 가능한 모듈 아키텍처
새 기능은 각 레이어 내부에서 책임이 명확한 컴포넌트, 라우터, 서비스, 도메인
단위로 분리한다. 순환 의존성, 거대한 범용 유틸 누적, 전역 상태 남용은 금지한다.
확장이 예상되는 경우 모듈 경계와 인터페이스를 먼저 정의하되, 불필요한 추상화는
도입하지 않는다. 이 원칙은 성장 가능한 구조를 유지하면서 과설계를 피하기 위한
것이다.

### V. 제한된 브랜치와 CI 게이트
Git 브랜치는 `main`, `front-end`, `back-end`만 사용한다. Spec Kit를 포함한 어떤
자동화도 추가 feature branch를 생성하거나 요구해서는 안 된다. 모든 변경은 해당
협업 브랜치에서 lint, test, build, 문서 동기화 검사를 수행하는 CI를 통과해야 하며,
실패 상태에서 병합하거나 배포할 수 없다. 이 원칙은 협업 정책을 명확히 하고 품질
게이트를 자동화하기 위한 것이다.

## Technology & Repository Standards

- 프론트엔드 구현 및 테스트는 `frontend/` 아래에 둔다.
- 백엔드 구현 및 테스트는 `backend/` 아래에 둔다.
- 계약 문서와 팀 간 합의된 명세는 `Docs/` 아래에 저장하며, `docs/`가 함께 존재해도
  정식 기준 문서는 `Docs/`다.
- 프론트엔드 API 호출부는 `Docs/`에 정의된 계약만 신뢰해야 하며, 백엔드는 같은
  계약과 일치하는 요청, 응답, 오류 형식을 제공해야 한다.
- 새로운 공유 예제, 픽스처, 모의 payload는 각 레이어 테스트에서 재사용 가능해야
  하며, 소유자가 없는 중복 사본을 양쪽에 흩뿌리지 않는다.

## Workflow & Quality Gates

- 모든 `spec.md`, `plan.md`, `tasks.md`는 영향 범위를 `Front-end`, `Back-end`,
  `Both` 중 하나 이상으로 명시해야 한다.
- API 또는 데이터 계약 변경 작업은 반드시 `Docs/` 변경, 테스트 추가, 구현 반영을
  함께 포함해야 한다.
- 구현 계획은 프론트엔드와 백엔드가 어떻게 분리 유지되는지, CI에서 어떤 검증
  명령을 실행할지 설명해야 한다.
- 태스크는 테스트 작성과 실패 확인을 구현보다 앞에 배치해야 하며, 프론트엔드와
  백엔드 작업을 동일 파일 집합에 섞어 기록해서는 안 된다.
- 리뷰와 병합 전 검증은 브랜치 정책 준수, `Docs/` 동기화, 테스트 통과, CI 통과를
  모두 확인해야 한다.

## Governance

이 헌법은 README, Spec Kit 템플릿, git extension, 개별 작업 관행보다 우선한다.
충돌이 발생하면 이 문서를 기준으로 관련 파일을 수정해야 한다.

개정은 다음 순서로 수행한다. 첫째, 헌법 본문과 상단 Sync Impact Report를 갱신한다.
둘째, 영향받는 템플릿, 스크립트, 안내 문서를 같은 변경 세트에서 동기화한다. 셋째,
코드 리뷰에서 헌법 준수 여부를 확인한다.

버전 정책은 시맨틱 버전 규칙을 따른다. MAJOR는 핵심 원칙, 브랜치 정책, 기술 경계의
비호환 변경이다. MINOR는 원칙, 필수 섹션, 품질 게이트의 실질적 추가 또는 확장이다.
PATCH는 의미를 바꾸지 않는 명확화, 표현 정리, 오탈자 수정이다.

모든 계획 문서, 태스크 문서, 리뷰 결과는 이 헌법의 준수 여부를 명시적으로 확인해야
한다.

**Version**: 1.0.0 | **Ratified**: 2026-04-19 | **Last Amended**: 2026-04-19
