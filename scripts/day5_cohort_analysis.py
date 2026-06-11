import pandas as pd

df = pd.read_csv("data/raw/08_investor_transactions.csv")

df.columns = [c.lower().replace(" ", "_") for c in df.columns]

df["transaction_date"] = pd.to_datetime(df["transaction_date"])

# First transaction per investor
first_txn = (
    df.groupby("investor_id")["transaction_date"]
      .min()
      .reset_index()
)

first_txn["cohort_year"] = first_txn["transaction_date"].dt.year

df = df.merge(
    first_txn[
        ["investor_id", "cohort_year"]
    ],
    on="investor_id",
    how="left"
)

# Avg SIP amount
avg_sip = (
    df[df["transaction_type"] == "SIP"]
      .groupby("cohort_year")["amount_inr"]
      .mean()
)

# Total invested
total_inv = (
    df.groupby("cohort_year")["amount_inr"]
      .sum()
)

# Top fund preference
top_fund = (
    df.groupby(
        ["cohort_year", "amfi_code"]
    )
    .size()
    .reset_index(name="count")
)

top_fund = (
    top_fund.sort_values(
        ["cohort_year", "count"],
        ascending=False
    )
    .groupby("cohort_year")
    .first()
    .reset_index()
)

out = pd.DataFrame({
    "cohort_year": avg_sip.index,
    "avg_sip_amount": avg_sip.values,
    "total_invested": total_inv.values
})

out = out.merge(
    top_fund[
        ["cohort_year", "amfi_code"]
    ],
    on="cohort_year"
)

out.rename(
    columns={
        "amfi_code": "top_fund"
    },
    inplace=True
)

out.to_csv(
    "reports/cohort_analysis.csv",
    index=False
)

print(out)

print("\nCohort Analysis Saved")
