# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib"]
# ///

"""
Read the JSON in data/, make one picture, save it to out/.

    uv run plot.py

8784 hourly PM2.5 values become 366 daily means, drawn as one line. The dashed
line is the WHO 24-hour guideline (15 µg/m³), so the picture shows not just the
numbers but how much of the year the air is above it.
"""

import json
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt

FILE = "hk-pm25-2026.json"     # the same name as in fetch.py
PICTURE = "pm25-year.png"      # what goes into out/, and into the README

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
    print(f"{DATA.name}: {len(times)} hourly values")
    print(f"first: {times[0]}  PM2.5 = {pm25[0]}")
    print(f"last:  {times[-1]}  PM2.5 = {pm25[-1]}")

    # one number per hour becomes one number per day (the mean)
    by_day = {}
    for t, v in zip(times, pm25):
        if v is None:                 # missing values
            continue
        by_day.setdefault(t[:10], []).append(v)

    days = sorted(by_day)
    xs = [datetime.strptime(d, "%Y-%m-%d") for d in days]
    ys = [sum(by_day[d]) / len(by_day[d]) for d in days]
    print(f"{len(days)} days, daily mean from {min(ys):.1f} to {max(ys):.1f}")

    fig, ax = plt.subplots(figsize=(11, 4))
    ax.plot(xs, ys, color="#d6591d", linewidth=1.0)
    ax.axhline(15, color="#1d9e75", linestyle="--", linewidth=1.2)
    ax.text(xs[0], 16, "WHO 24-hour guideline: 15 µg/m³",
            color="#0f6e56", fontsize=9)
    ax.set_xlabel("date")
    ax.set_ylabel("daily mean PM2.5 (µg/m³)")
    ax.set_title("Hong Kong PM2.5, one year (Open-Meteo)")
    fig.tight_layout()

    OUT.mkdir(exist_ok=True)
    fig.savefig(OUT / PICTURE, dpi=150)
    print(f"saved out/{PICTURE}")
    plt.show()


if __name__ == "__main__":
    main()
