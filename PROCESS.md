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

Three pictures before this one. A line of all 8,784 hourly values was too noisy
to read. A calendar of coloured squares was honest but looked like a
spreadsheet. I kept the spiral: one dot per day, coiled through the year, with
colour and size carrying the concentration — it is a picture first, and the
season still reads. I also rejected pandas for a plain dictionary — a list of
lists was enough, and one less dependency.
