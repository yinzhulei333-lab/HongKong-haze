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

Four pictures before this one. A line of all 8,784 hourly values was too noisy
to read; a calendar of squares was honest but looked like a spreadsheet; a
spiral of dots scattered; a set of tree rings looked tidy but ordinary. I kept
the bars: clean days are drawn almost in the colour of the background, so what
you see is only the pollution. I also rejected pandas for a plain dictionary —
a list of lists was enough, and one less dependency.
