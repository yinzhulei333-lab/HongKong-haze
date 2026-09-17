# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy"]
# ///

"""
A year of Hong Kong haze, coiled into a spiral.

    uv run plot.py

8,784 hourly PM2.5 values collapse to 366 daily means. Each day is one dot on a
spiral that starts in September and winds outward through a full year; the dot's
colour runs from green (clean) to purple (heavy) and its size grows with the
concentration. The result is a data picture, not a chart: winter flares red and
violet near the outer turns, summer cools back to green.
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

    # hourly -> daily mean
    by_day = {}
    for t, v in zip(times, pm25):
        if v is None:
            continue
        by_day.setdefault(t[:10], []).append(v)
    days = sorted(by_day)
    values = np.array([sum(by_day[d]) / len(by_day[d]) for d in days])
    print(f"{len(days)} days, daily mean from {values.min():.1f} to {values.max():.1f} ug/m3")

    n = len(days)
    idx = np.arange(n)
    theta = 2 * np.pi * idx / 30.44          # ~12 turns across the year
    r = 0.55 + 0.85 * idx / (n - 1)          # oldest day at the centre

    # green (clean) -> yellow -> orange -> red -> violet (heavy)
    stops = ["#0f2e1a", "#2e7d32", "#9ccc65", "#fdd835",
             "#fb8c00", "#e53935", "#8e24aa", "#2a0a3d"]
    cmap = LinearSegmentedColormap.from_list("haze", stops)

    fig = plt.figure(figsize=(11, 11), facecolor="#0b0b11")
    ax = fig.add_subplot(111, projection="polar")
    ax.set_facecolor("#0b0b11")

    sizes = 5 + values * 1.9
    # a soft halo under every dot; the heavy days flare through it
    ax.scatter(theta, r, c=values, cmap=cmap, s=sizes * 6,
               vmin=0, vmax=75, alpha=0.16, linewidths=0)
    ax.scatter(theta, r, c=values, cmap=cmap, s=sizes, vmin=0, vmax=75,
               alpha=0.95, linewidths=0)

    ax.set_ylim(0, 1.52)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.grid(False)
    ax.spines["polar"].set_visible(False)

    fig.text(0.5, 0.955, "a year of Hong Kong air", fontsize=21,
             fontweight="bold", color="#f5f5f2", ha="center", va="top")
    fig.text(0.5, 0.905, "one dot per day, coiled from September to September  ·  colour and size = daily PM2.5",
             fontsize=10, color="#8a8a93", ha="center", va="top")

    # a thin colour key under the title
    key_ax = fig.add_axes([0.36, 0.055, 0.28, 0.016])
    grad = np.linspace(0, 1, 256).reshape(1, -1)
    key_ax.imshow(grad, aspect="auto", cmap=cmap)
    key_ax.set_xticks([])
    key_ax.set_yticks([])
    for s in key_ax.spines.values():
        s.set_visible(False)
    fig.text(0.35, 0.04, "clean", color="#8a8a93", fontsize=9, ha="left", va="center")
    fig.text(0.65, 0.04, "heavy  (µg/m³)", color="#8a8a93", fontsize=9, ha="left", va="center")

    OUT.mkdir(exist_ok=True)
    fig.savefig(OUT / PICTURE, dpi=150, facecolor="#0b0b11")
    print(f"saved out/{PICTURE}")
    plt.show()


if __name__ == "__main__":
    main()
