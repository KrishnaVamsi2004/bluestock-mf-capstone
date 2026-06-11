import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

nav = pd.read_csv("data/raw/02_nav_history.csv")

nav.columns = [c.lower().replace(" ", "_") for c in nav.columns]

nav["date"] = pd.to_datetime(nav["date"])

funds = [
    100016,
    100025,
    100033,
    101206,
    101207
]

plt.figure(figsize=(12,6))

for fund in funds:

    df = nav[nav["amfi_code"] == fund].copy()

    df = df.sort_values("date")

    returns = df["nav"].pct_change()

    rolling_sharpe = (
        returns.rolling(90).mean()
        /
        returns.rolling(90).std()
    ) * np.sqrt(252)

    plt.plot(
        df["date"],
        rolling_sharpe,
        label=str(fund)
    )

plt.title("Rolling 90-Day Sharpe Ratio")
plt.xlabel("Date")
plt.ylabel("Sharpe Ratio")
plt.legend()
plt.grid(True)

plt.savefig(
    "reports/charts/rolling_sharpe_chart.png",
    bbox_inches="tight"
)

print("Rolling Sharpe Chart Saved")
