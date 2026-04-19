# 얼굴 성적기 MVP 스펙 문서

## 1. 개요

### 서비스명

- 얼굴 성적기
- FaceGrade

### 목적

사용자가 이름과 얼굴 사진을 등록하면, 얼굴 랜드마크 기반의 룰 엔진으로 `0.0 ~ 4.5` 범위의 재미용 성적 결과를 생성하는 엔터테인먼트 서비스다.

### 플랫폼

- 모바일 기준 웹 서비스

### 핵심 원칙

- 실제 학업 능력, 성실성, 지능, 성격을 평가하지 않는다.
- 결과는 연출형 결과이며 얼굴 비율 특징과 랜덤 요소를 함께 사용한다.
- 내부 기준 이미지 1장을 `0.0 / 4.5`의 고정 기준점으로 사용한다.
- 얼굴 데이터는 기본적으로 영구 저장하지 않는 방향으로 설계한다.

## 2. MVP 범위

### 포함

- 이름 입력
- 얼굴 사진 업로드
- 얼굴 검출 및 랜드마크 추출
- 룰 기반 점수 계산
- 결과 화면 표시
- 결과 이미지 다운로드
- 인스타그램 스토리 공유

### 제외

- 로그인
- DB 저장
- 랭킹
- 친구 비교
- 데스크톱 전용 최적화

## 3. 사용자 플로우

1. 사용자가 메인 화면에서 이름을 입력한다.
2. 얼굴 사진을 업로드한다.
3. `성적 조회 시작` 버튼을 누른다.
4. 서버가 얼굴 검출, 랜드마크 추출, feature 계산, 점수 환산을 수행한다.
5. 결과 화면에 사진, 점수, 등급, 코멘트, 칭호를 표시한다.
6. 사용자는 `다운로드` 또는 `인스타그램 스토리 공유`를 선택하고 흐름을 종료한다.

## 4. 화면 명세

### 4.1 메인 화면

표시 요소:

- 서비스 타이틀
- 이름 입력 필드
- 얼굴 사진 업로드 영역
- `성적 조회 시작` 버튼
- 안내 문구: `본 서비스는 재미용입니다. 실제 능력/성적과 무관합니다.`

동작 규칙:

- 이름과 사진이 모두 있어야 버튼이 활성화된다.
- 업로드 가능 형식은 `jpg`, `jpeg`, `png`다.
- 단일 얼굴만 허용한다.
- 업로드 즉시 사진 미리보기를 제공한다.

### 4.2 결과 화면

표시 요소:

- 업로드한 사진
- 이름
- 성적 점수: 예시 `3.7 / 4.5`
- 등급: 예시 `A0`
- 한줄 코멘트
- 세부 스탯 바 차트
- 칭호 2~3개
- `다운로드` 버튼
- `인스타그램 스토리 공유` 버튼

동작 규칙:

- `다운로드`는 현재 결과 화면을 저장 가능한 결과 이미지로 내려받게 한다.
- `인스타그램 스토리 공유`는 결과 이미지를 스토리 공유 흐름에 전달한다.
- 모바일 기준 웹 화면에서 주요 정보와 행동 버튼이 한 화면 흐름 안에서 읽히도록 구성한다.

### 4.3 예외 화면

오류 메시지 예시:

- 얼굴을 찾을 수 없습니다.
- 얼굴이 2개 이상 감지되었습니다.
- 지원하지 않는 파일 형식입니다.
- 파일 크기가 너무 큽니다.
- 분석 중 오류가 발생했습니다.

## 5. 기능 요구사항

### 5.1 입력

입력값:

- `name`: 사용자 이름, 결과 화면 표시용
- `file`: 얼굴 이미지 파일

제약 조건:

- 최대 파일 크기: 10MB
- 단일 이미지 업로드만 허용
- 정면 또는 준정면 얼굴 권장

### 5.2 처리 파이프라인

1. 얼굴 검출
2. 얼굴 crop
3. MediaPipe Face Mesh 랜드마크 추출
4. feature engineering
5. 중간 스탯 계산
6. 보너스/칭호 계산
7. 최종 raw score 계산
8. `0.0 ~ 4.5` 점수로 환산
9. 등급 구간 변환
10. 코멘트 생성
11. 결과 JSON 반환

## 6. 점수 산정 규칙

### 6.1 기준 이미지 정책

