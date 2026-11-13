import requests


def _download_text(url):
	try:
		response = requests.get(
			url,
			headers={
				"User-Agent": "Mozilla/5.0",
				"Referer": "https://www.tennisabstract.com/"
			},
			timeout=15
		)
		response.raise_for_status()
	except requests.RequestException as error:
		raise ValueError(
			f"Unable to download Tennis Abstract data from {url}: {error}"
		) from error

	return response.text
