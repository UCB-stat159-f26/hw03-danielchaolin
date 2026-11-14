import re
from datetime import datetime

from ._download import _download_text


def _parse_birthdate(text):
	match = re.search(r"\bvar\s+dob\s*=\s*['\"]?(\d{8})", text)
	if not match:
		return None
	return datetime.strptime(match.group(1), "%Y%m%d")


def _get_player_profile(player_name):
	urls = [
		f"https://www.tennisabstract.com/jsmatches/{player_name}.js",
		f"https://www.tennisabstract.com/cgi-bin/player-classic.cgi?p={player_name}",
		f"https://www.tennisabstract.com/cgi-bin/wplayer-classic.cgi?p={player_name}"
	]

	for url in urls:
		try:
			birthdate = _parse_birthdate(_download_text(url))
		except ValueError:
			continue
		if birthdate:
			return birthdate, None

	raise ValueError(f"Could not find a Tennis Abstract profile for '{player_name}'.")