- 운영자가 지정한 기준 얼굴 이미지를 `reference_baseline`으로 등록한다.
- 이 이미지의 raw score를 `baseline_raw`로 저장한다.
- 최종 점수 환산 시 `baseline_raw`는 항상 `0.0`의 기준점이 된다.
- 기준 이미지보다 낮은 점수는 모두 `0.0`으로 클램프한다.

### 6.2 랜드마크 추출

사용 라이브러리:

- MediaPipe Face Mesh

출력:

- 얼굴 랜드마크 468개 좌표 `(x, y, z)`

### 6.3 Feature 목록

| feature | 설명 | 계산 방식 |
| --- | --- | --- |
| `eye_size` | 눈 크기 | 눈 랜드마크 거리 / 얼굴 폭 |
| `eye_distance` | 눈 사이 거리 | 두 눈 중심 거리 / 얼굴 폭 |
| `eyebrow_angle` | 눈썹 기울기 | 눈썹 라인 각도 |
| `mouth_curve` | 입꼬리 각도 | 입꼬리 상승/하강 각도 |
| `face_ratio` | 얼굴 비율 | 얼굴 높이 / 얼굴 너비 |
| `symmetry` | 좌우 대칭성 | 좌우 landmark 차이 평균 |
| `forehead_ratio` | 이마 비율 | 이마 높이 / 얼굴 높이 |
| `jaw_angle` | 턱선 각도 | 턱 라인 기울기 |

정규화 식:

```python
value = (value - min_value) / (max_value - min_value)
value = clamp(value, 0.0, 1.0)
```

### 6.4 중간 스탯 계산

정의:

- `focus`: 집중력
- `diligence`: 성실성
- `execution`: 실행력
- `cramming`: 벼락치기력
- `luck`: 시험운

계산식:

```python
focus = (
    symmetry * 30 +
    eye_size * 25 +
    eyebrow_angle * 20 +
    (1 - eye_distance) * 15 +
    forehead_ratio * 10
)

diligence = (
    forehead_ratio * 30 +
    jaw_angle * 25 +
    symmetry * 20 +
    (1 - mouth_curve) * 15 +
    (1 - eye_size) * 10
)

execution = (
    jaw_angle * 35 +
    eyebrow_angle * 25 +
    symmetry * 20 +
    (1 - eye_distance) * 20
)

cramming = (
    mouth_curve * 30 +
    eye_size * 15 +
    (1 - jaw_angle) * 20 +
    random.uniform(0, 20)
)

luck = (
    symmetry * 20 +
    mouth_curve * 20 +
    random.uniform(0, 60)
)
```

### 6.5 보너스 룰 및 칭호

```python
bonus = 0
titles = []

if symmetry > 0.75 and forehead_ratio > 0.65:
    bonus += 8
    titles.append("모범생 상")

if mouth_curve > 0.6 and eye_size > 0.6:
    bonus += 6
    titles.append("벼락치기 생존형")

if eyebrow_angle > 0.7 and jaw_angle > 0.6:
    bonus += 7
    titles.append("독기 풀충전형")
```

추가 칭호 규칙:

- 최고 스탯이 `focus`면 `집중력 우수형`
- 최고 스탯이 `diligence`면 `꾸준함 특화형`
- 최고 스탯이 `execution`면 `실전 돌파형`
- 최고 스탯이 `cramming`면 `막판 스퍼트형`
- 최고 스탯이 `luck`면 `시험운 강한 상`

### 6.6 최종 raw score

```python
raw_score = (
    focus * 0.3 +
    diligence * 0.3 +
    execution * 0.15 +
    cramming * 0.1 +
    luck * 0.15 +
    bonus
)

raw_score = clamp(raw_score, 0, 100)
```

### 6.7 0.0 ~ 4.5 환산

초기 MVP 환산식:

```python
final_score = ((raw_score - baseline_raw) / (100 - baseline_raw)) * 4.5
final_score = clamp(final_score, 0.0, 4.5)
final_score = round(final_score, 1)
```

운영 튜닝 시 권장식:

```python
final_score = ((raw_score - baseline_raw) / (tuned_max_raw - baseline_raw)) * 4.5
```

정의:

- `baseline_raw`: 기준 이미지의 raw score
- `tuned_max_raw`: 밸런싱 이후 최고점 기준값

### 6.8 등급 변환

```python
if final_score >= 4.3:
    grade = "A+"
elif final_score >= 4.0:
    grade = "A0"
elif final_score >= 3.5:
    grade = "B+"
elif final_score >= 3.0:
    grade = "B0"
elif final_score >= 2.5:
    grade = "C+"
elif final_score >= 2.0:
    grade = "C0"
elif final_score >= 1.5:
    grade = "D+"
elif final_score >= 1.0:
    grade = "D0"
else:
    grade = "F"
```

