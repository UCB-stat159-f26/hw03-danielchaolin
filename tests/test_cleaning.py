from datetime import datetime
from pathlib import Path

import pytest

from tennis_career._cleaning import _clean_match
from tennis_career._parsing import _parse_matches


FIXTURES = Path(__file__).parent / "fixtures"


def _load_matches(filename):
	js_text = (FIXTURES / filename).read_text(encoding="utf-8")
	return _parse_matches(js_text)


def test_female_opponent_age():
	match = _load_matches("female_player.js")[0]
	record = _clean_match(match, datetime(1981, 9, 26), "wta")

	assert record["opponent"] == "Anne Miller"
	assert record["result"] == "L"
	assert record["player_age"] == pytest.approx(14.09, abs=0.02)
	assert record["opponent_age"] == pytest.approx(18.78, abs=0.02)
	assert record["age_diff"] < 0


def test_male_opponent_age():
	match = _load_matches("male_player.js")[0]
	record = _clean_match(match, datetime(1986, 6, 3), "atp")

	assert record["opponent"] == "Guillermo Platel"
	assert record["result"] == "L"
	assert record["opponent_age"] == pytest.approx(22.264202601)
	assert record["age_diff"] < 0


def test_missing_opponent_age():
	match = _load_matches("female_player.js")[0].copy()
	match[16] = ""

	assert _clean_match(match, datetime(1981, 9, 26), "wta") is None


def test_invalid_result():
	match = _load_matches("male_player.js")[0].copy()
	match[4] = "X"

	assert _clean_match(match, datetime(1986, 6, 3), "atp") is None
