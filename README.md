# Hong Kong haze

![Hong Kong daily mean PM2.5, one year](out/pm25-year.png)

## The phenomenon

Haze in Hong Kong, measured as PM2.5 — fine particles small enough to reach the
lungs. It rises in winter and falls in summer, and I wanted to see that swing
with one year of numbers rather than one grey afternoon.

## The source

One year of hourly PM2.5 and PM10 for Hong Kong (22.32 N, 114.17 E), from the
Open-Meteo air quality API — no key needed. The raw reply is 8,784 hourly rows
of JSON, committed unchanged to `data/hk-pm25-2026.json`. Each value is a
concentration in µg/m³, estimated by a weather model.

## What the picture shows

Each square is one day, laid out as a calendar, and its colour is that day's
mean PM2.5 on the AQI ladder. The year is dominated by yellow and orange — most
days sit at "moderate" to "unhealthy for sensitive groups". Winter brings the
reds and purples, peaking above 130 µg/m³ in January, while summer (June to
July) is the only season that reaches green.

The picture hides two things. Averaging each day to one square throws away the
worst single hours, and the numbers come from a model, not a roadside monitor,
so a real street is dirtier than the calendar shows.

## Run it

```
uv run fetch.py
uv run plot.py
```

`fetch.py` asks once and saves `data/hk-pm25-2026.json`; `plot.py` reads it and
writes `out/pm25-year.png`. The data is committed, so the plot runs offline.

## References

- Open-Meteo air quality API: https://open-meteo.com/en/docs/air-quality-api
- WHO global air quality guidelines: https://www.who.int/publications/i/item/9789240034228
