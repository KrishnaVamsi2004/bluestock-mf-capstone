import pandas as pd

nav = pd.read_csv("data/raw/02_nav_history.csv")

nav["date"] = pd.to_datetime(nav["date"])

results = []

for code in nav["amfi_code"].unique():

    fund = nav[nav["amfi_code"] == code].sort_values("date")

    start_nav = fund["nav"].iloc[0]
    end_nav = fund["nav"].iloc[-1]

    years = (
        (fund["date"].iloc[-1] - fund["date"].iloc[0]).days
        / 365.25
    )

    cagr = ((end_nav / start_nav) ** (1 / years) - 1) * 100

    results.append([code, round(cagr, 2)])

cagr_df = pd.DataFrame(
    results,
    columns=["amfi_code", "cagr_pct"]
)

cagr_df.to_csv(
    "reports/cagr_table.csv",
    index=False
)

print(cagr_df.head())
print("\nFunds:", len(cagr_df))
print("CAGR Table Saved")
