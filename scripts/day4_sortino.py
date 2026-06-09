import pandas as pd
import numpy as np

nav = pd.read_csv("data/raw/02_nav_history.csv")

nav["date"] = pd.to_datetime(nav["date"])

nav = nav.sort_values(["amfi_code", "date"])

nav["daily_return"] = (
    nav.groupby("amfi_code")["nav"]
       .pct_change()
)

rf = 0.065

results = []

for code in nav["amfi_code"].unique():

    fund = nav[nav["amfi_code"] == code]

    returns = fund["daily_return"].dropna()

    if len(returns) < 30:
        continue

    annual_return = returns.mean() * 252

    downside = returns[returns < 0]

    if len(downside) == 0:
        continue

    downside_std = downside.std() * np.sqrt(252)

    sortino = (
        annual_return - rf
    ) / downside_std

    results.append([
        code,
        round(sortino, 3)
    ])

sortino_df = pd.DataFrame(
    results,
    columns=[
        "amfi_code",
        "sortino_ratio"
    ]
)

sortino_df = sortino_df.sort_values(
    "sortino_ratio",
    ascending=False
)

sortino_df.to_csv(
    "reports/sortino_ratio.csv",
    index=False
)

print(sortino_df.head())

print("\nFunds:", len(sortino_df))

print("Sortino Ratio Saved")
