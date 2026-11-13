# Tennis Career Match Visualization

STAT 159 Homework 3 | UC Berkeley

## Overview

This project builds on HW2 by turning the Serena Williams career match visualization into a reusable Python package. It retrieves career match data for different tennis players from Tennis Abstract and generates scatter plots showing player age, opponent age differences, and match results.

The package handles differences between male and female players' match data and provides two public functions for retrieving and visualizing career matches.

## Installation

Install directly from the GitHub repository:

```bash
pip install git+https://github.com/UCB-stat159-f26/hw03-danielchaolin.git
```

## Usage

The package provides two public functions:

- `get_career_matches()`: Retrieves and processes a player's career match data into a pandas DataFrame.
- `plot_career_matches()`: Generates a scatter plot of the player's age against the age difference between the player and their opponents.

```python
from tennis_career import get_career_matches, plot_career_matches

# Serena Williams
serena = get_career_matches("Serena Williams")
plot_career_matches(serena)

# Rafael Nadal
rafa = get_career_matches("Rafael Nadal")
plot_career_matches(rafa)

# Invalid player
unknown = get_career_matches("Oski Bear")
# Raises a ValueError
```

Player names can be entered with different capitalization or without spaces.

## Visualization

The scatter plot uses:

- X-axis: Player's age at the time of each match
- Y-axis: Player's age minus opponent's age
- Cyan points: Wins
- Purple points: Losses

Positive age differences indicate the player was older than their opponent, while negative values indicate they were younger.

## Repository Structure

```text
hw03-danielchaolin/
├── src/
│   └── tennis_career/
│       ├── __init__.py
│       ├── _players.py
│       ├── _download.py
│       ├── _profiles.py
│       ├── _parsing.py
│       ├── _cleaning.py
│       ├── data.py
│       └── plotting.py
├── tests/
│   ├── fixtures/
│   │   ├── female_player.js
│   │   └── male_player.js
│   ├── test_parsing.py
│   ├── test_cleaning.py
│   └── test_public.py
├── pyproject.toml
├── instructions.md
├── .gitignore
└── README.md
```

## Testing

Install pytest and run the tests:

```bash
python -m pip install pytest
python -m pytest tests/ -v
```

The tests use sample JavaScript files and mocked downloads to avoid making requests to live servers.

They cover JavaScript parsing, data cleaning, age calculations, player-name variations, invalid inputs, and plotting.

The package was also manually tested using live career data for Serena Williams and Rafael Nadal.

## Personal Reflection

This assignment helped me understand to better break down a problem into separate smaller functions that build into a reusable Python package. Unlike the previous homework and projects, where I mainly handled the coding in larger Python scripts or large notebooks, this homework guided me towards creating this more modular approach by maintaining the 20 line limit for my functions.

One difficulty I encountered in this project was accounting for the differences in how Tennis Abstract stores opponent ages for male and female players. I also encountered issues with retrieving player birthdates when the I had not identified the correct data format. Debugging these problems were simpler once I had separated my package into multiple functions as I did not have to look through a large combined file to understand what I needed to change. However, an issue I had with debugging was that I initially used automated tests to determine if I had created my functions correctly. Because these automated tests were not based on the live data drawn from Tennis Abstract, but instead the sample data format given as a fixed test, I was unable to realize that my code had issues until I attempted to run it drawing on the actual online Tennis Abstract data.

All in all, what I got from this assignment was that modular code and clear comments were efficient for debugging and that testing with real data is needed to ensure that a package works beyond controlled cases.

## Data Source

[Tennis Abstract](https://www.tennisabstract.com/)
