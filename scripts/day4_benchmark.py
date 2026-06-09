import pandas as pd
import matplotlib.pyplot as plt

scorecard = pd.read_csv("reports/fund_scorecard.csv")
nav = pd.read_csv("data/raw/02_nav_history.csv")
bench = pd.read_csv("data/raw/10_benchmark_indices.csv")

top5 = scorecard["amfi_code"].head(5).tolist()

nav["date"] = pd.to_datetime(nav["date"])
bench["date"] = pd.to_datetime(bench["date"])

nav = nav[nav["amfi_code"].isin(top5)]

plt.figure(figsize=(12,6))

for code in top5:
    temp = nav[nav["amfi_code"] == code]
    temp = temp.sort_values("date")

    base = temp["nav"].iloc[0]

    plt.plot(
        temp["date"],
        temp["nav"] / base * 100,
        label=f"Fund {code}"
    )

for idx in ["NIFTY50", "NIFTY100"]:
    temp = bench[bench["index_name"] == idx]
    temp = temp.sort_values("date")

    base = temp["close_value"].iloc[0]

    plt.plot(
        temp["date"],
        temp["close_value"] / base * 100,
        label=idx
    )

plt.title("Top 5 Funds vs Benchmarks")
plt.legend()
plt.tight_layout()

plt.savefig(
    "reports/charts/benchmark_comparison.png"
)

print("Benchmark Chart Saved")
