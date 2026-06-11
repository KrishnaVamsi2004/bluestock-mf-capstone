import pandas as pd

df = pd.read_csv("data/raw/09_portfolio_holdings.csv")

sector_col = "sector"
weight_col = "weight_pct"

hhi = (
    df.groupby("amfi_code")[weight_col]
      .apply(lambda x: (x/100).pow(2).sum())
      .reset_index(name="hhi")
)

print(hhi.head())

hhi.to_csv(
    "reports/hhi_report.csv",
    index=False
)

print("\nHHI Report Saved")
