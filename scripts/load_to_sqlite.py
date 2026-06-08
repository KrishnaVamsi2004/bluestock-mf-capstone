from sqlalchemy import create_engine
import pandas as pd

engine = create_engine("sqlite:///data/db/bluestock_mf.db")

pd.read_csv("data/processed/fund_master_clean.csv").to_sql(
    "dim_fund",
    engine,
    if_exists="replace",
    index=False
)
