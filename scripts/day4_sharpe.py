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

    annual_volatility = returns.std() * np.sqrt(252)

    sharpe = (
        annual_return - rf
    ) / annual_volatility

    results.append([
        code,
        round(sharpe, 3)
    ])

sharpe_df = pd.DataFrame(
    results,
    columns=[
        "amfi_code",
        "sharpe_ratio"
    ]
)

sharpe_df = sharpe_df.sort_values(
    "sharpe_ratio",
    ascending=False
)

sharpe_df.to_csv(
    "reports/sharpe_ratio.csv",
    index=False
)

print(sharpe_df.head())

print("\nFunds:", len(sharpe_df))

print("Sharpe Ratio Saved")
