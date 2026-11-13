import re
from datetime import datetime
from html import unescape

from ._download import _download_text


def _parse_birthdate(html):
	text = re.sub(r"<[^>]+>", " ", html)
	text = " ".join(unescape(text).split())
	match = re.search(r"Age:\s*\d+\s*\((\d{2}-[A-Za-z]{3}-\d{4})\)", text)

	if not match:
		return None

	return datetime.strptime(match.group(1), "%d-%b-%Y")


def _get_player_profile(player_name):
	for tour, page in (("wta", "wplayer-classic"), ("atp", "player-classic")):
		url = f"https://www.tennisabstract.com/cgi-bin/{page}.cgi?p={player_name}"

		try:
			birthdate = _parse_birthdate(_download_text(url))
		except ValueError:
			continue

		if birthdate:
			return birthdate, tour

	raise ValueError(f"Could not find a Tennis Abstract profile for '{player_name}'.")
