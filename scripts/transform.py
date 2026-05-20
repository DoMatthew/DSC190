import pathlib

import pandas as pd

src = pathlib.Path("data/clean/events.csv")
out = pathlib.Path("data/transformed/events.csv")
out.parent.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(src)
df["date"] = pd.to_datetime(df["timestamp"]).dt.strftime("%Y-%m-%d")
df.to_csv(out, index=False)
print(f"transform: {len(df)} rows -> {out}")
