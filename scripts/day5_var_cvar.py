import pandas as pd

# Load NAV history
nav = pd.read_csv("data/raw/02_nav_history.csv")

# Fix column names
nav.columns = [c.lower().replace(" ", "_") for c in nav.columns]

# Convert date
nav["date"] = pd.to_datetime(nav["date"])

results = []

for amfi_code, grp in nav.groupby("amfi_code"):

    grp = grp.sort_values("date")

    returns = grp["nav"].pct_change().dropna()

    if len(returns) < 30:
        continue

    var95 = returns.quantile(0.05)
    cvar95 = returns[returns <= var95].mean()

    results.append([
        amfi_code,
        round(var95, 4),
        round(cvar95, 4)
    ])

out = pd.DataFrame(
    results,
    columns=[
        "amfi_code",
        "var_95",
        "cvar_95"
    ]
)

out.to_csv(
    "reports/var_cvar_report.csv",
    index=False
)

print(out.head())
print("\nFunds:", len(out))
print("\nVaR/CVaR Saved")
