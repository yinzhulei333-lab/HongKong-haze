# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy"]
# ///

"""
A year of haze as a poster — one glowing bar per day.

    uv run plot.py

8,784 hourly PM2.5 values collapse to 366 daily means, drawn as 366 vertical
bars. Clean days barely show, their bars nearly the colour of the night; dirty
days glow orange and magenta. The result is meant to look like a poster: the
skyline of a city lit through its own haze.
"""

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

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

    by_day = {}
    for t, v in zip(times, pm25):
        if v is None:
            continue
        by_day.setdefault(t[:10], []).append(v)
    days = sorted(by_day)
    values = np.array([sum(by_day[d]) / len(by_day[d]) for d in days])
    print(f"{len(days)} days, daily mean from {values.min():.1f} to {values.max():.1f} ug/m3")

    stops = ["#17161e", "#3a2f3a", "#7a4030", "#c0652a", "#e0452a", "#c02a80"]
    cmap = LinearSegmentedColormap.from_list("haze", stops)
    vmax = 75.0
    bg = "#0e0d12"

    fig = plt.figure(figsize=(14, 7.6), facecolor=bg)
    ax = fig.add_axes([0.055, 0.14, 0.89, 0.58])
    ax.set_facecolor(bg)

    x = np.arange(len(values))
    c = cmap(np.clip(values / vmax, 0, 1))

    ax.bar(x, values, width=3.2, color=c, alpha=0.12, linewidth=0)   # halo
    ax.bar(x, values, width=1.0, color=c, alpha=0.9, linewidth=0)    # core

    ax.axhline(0, color="#2a2833", linewidth=0.8)

    ax.set_xlim(-6, len(values) + 6)
    ax.set_ylim(0, vmax + 12)
    ax.axis("off")

    fig.text(0.055, 0.88, "A YEAR OF HAZE", fontsize=44, fontweight="bold",
             color="#f2efe6", va="top")
    fig.text(0.055, 0.795, "one bar per day · Hong Kong daily PM2.5 · the taller and hotter, the dirtier",
             fontsize=12, color="#8a8790", va="top")
    fig.text(0.945, 0.055, "data · Open-Meteo · 22.32°N 114.17°E · 2025–2026",
             fontsize=9, color="#5a5761", va="bottom", ha="right")

    OUT.mkdir(exist_ok=True)
    fig.savefig(OUT / PICTURE, dpi=150, facecolor=bg)
    print(f"saved out/{PICTURE}")
    plt.show()


if __name__ == "__main__":
    main()
