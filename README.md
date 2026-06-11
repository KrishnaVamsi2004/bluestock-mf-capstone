# Mutual Fund Analytics Platform

## Bluestock Fintech Capstone Project

### Author

Krishna Vamsi Bommireddy

### Project Duration

01 June 2026 – 07 June 2026

---

# Project Objective

Build an end-to-end Mutual Fund Analytics Platform to analyze mutual fund performance, NAV trends, SIP inflows, AUM growth, portfolio holdings, investor behavior, and fund risk metrics using Python, SQLite, Tableau/Power BI, and GitHub.

The project covers the complete analytics lifecycle including data ingestion, cleaning, storage, performance analytics, investor analysis, dashboard development, and business reporting.

---

# Technology Stack

## Programming & Analytics

* Python
* Pandas
* NumPy
* Matplotlib
* Seaborn
* Plotly
* SciPy

## Database

* SQLite
* SQLAlchemy
* SQL

## Visualization

* Tableau
* Power BI

## Version Control

* Git
* GitHub

---

# Project Structure

bluestock_mf_capstone/

├── data/
│   ├── raw/
│   ├── processed/
│   └── db/
│
├── notebooks/
│   ├── 01_data_ingestion.ipynb
│   ├── 02_data_cleaning.ipynb
│   ├── 03_eda_analysis.ipynb
│   ├── 04_performance_analytics.ipynb
│   └── 05_advanced_analytics.ipynb
│
├── scripts/
│   ├── data_ingestion.py
│   ├── data_cleaning.py
│   ├── live_nav_fetch.py
│   ├── load_to_sqlite.py
│   ├── day3_eda.py
│   ├── day5_var_cvar.py
│   ├── day5_rolling_sharpe.py
│   ├── day5_cohort_analysis.py
│   ├── day5_sip_continuity.py
│   ├── day5_hhi.py
│   └── recommender.py
│
├── sql/
│   ├── schema.sql
│   └── queries.sql
│
├── dashboard/
│
├── reports/
│   ├── Final_Report.pdf
│   ├── Bluestock_MF_Presentation.pptx
│   ├── charts/
│   └── data_dictionary.md
│
├── README.md
└── run_pipeline.py

---

# Datasets Used

| File                         | Description              |
| ---------------------------- | ------------------------ |
| 01_fund_master.csv           | Fund master information  |
| 02_nav_history.csv           | Daily NAV history        |
| 03_aum_by_fund_house.csv     | AMC AUM data             |
| 04_monthly_sip_inflows.csv   | SIP inflow statistics    |
| 05_category_inflows.csv      | Category-wise inflows    |
| 06_industry_folio_count.csv  | Industry folio counts    |
| 07_scheme_performance.csv    | Fund performance metrics |
| 08_investor_transactions.csv | Investor transactions    |
| 09_portfolio_holdings.csv    | Portfolio holdings       |
| 10_benchmark_indices.csv     | Benchmark indices        |

---

# Day 1 – Data Ingestion & Validation

## Tasks Completed

* Created project folder structure
* Initialized Git repository
* Connected project to GitHub
* Installed project dependencies
* Loaded all datasets using Pandas
* Performed dataset inspection
* Validated schema and datatypes
* Integrated AMFI NAV API
* Retrieved live NAV data
* Saved API responses
* Conducted data quality checks

## Deliverables

* requirements.txt
* data_ingestion.py
* live_nav_fetch.py
* GitHub Repository

---

# Day 2 – Data Cleaning & Database Setup

## Data Cleaning

### NAV History

* Date standardization
* Duplicate removal
* Missing NAV handling
* Data validation

### Investor Transactions

* Transaction standardization
* Amount validation
* KYC verification
* Date cleaning

### Scheme Performance

* Metric validation
* Range verification
* Consistency checks

## Database Design

Created normalized star schema:

* dim_fund
* dim_date
* fact_nav
* fact_transactions
* fact_performance
* fact_aum

## Deliverables

* Cleaned datasets
* SQLite database
* schema.sql
* queries.sql
* data_dictionary.md

---

# Day 3 – Exploratory Data Analysis

## Charts Created

1. AUM Growth by Fund House
2. Monthly SIP Trend
3. Category Inflow Heatmap
4. Investor Age Distribution
5. Investor Gender Distribution
6. State-wise Investment Distribution
7. City Tier Distribution
8. Industry Folio Growth
9. Folio Category Comparison
10. Top Funds by Returns
11. Sector Allocation Chart
12. Expense Ratio Distribution
13. Risk Grade Distribution
14. Morningstar Rating Distribution

## Key Insights

