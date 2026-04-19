from backend.app.domain.grade_service import build_result, grade_from_score


def test_grade_thresholds_match_spec():
    assert grade_from_score(4.5) == "A+"
    assert grade_from_score(4.2) == "A0"
    assert grade_from_score(3.7) == "B+"
    assert grade_from_score(3.2) == "B0"
    assert grade_from_score(2.7) == "C+"
    assert grade_from_score(2.2) == "C0"
    assert grade_from_score(1.6) == "D+"
    assert grade_from_score(1.2) == "D0"
    assert grade_from_score(0.9) == "F"


def test_build_result_is_deterministic():
    left = build_result(123456)
    right = build_result(123456)
    assert left == right
