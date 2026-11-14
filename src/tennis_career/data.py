
import pandas as pd

from ._players import _normalize_player_name
from ._download import _download_text
from ._profiles import _get_player_profile
from ._parsing import _parse_matches, _combine_matches
from ._cleaning import _clean_match, _detect_tour


def get_career_matches(player_name):
	"""Retrieve and clean career matches for a Tennis Abstract player."""
	name = _normalize_player_name(player_name)
	birthdate, _ = _get_player_profile(name)
	career_url = f"https://www.tennisabstract.com/jsmatches/{name}Career.js"
	older = _parse_matches(_download_text(career_url))
	tour = _detect_tour(older)

	page = "wplayer-classic" if tour == "wta" else "player-classic"
	profile_url = f"https://www.tennisabstract.com/cgi-bin/{page}.cgi?p={name}"
	recent = _parse_matches(_download_text(profile_url), "matchmx")
	matches = _combine_matches(recent, older)

	records = [
		record for match in matches
		if (record := _clean_match(match, birthdate, tour)) is not None
	]
	if not records:
		raise ValueError(f"No usable career matches found for '{player_name}'.")
	return pd.DataFrame(records)
