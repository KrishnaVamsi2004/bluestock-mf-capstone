import pandas as pd
import os

RAW_PATH = "data/raw"
PROCESSED_PATH = "data/processed"

os.makedirs(PROCESSED_PATH, exist_ok=True)

# -------------------------
# NAV HISTORY
# -------------------------
nav = pd.read_csv(f"{RAW_PATH}/02_nav_history.csv")

nav["date"] = pd.to_datetime(nav["date"])

nav = nav.sort_values(["amfi_code", "date"])

nav = nav.drop_duplicates()

nav["nav"] = nav.groupby("amfi_code")["nav"].ffill()

nav = nav[nav["nav"] > 0]

nav.to_csv(
    f"{PROCESSED_PATH}/02_nav_history_clean.csv",
    index=False
)

print("NAV History cleaned")

# -------------------------
# INVESTOR TRANSACTIONS
# -------------------------
txn = pd.read_csv(
    f"{RAW_PATH}/08_investor_transactions.csv"
)

if "transaction_date" in txn.columns:
    txn["transaction_date"] = pd.to_datetime(
        txn["transaction_date"],
        errors="coerce"
    )

if "amount" in txn.columns:
    txn = txn[txn["amount"] > 0]

txn.to_csv(
    f"{PROCESSED_PATH}/08_investor_transactions_clean.csv",
    index=False
)

print("Transactions cleaned")

# -------------------------
# SCHEME PERFORMANCE
# -------------------------
perf = pd.read_csv(
    f"{RAW_PATH}/07_scheme_performance.csv"
)

perf.to_csv(
    f"{PROCESSED_PATH}/07_scheme_performance_clean.csv",
    index=False
)

print("Scheme performance cleaned")

print("Data Cleaning Completed")
