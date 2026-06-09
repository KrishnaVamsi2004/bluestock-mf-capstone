import pandas as pd

nav = pd.read_csv("data/raw/02_nav_history.csv")

nav["date"] = pd.to_datetime(nav["date"])

results = []

for code in nav["amfi_code"].unique():

    fund = nav[nav["amfi_code"] == code].copy()

    fund = fund.sort_values("date")

    fund["running_max"] = fund["nav"].cummax()

    fund["drawdown"] = (
        fund["nav"] / fund["running_max"] - 1
    )

    max_dd = fund["drawdown"].min()

    results.append([
        code,
        round(max_dd * 100, 2)
    ])

drawdown_df = pd.DataFrame(
    results,
    columns=[
        "amfi_code",
        "max_drawdown_pct"
    ]
)

print(drawdown_df.head())

print("\nFunds:", len(drawdown_df))

drawdown_df.to_csv(
    "reports/max_drawdown.csv",
    index=False
)

print("\nMax Drawdown Saved")
