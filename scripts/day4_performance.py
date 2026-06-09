import pandas as pd
import numpy as np

nav = pd.read_csv("data/raw/02_nav_history.csv")

nav["date"] = pd.to_datetime(nav["date"])

results = []

for code, df in nav.groupby("amfi_code"):

    df = df.sort_values("date")

    start_nav = df["nav"].iloc[0]
    end_nav = df["nav"].iloc[-1]

    years = (
        (df["date"].iloc[-1] - df["date"].iloc[0]).days
        / 365.25
    )

    cagr = ((end_nav / start_nav) ** (1 / years) - 1) * 100

    results.append([
        code,
        round(cagr, 2)
    ])

cagr_df = pd.DataFrame(
    results,
    columns=[
        "amfi_code",
        "cagr_pct"
    ]
)

print(cagr_df.head())

print("\nFunds:", len(cagr_df))
