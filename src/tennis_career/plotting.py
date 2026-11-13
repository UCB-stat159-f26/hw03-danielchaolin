
import matplotlib.pyplot as plt


def plot_career_matches(matches):
	"""Plot player age against opponent age difference."""
	required = {"player_age", "age_diff", "result"}
	if not required.issubset(matches.columns):
		raise ValueError("DataFrame is missing required plot columns.")

	fig, ax = plt.subplots(figsize=(11, 7))

	for result, color, label in [("W", "#19b4cf", "Wins"), ("L", "#8053a6", "Losses")]:
		subset = matches[matches["result"] == result]
		ax.scatter(subset["player_age"], subset["age_diff"],
				   c=color, s=18, alpha=0.7, label=label)

	ax.axhline(0, color="gray", linewidth=0.8)
	ax.set_xlabel("Player's age")
	ax.set_ylabel("Player's age minus opponent's age")
	ax.set_title("Career Matches by Age Difference")
	ax.legend()
	fig.tight_layout()

	return fig
