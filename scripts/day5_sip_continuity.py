import pandas as pd

df = pd.read_csv("data/raw/08_investor_transactions.csv")

df["transaction_date"] = pd.to_datetime(df["transaction_date"])

sip = df[df["transaction_type"] == "SIP"].copy()

sip = sip.sort_values(
    ["investor_id", "transaction_date"]
)

sip["gap_days"] = (
    sip.groupby("investor_id")["transaction_date"]
       .diff()
       .dt.days
)

summary = (
    sip.groupby("investor_id")
       .agg(
            sip_count=("transaction_date", "count"),
            avg_gap=("gap_days", "mean")
       )
       .reset_index()
)

summary = summary[
    summary["sip_count"] >= 6
]

summary["status"] = summary["avg_gap"].apply(
    lambda x: "At Risk"
    if x > 35
    else "Healthy"
)

summary.to_csv(
    "reports/sip_continuity_report.csv",
    index=False
)

print(summary.head())

print("\nSIP Continuity Saved")
