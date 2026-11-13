from datetime import datetime
from pathlib import Path
from unittest.mock import patch

import matplotlib.pyplot as plt
import pandas as pd
import pytest

from tennis_career import get_career_matches, plot_career_matches


FIXTURES = Path(__file__).parent / "fixtures"


def _mock_matches(player_name, birthdate, tour, fixture):
	js_text = (FIXTURES / fixture).read_text(encoding="utf-8")
	with patch("tennis_career.data._get_player_profile", return_value=(birthdate, tour)):
		with patch("tennis_career.data._download_text", return_value=js_text):
			return get_career_matches(player_name)


@pytest.mark.parametrize("name", [
	"serena williams", "Serena Williams", "SerenaWilliams"
])
def test_player_name_variations(name):
	matches = _mock_matches(name, datetime(1981, 9, 26), "wta", "female_player.js")

	assert isinstance(matches, pd.DataFrame)
	assert len(matches) == 3
	assert {"player_age", "opponent_age", "age_diff", "result"}.issubset(matches.columns)


def test_male_career_matches():
	matches = _mock_matches(
		"Rafael Nadal", datetime(1986, 6, 3), "atp", "male_player.js"
	)

	assert len(matches) == 3
	assert matches.iloc[0]["opponent"] == "Guillermo Platel"
	assert matches.iloc[0]["opponent_age"] == pytest.approx(22.264202601)


def test_invalid_player():
	with patch("tennis_career.data._get_player_profile",
			   side_effect=ValueError("Player not found")):
		with pytest.raises(ValueError, match="Player not found"):
			get_career_matches("GastonSanchez")


def test_scatter_plot():
	matches = _mock_matches(
		"Rafael Nadal", datetime(1986, 6, 3), "atp", "male_player.js"
	)
	fig = plot_career_matches(matches)

	assert len(fig.axes) == 1
	assert fig.axes[0].get_xlabel() == "Player's age"
	assert fig.axes[0].get_ylabel() == "Player's age minus opponent's age"
	assert len(fig.axes[0].collections) == 2
	plt.close(fig)


def test_invalid_plot_data():
	with pytest.raises(ValueError, match="missing required"):
		plot_career_matches(pd.DataFrame({"player_age": [20]}))
