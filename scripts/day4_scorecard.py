import pandas as pd

cagr = pd.read_csv("reports/cagr_table.csv")
sharpe = pd.read_csv("reports/sharpe_ratio.csv")
alpha = pd.read_csv("reports/alpha_beta.csv")
drawdown = pd.read_csv("reports/max_drawdown.csv")

df = cagr.merge(sharpe, on="amfi_code")
df = df.merge(alpha[["amfi_code", "alpha"]], on="amfi_code")
df = df.merge(drawdown, on="amfi_code")

df["cagr_rank"] = df["cagr_pct"].rank(ascending=False)
df["sharpe_rank"] = df["sharpe_ratio"].rank(ascending=False)
df["alpha_rank"] = df["alpha"].rank(ascending=False)

df["drawdown_rank"] = df["max_drawdown_pct"].rank(
    ascending=False
)

df["score"] = (
    0.30 * df["cagr_rank"] +
    0.25 * df["sharpe_rank"] +
    0.20 * df["alpha_rank"] +
    0.25 * df["drawdown_rank"]
)

df = df.sort_values(
    "score",
    ascending=False
)

print(df.head(10))

df.to_csv(
    "reports/fund_scorecard.csv",
    index=False
)

print("\nFund Scorecard Saved")