등급 집합:

- `A+`
- `A0`
- `B+`
- `B0`
- `C+`
- `C0`
- `D+`
- `D0`
- `F`

### 6.9 코멘트 생성

코멘트는 최종 점수와 상위 스탯 조합으로 생성한다.

예시:

- `focus + diligence` 우세: `계획형 모범생 스타일`
- `execution + luck` 우세: `실전에서 강한 한방형`
- `cramming + luck` 우세: `벼락치기 생존 확률 높은 타입`
- `diligence` 우세 + `mouth_curve` 낮음: `묵묵하게 쌓아가는 안정형`

## 7. API 명세

### POST `/analyze`

요청:

- `Content-Type: multipart/form-data`

폼 필드:

- `name`: string
- `file`: image file

응답 예시:

```json
{
  "name": "홍길동",
  "score": 3.7,
  "maxScore": 4.5,
  "grade": "B+",
  "stats": {
    "focus": 72.1,
    "diligence": 80.4,
    "execution": 68.2,
    "cramming": 55.0,
    "luck": 82.3
  },
  "titles": ["모범생 상", "시험운 강한 상"],
  "comment": "평소 꾸준함이 강하고 실전 운도 따라주는 안정형",
  "imageUrl": "/temp/result/abc123.jpg"
}
```

오류 응답:

- `400`: 파일 누락, 형식 오류
- `422`: 얼굴 미검출, 복수 얼굴 감지
- `500`: 내부 분석 오류

## 8. 시스템 아키텍처

### Backend

- Python
- FastAPI
- 이미지 validation
- MediaPipe 분석
- 점수 계산 엔진
- JSON 응답 생성

### Frontend

- React 또는 Next.js
- 모바일 퍼스트 웹 UI
- 업로드 화면
- 결과 화면
- 다운로드 및 인스타그램 스토리 공유 행동
- 로딩/에러 처리

### 비전/연산

- MediaPipe
- OpenCV
- NumPy

처리 흐름:

```text
Client
  -> Image Upload
  -> Face Detection
  -> Landmark Extraction
  -> Feature Calculation
  -> Score Engine
  -> Result Generator
  -> JSON Response
```

## 9. 정책 및 제한사항

반드시 표시할 문구:

- 본 서비스는 재미용입니다.
- 실제 능력, 성적, 성격과 무관합니다.
- 얼굴 데이터 저장 여부를 명확히 고지합니다.

운영 원칙:

- 업로드 이미지는 기본적으로 영구 저장하지 않는다.
- 이름은 결과 표시 용도로만 사용하고 점수 계산에는 사용하지 않는다.
- 실제 평가, 선발, 진단 용도로 사용하지 못하도록 명시한다.

## 10. 밸런싱 전략

목표 분포:

- A 계열: 20%
- B 계열: 35%
- C 계열: 30%
- D 계열: 10%
- F: 5%

튜닝 항목:

- `baseline_raw`
- `tuned_max_raw`
- `bonus` 가중치
- `luck`, `cramming` 랜덤 폭

검증 방식:

- 테스트 이미지 다건 분석
- score histogram 확인
- 등급 분포 확인
- 특정 얼굴형에 과도하게 편향되는지 확인

## 11. 개발 우선순위

1. 이미지 업로드 및 입력 검증
2. MediaPipe 얼굴 검출 및 랜드마크 추출
3. feature 계산 함수 구현
4. 점수 엔진 및 결과 생성기 구현
5. FastAPI `/analyze` API 연결
6. 메인 화면 및 결과 화면 구현
7. 예외 처리 및 밸런싱

## 12. MVP 완료 기준

- 메인 화면에서 이름과 사진을 입력할 수 있다.
- 얼굴 1개가 정상 검출되면 결과가 반환된다.
- 결과 화면에 사진, 점수, 등급, 코멘트, 칭호가 표시된다.
- 결과 이미지 다운로드가 동작한다.
- 인스타그램 스토리 공유 흐름이 동작한다.
- 오류 상황에서 적절한 메시지가 노출된다.
- 기준 이미지가 `0.0 / 4.5` 기준점으로 정상 동작한다.
- 모바일 기준 웹 화면에서 주요 흐름이 가로 스크롤 없이 동작한다.
