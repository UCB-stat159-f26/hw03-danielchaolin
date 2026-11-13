from pathlib import Path

import pytest

from tennis_career._parsing import _parse_matches


FIXTURES = Path(__file__).parent / "fixtures"


@pytest.mark.parametrize("filename", ["female_player.js", "male_player.js"])
def test_parse_match_data(filename):
	js_text = (FIXTURES / filename).read_text(encoding="utf-8")
	matches = _parse_matches(js_text)

	assert len(matches) == 3
	assert all(isinstance(match, list) for match in matches)


def test_missing_match_array():
	with pytest.raises(ValueError, match="Could not find"):
		_parse_matches("var something_else = [];")


def test_malformed_match_array():
	with pytest.raises(ValueError):
		_parse_matches('var morematchmx = ["incomplete", ];')
