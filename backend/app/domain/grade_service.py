from dataclasses import dataclass
from random import Random
from typing import Dict, List, Tuple

from .models import StatBreakdown


GRADE_BANDS: List[Tuple[float, str]] = [
    (4.3, "A+"),
    (4.0, "A0"),
    (3.5, "B+"),
    (3.0, "B0"),
    (2.5, "C+"),
    (2.0, "C0"),
    (1.5, "D+"),
    (1.0, "D0"),
]

TITLE_POOL = {
    "focus": ("집중보정러", "연구러", "꾸준함 마스터"),
    "diligence": ("성실러", "공부벌레", "루틴러"),
    "execution": ("실행형", "마감돌파", "집중실행"),
    "cramming": ("고득점 마무리", "단기돌파", "밤샘달인"),
    "luck": ("운좋은 날", "반짝카드", "행운러"),
}

COMMENT_POOL: Dict[str, List[str]] = {
    "focus": [
        "집중도가 높을수록 커피 한 잔이 더 잘 맞아요.",
        "지금은 몰입력 연습기로서 아주 안정적인 점수군요.",
    ],
    "diligence": [
        "꾸준함이 성적의 기본입니다. 재미 점수에서는 꽤 잘 버텨요.",
        "꾸준함은 이미 보유중. 과몰입 조절만 조금 더.",
    ],
    "execution": [
        "실행 속도가 좋으면 결과는 금방 오더라도 금방 사라져요.",
        "실행력은 충분, 다음은 회복력만 올리면 완성입니다.",
    ],
    "cramming": [
        "짧은 기간 몰입도는 장점이지만, 장기 유지가 과제입니다.",
        "압축 학습 모드가 강점이라 스코어가 반짝올랐네요.",
    ],
    "luck": [
        "운영이 잘 맞을수록 결과 화면도 잘 나옵니다.",
        "운이 따른 날이군요. 변수가 강한 항목입니다.",
    ],
}


def grade_from_score(score: float) -> str:
    for threshold, grade in GRADE_BANDS:
        if score >= threshold:
            return grade
    return "F"


def seed_to_stats(seed: int) -> StatBreakdown:
    rng = Random(seed)
    values = [rng.randint(20, 100) for _ in range(5)]
    return StatBreakdown(*values)


def pick_titles(seed: int) -> List[str]:
    rng = Random(seed + 1)
    title_keys = list(TITLE_POOL.keys())
    primary = rng.choice(title_keys)
    secondary = rng.sample(title_keys, 2)
    titles = [TITLE_POOL[primary][0]] + [TITLE_POOL[key][0] for key in secondary]
    # Preserve at least 2 and at most 3
    return list(dict.fromkeys(titles))[:3]


def pick_comment(primary_title: str, seed: int) -> str:
    key = next((k for k, values in TITLE_POOL.items() if values[0] == primary_title), "luck")
    comments = COMMENT_POOL.get(key, COMMENT_POOL["luck"])
    return comments[seed % len(comments)]


@dataclass(frozen=True)
class GradeResult:
    score: float
    grade: str
    titles: List[str]
    comment: str
    stats: StatBreakdown


def build_result(seed: int) -> GradeResult:
    score = round((seed % 451) / 100, 1)
    grade = grade_from_score(score)
    titles = pick_titles(seed)
    primary_title = titles[0]
    comment = pick_comment(primary_title, seed)
    stats = seed_to_stats(seed)
    return GradeResult(score=score, grade=grade, titles=titles, comment=comment, stats=stats)
