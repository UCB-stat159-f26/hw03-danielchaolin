
import pandas as pd

from ._players import _normalize_player_name
from ._download import _download_text
from ._profiles import _get_player_profile
from ._parsing import _parse_matches, _combine_matches
from ._cleaning import _clean_match, _detect_tour


def _get_profile_matches(name):
	url = f"https://www.tennisabstract.com/cgi-bin/player-classic.cgi?p={name}"
	try:
		html = _download_text(url)
		return _parse_matches(html, "matchmx")
	except ValueError:
		return []


def get_career_matches(player_name):
	"""Retrieve and clean career matches for a Tennis Abstract player."""
	name = _normalize_player_name(player_name)
	birthdate, _ = _get_player_profile(name)
	base = "https://www.tennisabstract.com/jsmatches/"
	older = _parse_matches(_download_text(f"{base}{name}Career.js"))
	recent = _parse_matches(_download_text(f"{base}{name}.js"), "matchmx")
	tour = _detect_tour(older)
	profile = _get_profile_matches(name) if tour == "atp" else []
	matches = _combine_matches(profile, _combine_matches(recent, older))

	records = [
		record for match in matches
		if (record := _clean_match(match, birthdate, tour)) is not None
	]
	if not records:
		raise ValueError(f"No usable career matches found for '{player_name}'.")
	return pd.DataFrame(records).drop_duplicates().reset_index(drop=True)

