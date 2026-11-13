import json
import re


def _parse_matches(js_text):
	match = re.search(r"var\s+morematchmx\s*=\s*(\[[\s\S]*?\])\s*;", js_text)

	if not match:
		raise ValueError("Could not find career match data in JavaScript.")

	try:
		matches = json.loads(match.group(1))
	except json.JSONDecodeError as error:
		raise ValueError("Career match data contains invalid JSON.") from error

	if not isinstance(matches, list):
		raise ValueError("Career match data must be a list.")

	return matches
