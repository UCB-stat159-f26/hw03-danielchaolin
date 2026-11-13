import re
from datetime import datetime

from ._download import _download_text


def _parse_birthdate(text):
	match = re.search(r"\bvar\s+dob\s*=\s*['\"]?(\d{8})", text)
	if not match:
		return None
	return datetime.strptime(match.group(1), "%Y%m%d")


def _get_player_profile(player_name):
	for tour, page in (("wta", "wplayer-classic"), ("atp", "player-classic")):
		url = f"https://www.tennisabstract.com/cgi-bin/{page}.cgi?p={player_name}"
		try:
			html = _download_text(url)
		except ValueError:
			continue

		birthdate = _parse_birthdate(html)
		script = f"/jsmatches/{player_name}.js"
		if not birthdate and script in html:
			js_url = f"https://www.tennisabstract.com/jsmatches/{player_name}.js"
			birthdate = _parse_birthdate(_download_text(js_url))

		if birthdate:
			return birthdate, tour

	raise ValueError(f"Could not find a Tennis Abstract profile for '{player_name}'.")
