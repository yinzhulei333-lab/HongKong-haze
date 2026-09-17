# /// script
# requires-python = ">=3.10"
# dependencies = ["requests"]
# ///

"""
Fetch the numbers once, save the raw reply to data/, and never fetch again.

    uv run fetch.py

One year of hourly PM2.5 and PM10 for Hong Kong, from Open-Meteo's air-quality
API (no key needed). The reply is JSON, saved byte for byte to data/.
"""

from pathlib import Path

import requests

URL = ("https://air-quality-api.open-meteo.com/v1/air-quality"
       "?latitude=22.32&longitude=114.17&hourly=pm10,pm2_5"
       "&start_date=2025-09-17&end_date=2026-09-17"
       "&timezone=Asia%2FHong_Kong")
FILE = "hk-pm25-2026.json"        # one year of Hong Kong PM2.5 and PM10, hourly

HERE = Path(__file__).parent
DATA = HERE / "data"


def fetch(url, path):
    """Ask for the file once. If it is already in data/, do nothing."""
    if path.exists():
        print(f"data/{path.name} is already here ({path.stat().st_size // 1024} KB). "
              "Delete it to fetch again.")
        return path
    DATA.mkdir(exist_ok=True)
    print(f"asking {url}")
    reply = requests.get(url, timeout=60, headers={"User-Agent": "SD5913 PolyU student"})
    reply.raise_for_status()
    path.write_bytes(reply.content)      # the raw reply, byte for byte
    print(f"saved data/{path.name} ({path.stat().st_size // 1024} KB). Now: git add data")
    return path


if __name__ == "__main__":
    fetch(URL, DATA / FILE)
