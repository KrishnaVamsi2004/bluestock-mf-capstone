"""
Master Pipeline Runner
"""

import os

scripts = [
    "scripts/data_ingestion.py",
    "scripts/data_cleaning.py",
    "scripts/load_to_sqlite.py",
    "scripts/day3_eda.py",
    "scripts/day4_performance.py",
    "scripts/day5_var_cvar.py",
    "scripts/day5_rolling_sharpe.py",
    "scripts/day5_cohort_analysis.py",
    "scripts/day5_sip_continuity.py",
    "scripts/recommender.py",
    "scripts/day5_hhi.py"
]

for script in scripts:
    print(f"Running {script}")
    os.system(f"python3 {script}")

print("Pipeline Complete")
