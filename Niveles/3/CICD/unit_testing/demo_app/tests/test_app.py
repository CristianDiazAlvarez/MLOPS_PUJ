import pytest

from app import classify_score, normalize_temperature


def test_normalize_temperature_freezing_point() -> None:
    assert normalize_temperature(0) == 32.0


def test_normalize_temperature_boiling_point() -> None:
    assert normalize_temperature(100) == 212.0


def test_classify_score_high() -> None:
    assert classify_score(0.95) == "high"


def test_classify_score_medium() -> None:
    assert classify_score(0.6) == "medium"


def test_classify_score_low() -> None:
    assert classify_score(0.2) == "low"


def test_classify_score_invalid_range() -> None:
    with pytest.raises(ValueError):
        classify_score(1.5)
