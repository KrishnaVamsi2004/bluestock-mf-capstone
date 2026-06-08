# Mutual Fund Analytics Platform

## Objective

Build an end-to-end Mutual Fund Analytics Platform to analyze fund performance, NAV trends, SIP inflows, AUM growth, portfolio holdings, and investor behavior using Python, SQL, and Power BI.

## Datasets

* Fund Master
* NAV History
* AUM by Fund House
* Monthly SIP Inflows
* Category Inflows
* Industry Folio Count
* Scheme Performance
* Investor Transactions
* Portfolio Holdings
* Benchmark Indices
* Live NAV Data (API)

## Tech Stack

* Python
* Pandas
* NumPy
* SQL
* SQLite
* Power BI
* Git & GitHub
* Jupyter Notebook

## Project Structure

bluestock_mf_capstone/

* data/

  * raw/
  * processed/
  * db/
* notebooks/
* scripts/
* sql/
* dashboard/
* reports/
* README.md
* requirements.txt

## Day 1 - Data Ingestion & Setup

### Tasks Completed

* Created project folder structure
* Configured Python virtual environment
* Installed required dependencies
* Loaded all 10 mutual fund datasets
* Created data ingestion pipeline
* Fetched live NAV data using MFAPI
* Performed initial data quality checks
* Validated AMFI scheme codes
* Initialized Git repository
* Pushed project to GitHub

### Deliverables

* data_ingestion.py
* live_nav_fetch.py
* requirements.txt
* GitHub Repository

## Day 2 - Data Cleaning & Database Setup

### Planned Tasks

* Handle missing values
* Identify and remove duplicates
* Standardize column names
* Convert data types
* Create SQLite database
* Design SQL schema
* Load cleaned datasets into database
* Generate data quality report
* Create exploratory data analysis notebook

### Deliverables

* Cleaned datasets in data/processed/
* SQLite database
* schema.sql
* queries.sql
* Data quality report
* Jupyter notebook

## Key Validation Results

* Total Schemes: 40
* Unique Fund Houses: 10
* AMFI Validation: Passed
* Duplicate Records: None Found
* Missing Values: Detected in SIP Inflows dataset

## Future Scope

* Fund ranking system
* Risk-adjusted return analysis
* SIP growth forecasting
* Portfolio concentration analysis
* Interactive Power BI dashboard
* Automated reporting pipeline
