import pathlib

import pandas as pd

src = pathlib.Path("data/transformed/events.csv")
out = pathlib.Path("data/features/events.csv")
out.parent.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(src)
df["duration_minutes"] = df["duration_seconds"] / 60
df["weekday"] = pd.to_datetime(df["date"]).dt.day_name()
df.to_csv(out, index=False)
print(f"features: {len(df)} rows -> {out}")
