import re


def _normalize_player_name(name):
	if not isinstance(name, str) or not name.strip():
		raise ValueError("Player name must be a nonempty string.")

	name = re.sub(r"([a-z])([A-Z])", r"\1 \2", name.strip())
	parts = name.split()

	if not all(part.isalpha() for part in parts):
		raise ValueError("Player name must contain only letters and spaces.")

	return "".join(part.capitalize() for part in parts)
