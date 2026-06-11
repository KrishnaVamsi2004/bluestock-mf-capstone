import pandas as pd

score = pd.read_csv("reports/fund_scorecard.csv")
master = pd.read_csv("data/raw/01_fund_master.csv")

df = score.merge(
    master[["amfi_code","risk_category","scheme_name"]],
    on="amfi_code",
    how="left"
)

risk = input("Risk (Low/Moderate/High): ")

if risk.lower() == "low":
    filt = df["risk_category"].str.contains("Low", case=False, na=False)

elif risk.lower() == "moderate":
    filt = df["risk_category"].str.contains("Moderate", case=False, na=False)

else:
    filt = df["risk_category"].str.contains("High", case=False, na=False)

top3 = (
    df[filt]
    .sort_values("sharpe_ratio", ascending=False)
    .head(3)
)

print(top3[
    ["amfi_code","scheme_name","sharpe_ratio"]
])

top3.to_csv(
    "reports/recommended_funds.csv",
    index=False
)

print("\nRecommendations Saved")