* SBI Mutual Fund maintains highest AUM.
* SIP inflows show strong growth.
* Equity categories dominate inflows.
* Folio counts doubled from 2022 to 2025.
* Portfolio holdings show sector concentration.
* Higher-rated funds generally outperform peers.

## Deliverables

* 14 EDA Charts
* EDA Scripts
* Analytical Insights

---

# Day 4 – Performance Analytics

## Metrics Calculated

### Return Metrics

* Daily Returns
* CAGR

### Risk Metrics

* Standard Deviation
* Maximum Drawdown

### Risk Adjusted Metrics

* Sharpe Ratio
* Sortino Ratio
* Alpha
* Beta

## Outputs Generated

* cagr_table.csv
* sharpe_ratio.csv
* sortino_ratio.csv
* alpha_beta.csv
* max_drawdown.csv
* fund_scorecard.csv

## Key Findings

* Evaluated all 40 schemes.
* Ranked funds using composite scorecard.
* Benchmarked schemes against market indices.
* Identified top-performing mutual funds.

---

# Day 5 – Advanced Analytics

## Historical VaR & CVaR

Computed downside risk metrics for all schemes.

Output:

* var_cvar_report.csv

## Rolling Sharpe Ratio

Generated rolling 90-day Sharpe analysis.

Output:

* rolling_sharpe_chart.png

## Investor Cohort Analysis

Grouped investors by first transaction year.

Output:

* cohort_analysis.csv

## SIP Continuity Analysis

Identified at-risk investors based on SIP gaps.

Output:

* sip_continuity_report.csv

## Fund Recommendation Engine

Generated fund recommendations based on:

* Risk Appetite
* Sharpe Ratio
* Risk Category

Output:

* recommended_funds.csv

## Sector HHI Analysis

Measured portfolio concentration.

Output:

* hhi_report.csv

---

# Day 6 – Dashboard Development

## Dashboard Pages

### Page 1 – Industry Overview

* Industry AUM
* SIP Inflows
* Folio Count
* AUM by AMC

### Page 2 – Fund Performance

* Risk vs Return
* Fund Scorecard
* NAV vs Benchmark

### Page 3 – Investor Analytics

* State Analysis
* Age Group Analysis
* Transaction Analysis

### Page 4 – SIP & Market Trends

* SIP vs Nifty
* Category Heatmap
* Market Trend Analysis

## Features

* Interactive Filters
* Tooltips
* Drill-down Analysis
* Dynamic Charts

---

# Day 7 – Documentation & Reporting

## Deliverables

### Report

* Final_Report.pdf

### Presentation

* Bluestock_MF_Presentation.pptx

### Dashboard

* Tableau / Power BI Dashboard

### Analytics Reports

* Performance Analytics
* Advanced Analytics

---

# How To Run The Project

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Run ETL Pipeline

```bash
python3 scripts/data_ingestion.py
python3 scripts/data_cleaning.py
python3 scripts/load_to_sqlite.py
```

## Run Performance Analytics

```bash
python3 scripts/day4_performance.py
```

## Run Advanced Analytics

```bash
python3 scripts/day5_var_cvar.py
python3 scripts/day5_rolling_sharpe.py
python3 scripts/day5_cohort_analysis.py
python3 scripts/day5_sip_continuity.py
python3 scripts/recommender.py
python3 scripts/day5_hhi.py
```

## Run Complete Pipeline

```bash
python3 run_pipeline.py
```

---

# Dashboard

Open Tableau Workbook or Power BI Dashboard located in:

dashboard/

---

# Key Business Findings

1. Industry AUM exceeded ₹81 Lakh Crore.
2. SIP inflows crossed ₹31,002 Crore.
3. Mid-cap funds outperformed large-cap funds.
4. 2024 investor cohort invested the most capital.
5. Several investors were flagged as SIP continuity risks.
6. High-risk funds achieved superior Sharpe ratios.
7. Some funds showed high sector concentration.

---

# Deliverables

## D1

ETL Pipeline

## D2

SQLite Database

## D3

EDA Notebook

## D4

Performance Analytics

## D5

Interactive Dashboard

## D6

Advanced Analytics

## D7

Final Report & Presentation

---

# Final Submission Checklist

| Deliverable           | Status |
| --------------------- | ------ |
| ETL Pipeline          | ✅      |
| SQLite Database       | ✅      |
| EDA Analysis          | ✅      |
| Performance Analytics | ✅      |
| Advanced Analytics    | ✅      |
| Dashboard             | ✅      |
| Final Report          | ✅      |
| Presentation          | ✅      |
| Documentation         | ✅      |
| GitHub Repository     | ✅      |

---

# Version

v1.0

# Author

Krishna Vamsi Bommireddy

Bluestock Fintech Pvt. Ltd.

Mutual Fund Analytics Platform Capstone Project

June 2026

