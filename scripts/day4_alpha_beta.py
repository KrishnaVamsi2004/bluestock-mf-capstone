import pandas as pd
from scipy.stats import linregress

nav = pd.read_csv("data/raw/02_nav_history.csv")
bench = pd.read_csv("data/raw/10_benchmark_indices.csv")

nav["date"] = pd.to_datetime(nav["date"])
bench["date"] = pd.to_datetime(bench["date"])

# Fund returns
nav = nav.sort_values(["amfi_code", "date"])
nav["fund_return"] = nav.groupby("amfi_code")["nav"].pct_change()

# NIFTY100 benchmark
nifty100 = bench[bench["index_name"] == "NIFTY100"].copy()
nifty100 = nifty100.sort_values("date")

nifty100["benchmark_return"] = nifty100["close_value"].pct_change()

results = []

for code in nav["amfi_code"].unique():

    fund = nav[nav["amfi_code"] == code][
        ["date", "fund_return"]
    ]

    merged = pd.merge(
        fund,
        nifty100[["date", "benchmark_return"]],
        on="date",
        how="inner"
    ).dropna()

    if len(merged) < 30:
        continue

    slope, intercept, r, p, stderr = linregress(
        merged["benchmark_return"],
        merged["fund_return"]
    )

    alpha = intercept * 252
    beta = slope

    results.append([
        code,
        round(alpha, 4),
        round(beta, 4)
    ])

alpha_beta_df = pd.DataFrame(
    results,
    columns=[
        "amfi_code",
        "alpha",
        "beta"
    ]
)

print(alpha_beta_df.head())

print("\nFunds:", len(alpha_beta_df))

alpha_beta_df.to_csv(
    "reports/alpha_beta.csv",
    index=False
)

print("\nAlpha Beta Saved")
