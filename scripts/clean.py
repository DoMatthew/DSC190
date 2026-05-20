import pathlib

import pandas as pd

VALID_EVENT_TYPES = {"click", "login", "purchase", "scroll", "view"}

raw = pathlib.Path("data/raw/events.csv")
out = pathlib.Path("data/clean/events.csv")
out.parent.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(raw, dtype=str)

# Drop rows with any missing fields
df = df.dropna()
df = df[df.apply(lambda r: all(str(v).strip() != "" for v in r), axis=1)]

# Drop invalid event_type
df = df[df["event_type"].isin(VALID_EVENT_TYPES)]

# Drop non-positive duration_seconds
df["duration_seconds"] = pd.to_numeric(df["duration_seconds"], errors="coerce")
df = df[df["duration_seconds"] > 0]

# Normalize timestamp to ISO 8601 YYYY-MM-DDTHH:MM:SS
df["timestamp"] = pd.to_datetime(
    df["timestamp"], format="mixed", dayfirst=False
).dt.strftime("%Y-%m-%dT%H:%M:%S")

df.to_csv(out, index=False)
print(f"clean: {len(df)} rows -> {out}")
