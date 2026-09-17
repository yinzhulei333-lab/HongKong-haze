# Process

## Tools

Python with uv, the requests and matplotlib libraries, and the Open-Meteo air
quality API. I wrote the code with the help of an AI assistant (WorkBuddy) that
started from the course template, and I checked each change it made before
running it.

## Kept

The raw JSON exactly as Open-Meteo sent it, byte for byte, committed under
`data/`. Keeping the file untouched means the plot can be redrawn with no
internet and the numbers stay auditable.

## Rejected

Drawing all 8,784 hourly values as one line. That line is so noisy it hides the
season. I rejected it and averaged each day to a single mean, then drew the WHO
guideline underneath so the comparison is visible. I also rejected pandas for a
plain dictionary — a list of lists was enough, and one less dependency.
