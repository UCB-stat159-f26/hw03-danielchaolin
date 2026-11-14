import json
import re


def _parse_matches(js_text, variable="morematchmx"):
	pattern = rf"\bvar\s+{re.escape(variable)}\s*=\s*(\[[\s\S]*?\])\s*;"
	match = re.search(pattern, js_text)

	if not match:
		if variable == "matchmx":
			return []
		raise ValueError("Could not find career match data in JavaScript.")

	try:
		matches = json.loads(match.group(1))
	except json.JSONDecodeError as error:
		raise ValueError("Career match data contains invalid JSON.") from error

	if not isinstance(matches, list):
		raise ValueError("Career match data must be a list.")

	return matches


def _combine_matches(recent, older):
	seen = set()
	combined = []

	for match in recent + older:
		key = tuple(match[i] if len(match) > i else "" for i in (0, 1, 4, 8, 9, 11))
		if key not in seen:
			seen.add(key)
			combined.append(match)

	return combined
