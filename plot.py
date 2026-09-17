# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy"]
# ///

"""
A year of Hong Kong haze as a calendar — one square per day.

    uv run plot.py

8,784 hourly PM2.5 values collapse to 366 daily means, laid out as a calendar
where each day's colour is its air. The palette is the AQI ladder (green = good,
purple = very unhealthy), so the picture reads as a health map rather than a
line graph.
"""

import json
from datetime import date, timedelta
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import BoundaryNorm, ListedColormap
from matplotlib.patches import Patch

FILE = "hk-pm25-2026.json"
PICTURE = "pm25-year.png"

HERE = Path(__file__).parent
DATA = HERE / "data" / FILE
OUT = HERE / "out"


def load(path):
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def main():
    raw = load(DATA)
    times = raw["hourly"]["time"]
    pm25 = raw["hourly"]["pm2_5"]

    # 8,784 hourly values -> 366 daily means
    by_day = {}
    for t, v in zip(times, pm25):
        if v is None:
            continue
        by_day.setdefault(t[:10], []).append(v)
    days = sorted(by_day)
    mean = {d: sum(by_day[d]) / len(by_day[d]) for d in days}
    print(f"{len(days)} days, daily mean from {min(mean.values()):.1f} "
          f"to {max(mean.values()):.1f} ug/m3")

    start = date.fromisoformat(days[0])
    end = date.fromisoformat(days[-1])
    first_monday = start - timedelta(days=start.weekday())
    n_weeks = (end - first_monday).days // 7 + 2

    # grid: row = weekday (Mon..Sun), column = week
    grid = np.full((7, n_weeks), np.nan)
    for d in days:
        day = date.fromisoformat(d)
        offset = (day - first_monday).days
        grid[offset % 7, offset // 7] = mean[d]

    # AQI-style palette for PM2.5, ug/m3
    levels = [0, 15, 35, 55, 75, 110, 250]
    colors = ["#2e7d32", "#f9a825", "#ef6c00", "#d32f2f", "#7b1fa2", "#4527a0"]
    cmap = ListedColormap(colors)
    cmap.set_bad("#ffffff")
    norm = BoundaryNorm(levels, cmap.N)

    fig, ax = plt.subplots(figsize=(14, 5.5))
    ax.pcolormesh(np.flipud(grid), cmap=cmap, norm=norm,
                  edgecolor="white", linewidth=0.9)

    # weekday labels, Monday on top
    ax.set_yticks(np.arange(7) + 0.5)
    ax.set_yticklabels(["Sun", "Sat", "Fri", "Thu", "Wed", "Tue", "Mon"])
    ax.tick_params(axis="y", length=0)
    ax.set_ylim(0, 7)

    # month labels along the top
    ticks, labels = [], []
    y, m = start.year, start.month
    while True:
        first = date(y, m, 1)
        if first > end:
            break
        col = max(0, (first - first_monday).days // 7)
        ticks.append(col + 0.5)
        labels.append(first.strftime("%b"))
        m += 1
        if m == 13:
            m, y = 1, y + 1
    ax.set_xticks(ticks)
    ax.set_xticklabels(labels)
    ax.tick_params(axis="x", length=0)
    ax.set_xlim(0, n_weeks)

    # title and subtitle
    fig.text(0.015, 0.935, "365 days of Hong Kong air",
             fontsize=17, fontweight="bold", va="top")
    fig.text(0.015, 0.865, "one square per day, coloured by daily mean PM2.5 (ug/m3)  ·  Open-Meteo  ·  22.32°N, 114.17°E",
             fontsize=10, color="#666666", va="top")

    # AQI legend along the bottom
    handles = [Patch(color=c) for c in colors]
    names = ["Good  <15", "Moderate  15-35", "Unhealthy (sensitive)  35-55",
             "Unhealthy  55-75", "Very unhealthy  75-110", "Hazardous  >110"]
    fig.legend(handles, names, loc="lower center", ncol=6,
               frameon=False, fontsize=8.5, bbox_to_anchor=(0.5, 0.01))

    fig.subplots_adjust(left=0.05, right=0.99, top=0.82, bottom=0.14)

    OUT.mkdir(exist_ok=True)
    fig.savefig(OUT / PICTURE, dpi=150, facecolor="white")
    print(f"saved out/{PICTURE}")
    plt.show()


if __name__ == "__main__":
    main()
