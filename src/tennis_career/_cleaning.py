from datetime import datetime


def _detect_tour(matches):
	for match in matches:
		if len(match) <= 16 or not match[16]:
			continue
		value = str(match[16])
		if len(value) == 8 and value.isdigit():
			return "wta"
		try:
			float(value)
			return "atp"
		except ValueError:
			continue
	raise ValueError("Could not determine player tour from match data.")


def _calculate_age(birthdate, match_date):
	return (match_date - birthdate).days / 365.25


def _get_opponent_age(value, match_date, tour):
	if tour == "wta":
		birthdate = datetime.strptime(value, "%Y%m%d")
		return _calculate_age(birthdate, match_date)
	if tour == "atp":
		return float(value)
	raise ValueError("Unknown player tour.")


def _clean_match(match, player_birthdate, tour):
	try:
		match_date = datetime.strptime(match[0], "%Y%m%d")
		player_age = _calculate_age(player_birthdate, match_date)
		opponent_age = _get_opponent_age(match[16], match_date, tour)
		result = match[4]

		if player_age < 0 or opponent_age < 0 or result not in ("W", "L"):
			return None

		return {
			"date": match_date,
			"opponent": match[11],
			"player_age": player_age,
			"opponent_age": opponent_age,
			"age_diff": player_age - opponent_age,
			"result": result
		}
	except (ValueError, TypeError, IndexError):
		return None
