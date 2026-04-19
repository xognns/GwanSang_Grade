# Quickstart: 얼굴 성적기 MVP

## Prerequisites

- Node.js 20+
- npm 10+
- Python 3.12
- `frontend/`와 `backend/` 디렉터리가 이 plan 기준으로 생성되어 있어야 함

## 1. Install dependencies

### Front-end

```bash
cd frontend
npm install
```

### Back-end

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
```

## 2. Run the services

### Back-end API

```bash
cd backend
source .venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Front-end web app

```bash
cd frontend
npm run dev -- --host 0.0.0.0 --port 5173
```

## 3. Execute tests

### Front-end unit/integration

```bash
cd frontend
npm run test
```

### Front-end mobile viewport smoke

```bash
cd frontend
npm run test:e2e
```

### Back-end unit/integration/contract

```bash
cd backend
source .venv/bin/activate
pytest
```

## 4. Manual validation checklist

1. 모바일 뷰포트에서 이름 입력과 이미지 업로드가 한 화면 흐름 안에서 동작해야 한다.
2. 단일 얼굴 이미지 제출 시 점수, 9단계 등급, 칭호, 코멘트가 표시되어야 한다.
3. 잘못된 입력은 사용자 이해 가능한 오류 메시지로 표시되어야 한다.
4. 다운로드 버튼은 결과 카드를 PNG로 저장해야 한다.
5. 모바일 브라우저에서 Web Share API가 가능하면 공유 시트가 열리고, 불가하면 다운로드 fallback이 유지되어야 한다.

## 5. CI commands to codify

- `cd frontend && npm run lint && npm run test && npm run build`
- `cd frontend && npm run test:e2e`
- `cd backend && source .venv/bin/activate && pytest`
- Contract sync check between `specs/001-face-grade-mvp/contracts/` and promoted `Docs/` contract files
