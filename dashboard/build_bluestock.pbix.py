#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║       BLUESTOCK MUTUAL FUND ANALYTICS — FULL .pbix BUILDER                  ║
║  Generates all pbi-tools source files then compiles to a real .pbix          ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  REQUIREMENTS (run once on your machine)                                     ║
║    1. Python 3.9+  →  pip install pandas openpyxl                           ║
║    2. .NET 8 SDK   →  https://dotnet.microsoft.com/download                  ║
║    3. pbi-tools    →  dotnet tool install -g pbi-tools                       ║
║                       (or download from https://pbi.tools)                   ║
║  USAGE                                                                        ║
║    python build_bluestock_pbix.py                                             ║
║  OUTPUT                                                                       ║
║    bluestock_mf_pbix_src/   ← pbi-tools source folder                        ║
║    bluestock_mf_analytics.pbix  ← compiled Power BI file                     ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import json, os, sys, shutil, subprocess, textwrap
from pathlib import Path
import pandas as pd

# ─── PATHS ───────────────────────────────────────────────────────────────────
ROOT   = Path("bluestock_mf_pbix_src")
PBIX   = Path("bluestock_mf_analytics.pbix")

# pbi-tools source layout
REPORT      = ROOT / "Report"
PAGES       = REPORT / "pages"
DATAMODEL   = ROOT / ".pbi" / "localSettings.json"
MASHUP      = ROOT / "Mashup"
CONNECTIONS = ROOT / "Connections"
SETTINGS    = ROOT / ".pbi"

def clean():
    if ROOT.exists():
        shutil.rmtree(ROOT)
    ROOT.mkdir(parents=True)
    REPORT.mkdir(parents=True)
    PAGES.mkdir(parents=True)
    (ROOT / ".pbi").mkdir(parents=True)
    MASHUP.mkdir(parents=True)
    CONNECTIONS.mkdir(parents=True)

# ═════════════════════════════════════════════════════════════════════════════
# 1.  ALL DATA (exact values from Bluestock MF Dashboard)
# ═════════════════════════════════════════════════════════════════════════════

AUM_PERIODS = ["Mar22","Jun22","Sep22","Dec22","Mar23","Jun23","Sep23",
               "Dec23","Mar24","Jun24","Sep24","Dec24","Mar25","Jun25","Sep25","Dec25"]
AUM_VALS    = [38.0,38.8,37.7,40.5,39.4,43.2,46.6,50.8,
               53.4,57.3,66.7,66.9,53.4,64.9,67.1,81.4]

FUNDS = [
  {"SchemeCode":"119551","SchemeName":"SBI Bluechip - Regular","FundHouse":"SBI Mutual Fund","Category":"Large Cap","Plan":"Regular","Return1Y":12.42,"Return3Y":12.36,"SharpeRatio":0.88,"StdDev":14.0,"AUM_Crore":14288,"Rating":4,"Alpha":0.87,"RiskGrade":"Moderate"},
  {"SchemeCode":"119552","SchemeName":"SBI Bluechip - Direct","FundHouse":"SBI Mutual Fund","Category":"Large Cap","Plan":"Direct","Return1Y":15.25,"Return3Y":11.30,"SharpeRatio":0.81,"StdDev":14.0,"AUM_Crore":1231,"Rating":3,"Alpha":1.78,"RiskGrade":"Moderate"},
  {"SchemeCode":"SBI003","SchemeName":"SBI Small Cap - Regular","FundHouse":"SBI Mutual Fund","Category":"Small Cap","Plan":"Regular","Return1Y":18.75,"Return3Y":22.10,"SharpeRatio":1.12,"StdDev":21.5,"AUM_Crore":28903,"Rating":5,"Alpha":3.20,"RiskGrade":"High"},
  {"SchemeCode":"SBI004","SchemeName":"SBI Small Cap - Direct","FundHouse":"SBI Mutual Fund","Category":"Small Cap","Plan":"Direct","Return1Y":20.10,"Return3Y":23.45,"SharpeRatio":1.19,"StdDev":21.5,"AUM_Crore":3214,"Rating":5,"Alpha":4.55,"RiskGrade":"High"},
  {"SchemeCode":"120503","SchemeName":"HDFC Top 100 - Regular","FundHouse":"HDFC Mutual Fund","Category":"Large Cap","Plan":"Regular","Return1Y":11.89,"Return3Y":14.22,"SharpeRatio":0.95,"StdDev":13.5,"AUM_Crore":32168,"Rating":4,"Alpha":2.73,"RiskGrade":"Moderate"},
  {"SchemeCode":"HDFC02","SchemeName":"HDFC Top 100 - Direct","FundHouse":"HDFC Mutual Fund","Category":"Large Cap","Plan":"Direct","Return1Y":13.05,"Return3Y":15.35,"SharpeRatio":1.00,"StdDev":13.5,"AUM_Crore":4521,"Rating":4,"Alpha":3.86,"RiskGrade":"Moderate"},
  {"SchemeCode":"120505","SchemeName":"HDFC Mid-Cap Opp - Regular","FundHouse":"HDFC Mutual Fund","Category":"Mid Cap","Plan":"Regular","Return1Y":22.30,"Return3Y":25.60,"SharpeRatio":1.35,"StdDev":19.0,"AUM_Crore":61432,"Rating":5,"Alpha":5.10,"RiskGrade":"High"},
  {"SchemeCode":"HDFC04","SchemeName":"HDFC Flexi Cap - Direct","FundHouse":"HDFC Mutual Fund","Category":"Flexi Cap","Plan":"Direct","Return1Y":17.45,"Return3Y":18.90,"SharpeRatio":1.08,"StdDev":16.0,"AUM_Crore":5643,"Rating":4,"Alpha":3.40,"RiskGrade":"Moderate"},
  {"SchemeCode":"ICICI01","SchemeName":"ICICI Pru Bluechip - Regular","FundHouse":"ICICI Prudential MF","Category":"Large Cap","Plan":"Regular","Return1Y":13.20,"Return3Y":15.80,"SharpeRatio":0.99,"StdDev":13.0,"AUM_Crore":48321,"Rating":4,"Alpha":4.31,"RiskGrade":"Moderate"},
  {"SchemeCode":"ICICI02","SchemeName":"ICICI Pru Midcap - Regular","FundHouse":"ICICI Prudential MF","Category":"Mid Cap","Plan":"Regular","Return1Y":19.85,"Return3Y":23.10,"SharpeRatio":1.20,"StdDev":20.5,"AUM_Crore":5123,"Rating":4,"Alpha":2.60,"RiskGrade":"High"},
  {"SchemeCode":"125494","SchemeName":"Axis Bluechip - Direct","FundHouse":"Axis Mutual Fund","Category":"Large Cap","Plan":"Direct","Return1Y":10.50,"Return3Y":9.80,"SharpeRatio":0.72,"StdDev":14.5,"AUM_Crore":37820,"Rating":3,"Alpha":-0.69,"RiskGrade":"Moderate"},
  {"SchemeCode":"MIRAE01","SchemeName":"Mirae Asset ELSS - Direct","FundHouse":"Mirae Asset MF","Category":"ELSS","Plan":"Direct","Return1Y":16.70,"Return3Y":17.20,"SharpeRatio":1.05,"StdDev":17.5,"AUM_Crore":21432,"Rating":5,"Alpha":3.70,"RiskGrade":"High"},
  {"SchemeCode":"NIP01","SchemeName":"Nippon India Liquid - Regular","FundHouse":"Nippon India MF","Category":"Liquid","Plan":"Regular","Return1Y":7.20,"Return3Y":6.90,"SharpeRatio":2.10,"StdDev":0.8,"AUM_Crore":28451,"Rating":3,"Alpha":0.20,"RiskGrade":"Low"},
  {"SchemeCode":"DSP01","SchemeName":"DSP Gilt - Regular","FundHouse":"DSP Mutual Fund","Category":"Gilt","Plan":"Regular","Return1Y":9.40,"Return3Y":8.50,"SharpeRatio":1.45,"StdDev":6.2,"AUM_Crore":2841,"Rating":3,"Alpha":0.50,"RiskGrade":"Moderate"},
  {"SchemeCode":"KOT01","SchemeName":"Kotak Small Cap - Direct","FundHouse":"Kotak Mahindra MF","Category":"Small Cap","Plan":"Direct","Return1Y":21.50,"Return3Y":26.80,"SharpeRatio":1.28,"StdDev":22.0,"AUM_Crore":14230,"Rating":5,"Alpha":5.80,"RiskGrade":"High"},
  {"SchemeCode":"UTI01","SchemeName":"UTI Nifty 50 Index - Direct","FundHouse":"UTI Mutual Fund","Category":"Large Cap","Plan":"Direct","Return1Y":12.80,"Return3Y":13.50,"SharpeRatio":0.91,"StdDev":13.2,"AUM_Crore":19200,"Rating":4,"Alpha":0.10,"RiskGrade":"Moderate"},
  {"SchemeCode":"ABSL01","SchemeName":"ABSL Frontline Equity - Regular","FundHouse":"Aditya Birla Sun Life MF","Category":"Large Cap","Plan":"Regular","Return1Y":11.70,"Return3Y":13.90,"SharpeRatio":0.92,"StdDev":13.8,"AUM_Crore":22500,"Rating":4,"Alpha":1.95,"RiskGrade":"Moderate"},
  {"SchemeCode":"ABSL02","SchemeName":"ABSL Small Cap - Direct","FundHouse":"Aditya Birla Sun Life MF","Category":"Small Cap","Plan":"Direct","Return1Y":19.40,"Return3Y":24.20,"SharpeRatio":1.22,"StdDev":21.8,"AUM_Crore":5100,"Rating":5,"Alpha":4.15,"RiskGrade":"High"},
  {"SchemeCode":"NIP02","SchemeName":"Nippon India Growth - Direct","FundHouse":"Nippon India MF","Category":"Mid Cap","Plan":"Direct","Return1Y":20.60,"Return3Y":24.80,"SharpeRatio":1.30,"StdDev":20.0,"AUM_Crore":31200,"Rating":5,"Alpha":4.90,"RiskGrade":"High"},
  {"SchemeCode":"KOT02","SchemeName":"Kotak Emerging Equity - Regular","FundHouse":"Kotak Mahindra MF","Category":"Mid Cap","Plan":"Regular","Return1Y":18.90,"Return3Y":22.40,"SharpeRatio":1.18,"StdDev":19.5,"AUM_Crore":41000,"Rating":5,"Alpha":3.60,"RiskGrade":"High"},
]

SIP_INFLOWS = [11517,12328,12140,12976,13686,14265,15245,16928,
               18838,20371,23332,25323,26400,23109,24509,25323,31002]
NIFTY_VALS  = [17492,17245,16958,18012,17891,18634,19752,20267,
               21964,22648,25014,24874,23508,24346,25219,26216,24700]

FOLIO_EQUITY  = [9.28,9.74,10.35,10.90,11.50,12.22,12.93,13.72,14.60,15.52,16.23,16.83,17.32,17.86,18.12,17.92,18.28]
FOLIO_DEBT    = [1.86,1.95,2.05,2.15,2.24,2.35,2.44,2.55,2.66,2.78,2.90,3.03,3.15,3.28,3.41,3.58,3.66]
FOLIO_HYBRID  = [0.80,0.83,0.87,0.91,0.95,0.99,1.03,1.08,1.13,1.18,1.23,1.30,1.37,1.45,1.50,1.54,1.57]
SIP_ACCOUNTS  = [4.91,4.93,5.02,5.15,5.30,5.50,5.78,6.02,6.39,6.75,7.10,7.49,7.90,8.28,8.67,9.10]

CAT_MONTHS = ["Apr24","May24","Jun24","Jul24","Aug24","Sep24",
               "Oct24","Nov24","Dec24","Jan25","Feb25","Mar25"]
CAT_DATA = {
    "Large Cap": [2413,2580,2634,2712,2498,2891,3012,2734,2856,3124,2987,3201],
    "Mid Cap":   [3897,4012,4234,4567,3934,4789,5012,4623,4912,5234,4978,5567],
    "Small Cap": [2145,2367,2012,2589,2234,2734,2891,2612,2789,2934,2756,2967],
    "Flexi Cap": [1823,1956,2012,2234,1978,2345,2456,2123,2345,2567,2389,2678],
    "ELSS":      [891,978,1045,1123,967,1234,1289,1123,1234,1345,1267,1456],
    "Liquid":    [-892,-756,-834,-912,-834,-978,-1012,-889,-934,-1023,-945,-1089],
}
SIP_GROWTH_PERIODS = ["Jan23","Apr23","Jul23","Oct23","Jan24","Apr24","Jul24","Oct24","Jan25","Apr25","Jul25","Oct25","Dec25"]
SIP_GROWTH_AUM     = [5.20,5.95,6.58,7.04,7.55,8.02,8.63,8.97,8.50,8.83,9.01,9.18,9.25]
SIP_GROWTH_YOY     = [20.1,21.4,23.8,25.2,27.1,25.3,23.7,21.8,20.5,18.9,17.2,15.8,14.2]

AMC_HOUSES = ["SBI Mutual Fund","ICICI Prudential MF","HDFC Mutual Fund","Nippon India MF",
               "Kotak Mahindra MF","ABSL MF","UTI Mutual Fund","Axis Mutual Fund","Mirae Asset MF","DSP Mutual Fund"]
AMC_AUM    = [12.50,10.74,9.30,7.00,5.80,4.60,4.10,3.50,2.90,2.30]

# ═════════════════════════════════════════════════════════════════════════════
# 2.  pbi-tools MODEL.json  (data model + relationships + DAX measures)
# ═════════════════════════════════════════════════════════════════════════════

def build_model_bim():
    """Generate model.bim — the Tabular Model JSON that pbi-tools uses."""

    # ── Inline data as DAX tables ─────────────────────────────────────────────
    def csv_expr(headers, rows):
        """Build a DATATABLE DAX expression."""
        def fmt(v):
            if v is None: return "BLANK()"
            if isinstance(v, str): return f'"{v}"'
            return str(v)
        header_part = ", ".join(f'"{h}", {dtype(rows, i)}'
                                for i, h in enumerate(headers))
        row_parts = ",\n            ".join(
            "{" + ", ".join(fmt(r[i]) for i in range(len(headers))) + "}"
            for r in rows
        )
        return f"DATATABLE({header_part},\n        {{{row_parts}}})"

    def dtype(rows, col_idx):
        sample = next((r[col_idx] for r in rows if r[col_idx] is not None), "")
        if isinstance(sample, float): return "DOUBLE"
        if isinstance(sample, int):   return "INTEGER"
        return "STRING"

    # Build rows for each table
    aum_rows  = [[p, v] for p, v in zip(AUM_PERIODS, AUM_VALS)]
    sip_rows  = [[p, inf, n] for p, inf, n in zip(AUM_PERIODS, SIP_INFLOWS, NIFTY_VALS)]
    folio_rows= [[p, e, d, h, round(e+d+h,2)]
                 for p,e,d,h in zip(AUM_PERIODS, FOLIO_EQUITY, FOLIO_DEBT, FOLIO_HYBRID)]
    sipa_rows = [[p, a] for p, a in zip(AUM_PERIODS[:16], SIP_ACCOUNTS)]
    amc_rows  = [[h, v, round(v/sum(AMC_AUM)*100,2)]
                 for h, v in zip(AMC_HOUSES, AMC_AUM)]
    fund_rows = [[f["SchemeCode"],f["SchemeName"],f["FundHouse"],f["Category"],
                  f["Plan"],f["Return1Y"],f["Return3Y"],f["SharpeRatio"],
                  f["StdDev"],f["AUM_Crore"],f["Rating"],f["Alpha"],f["RiskGrade"]]
                 for f in FUNDS]
    cat_rows  = [[cat, m, v]
                 for cat, vals in CAT_DATA.items()
                 for m, v in zip(CAT_MONTHS, vals)]
    sg_rows   = [[p, a, g] for p, a, g in zip(SIP_GROWTH_PERIODS, SIP_GROWTH_AUM, SIP_GROWTH_YOY)]
    txn_rows  = [["SIP",19716,60.0],["Lumpsum",8095,24.7],["Redemption",4967,15.2]]
    state_rows= [["Punjab",315780,"T30"],["Tamil Nadu",315177,"T30"],
                 ["Madhya Pradesh",308312,"B30"],["Rajasthan",298645,"B30"],
                 ["Gujarat",298358,"T30"],["West Bengal",297182,"T30"],
                 ["Telangana",290219,"T30"],["Delhi",289633,"T30"],
                 ["Uttar Pradesh",285368,"B30"],["Haryana",279634,"T30"]]
    age_rows  = [["18-25",108144],["26-35",107821],["36-45",107003],
                 ["46-55",107278],["56+",105613]]
    mtxn_rows = [["Jan24",2612],["Feb24",2488],["Mar24",2843],["Apr24",2715],
                 ["May24",2658],["Jun24",2730],["Jul24",2839],["Aug24",2756],
                 ["Sep24",2842],["Oct24",2981],["Nov24",2834],["Dec24",3083]]
    kpi_rows  = [
        ["Total Industry AUM","81.44","₹ Lakh Crore","Dec 2025",34.7],
        ["Monthly SIP Inflows","31002","₹ Crore","Dec 2025",32.1],
        ["Total Folios","26.12","Crore","Dec 2025",97.0],
        ["Total Schemes","40","Count","Dec 2025",0.0],
        ["Active SIP Accounts","9.35","Crore","Dec 2025",90.0],
    ]

    # ── DAX Measures ─────────────────────────────────────────────────────────
    measures = [
        # Page 1 — Industry KPIs
        ("Latest Industry AUM",
         'CALCULATE(MAX(AUM_Trend[AUM_LakhCrore]), AUM_Trend[Period] = "Dec25")',
         "₹ L Cr"),
        ("Latest SIP Inflow",
         'CALCULATE(MAX(SIP_Monthly[SIP_Inflows_Cr]), SIP_Monthly[Period] = "Dec25")',
         "₹ Cr"),
        ("Latest SIP Accounts",
         'CALCULATE(MAX(SIP_Accounts[ActiveAccounts]), SIP_Accounts[Period] = "Oct25")',
         "Crore"),
        ("Latest Total Folios",
         'CALCULATE(MAX(Folio_Growth[Total_Folios]), Folio_Growth[Period] = "Dec25")',
         "Crore"),
        ("Total Schemes",
         "DISTINCTCOUNT(Fund_Scorecard[SchemeCode])",
         "Count"),
        ("AUM YoY Growth Pct",
         """
VAR _cur = CALCULATE(MAX(AUM_Trend[AUM_LakhCrore]), AUM_Trend[Period] = "Dec25")
VAR _py  = CALCULATE(MAX(AUM_Trend[AUM_LakhCrore]), AUM_Trend[Period] = "Dec24")
RETURN DIVIDE(_cur - _py, _py) * 100""",
         "%"),
        # Page 2 — Fund Performance
        ("Avg 1Y Return",
         "AVERAGE(Fund_Scorecard[Return1Y])",
         "%"),
        ("Avg 3Y Return",
         "AVERAGE(Fund_Scorecard[Return3Y])",
         "%"),
        ("Avg Sharpe Ratio",
         "AVERAGE(Fund_Scorecard[SharpeRatio])",
         ""),
        ("Total AUM Selected",
         "SUM(Fund_Scorecard[AUM_Crore])",
         "₹ Cr"),
        ("Funds Positive Alpha Pct",
         """
DIVIDE(
    COUNTROWS(FILTER(Fund_Scorecard, Fund_Scorecard[Alpha] > 0)),
    COUNTROWS(Fund_Scorecard)
) * 100""",
         "%"),
        ("High Risk Count",
         'CALCULATE(COUNTROWS(Fund_Scorecard), Fund_Scorecard[RiskGrade] = "High")',
         ""),
        # Page 3 — Investor
        ("Total Transactions",
         "SUM(Txn_By_Type[Count])",
         ""),
        ("SIP Share Pct",
         """DIVIDE(
    CALCULATE(SUM(Txn_By_Type[Count]), Txn_By_Type[TxnType] = "SIP"),
    [Total Transactions]
) * 100""",
         "%"),
        ("Avg SIP Ticket",
         "AVERAGE(Age_Avg_SIP[AvgSIPAmt])",
         "₹"),
        ("T30 Txn Share Pct",
         """DIVIDE(
    CALCULATE(SUM(Txn_By_State[TxnAmount]), Txn_By_State[CityTier] = "T30"),
    SUM(Txn_By_State[TxnAmount])
) * 100""",
         "%"),
        ("Peak Monthly Txn",
         "MAX(Monthly_Txn_Vol[TxnCount])",
         ""),
        # Page 4 — SIP & Market
        ("Net Category Inflow FY25",
         "SUM(Category_Inflows[NetInflow_Cr])",
         "₹ Cr"),
        ("Latest SIP YoY Growth",
         """CALCULATE(
    MAX(SIP_Growth[YoY_Growth_Pct]),
    SIP_Growth[Period] = "Dec25"
)""",
         "%"),
        ("SIP AUM CAGR 3Y",
         """
VAR _s = CALCULATE(MIN(SIP_Growth[SIP_AUM_LCr]), SIP_Growth[Period] = "Jan23")
VAR _e = CALCULATE(MAX(SIP_Growth[SIP_AUM_LCr]), SIP_Growth[Period] = "Dec25")
RETURN (POWER(_e / _s, 1.0/3) - 1) * 100""",
         "%"),
        ("Liquid Net Outflow",
         'CALCULATE(SUM(Category_Inflows[NetInflow_Cr]), Category_Inflows[Category] = "Liquid")',
         "₹ Cr"),
    ]

    def table(name, dax_expr, columns, meas=None):
        cols = [{"name": c[0], "dataType": c[1],
                 "sourceColumn": c[0],
                 "formatString": c[2] if len(c) > 2 else ""}
                for c in columns]
        t = {
            "name": name,
            "columns": cols,
            "partitions": [{"name": f"{name}-part", "mode": "import",
                            "source": {"type": "calculated", "expression": dax_expr}}],
        }
        if meas:
            t["measures"] = meas
        return t

    def meas_list(items):
        return [{"name": m[0], "expression": m[1].strip(),
                 "formatString": m[2] if len(m) > 2 else ""}
                for m in items]

    tables = [
        table("AUM_Trend",
              csv_expr(["Period","AUM_LakhCrore"], aum_rows),
              [("Period","string"),("AUM_LakhCrore","double","#,0.0")],
              meas_list([m for m in measures if m[0] in
                         ("Latest Industry AUM","AUM YoY Growth Pct")])),

        table("SIP_Monthly",
              csv_expr(["Period","SIP_Inflows_Cr","NIFTY50"], sip_rows),
              [("Period","string"),("SIP_Inflows_Cr","int64","₹#,##0"),("NIFTY50","int64","#,##0")],
              meas_list([m for m in measures if m[0] in
                         ("Latest SIP Inflow",)])),

        table("Folio_Growth",
              csv_expr(["Period","Equity","Debt","Hybrid","Total_Folios"], folio_rows),
              [("Period","string"),("Equity","double"),("Debt","double"),
               ("Hybrid","double"),("Total_Folios","double","#,0.00")],
              meas_list([m for m in measures if m[0] in
                         ("Latest Total Folios",)])),

        table("SIP_Accounts",
              csv_expr(["Period","ActiveAccounts"], sipa_rows),
              [("Period","string"),("ActiveAccounts","double","#,0.00")],
              meas_list([m for m in measures if m[0] in
                         ("Latest SIP Accounts",)])),

        table("AMC_AUM_Snapshot",
              csv_expr(["FundHouse","AUM_LakhCrore","MarketShare_Pct"], amc_rows),
              [("FundHouse","string"),("AUM_LakhCrore","double","#,0.00"),
               ("MarketShare_Pct","double","0.0%")]),

        table("Fund_Scorecard",
              csv_expr(["SchemeCode","SchemeName","FundHouse","Category","Plan",
                        "Return1Y","Return3Y","SharpeRatio","StdDev",
                        "AUM_Crore","Rating","Alpha","RiskGrade"], fund_rows),
              [("SchemeCode","string"),("SchemeName","string"),
               ("FundHouse","string"),("Category","string"),("Plan","string"),
               ("Return1Y","double","0.0%"),("Return3Y","double","0.0%"),
               ("SharpeRatio","double","0.00"),("StdDev","double","0.0%"),
               ("AUM_Crore","int64","₹#,##0"),("Rating","int64"),
               ("Alpha","double","0.00"),("RiskGrade","string")],
              meas_list([m for m in measures if m[0] in
                         ("Avg 1Y Return","Avg 3Y Return","Avg Sharpe Ratio",
                          "Total AUM Selected","Funds Positive Alpha Pct",
                          "High Risk Count","Total Schemes")])),

        table("Category_Inflows",
              csv_expr(["Category","Month","NetInflow_Cr"], cat_rows),
              [("Category","string"),("Month","string"),
               ("NetInflow_Cr","int64","₹#,##0")],
              meas_list([m for m in measures if m[0] in
                         ("Net Category Inflow FY25","Liquid Net Outflow")])),

        table("SIP_Growth",
              csv_expr(["Period","SIP_AUM_LCr","YoY_Growth_Pct"], sg_rows),
              [("Period","string"),("SIP_AUM_LCr","double"),
               ("YoY_Growth_Pct","double","0.0%")],
              meas_list([m for m in measures if m[0] in
                         ("Latest SIP YoY Growth","SIP AUM CAGR 3Y")])),

        table("Txn_By_Type",
              csv_expr(["TxnType","Count","Pct"], txn_rows),
              [("TxnType","string"),("Count","int64"),("Pct","double","0.0%")],
              meas_list([m for m in measures if m[0] in
                         ("Total Transactions","SIP Share Pct")])),

        table("Txn_By_State",
              csv_expr(["State","TxnAmount","CityTier"], state_rows),
              [("State","string"),("TxnAmount","int64","₹#,##0"),("CityTier","string")],
              meas_list([m for m in measures if m[0] in
                         ("T30 Txn Share Pct",)])),

        table("Age_Avg_SIP",
              csv_expr(["AgeGroup","AvgSIPAmt"], age_rows),
              [("AgeGroup","string"),("AvgSIPAmt","int64","₹#,##0")],
              meas_list([m for m in measures if m[0] in
                         ("Avg SIP Ticket",)])),

        table("Monthly_Txn_Vol",
              csv_expr(["Month","TxnCount"], mtxn_rows),
              [("Month","string"),("TxnCount","int64")],
              meas_list([m for m in measures if m[0] in
                         ("Peak Monthly Txn",)])),

        table("KPI_Summary",
              csv_expr(["KPI","Value","Unit","AsOf","YoY_Pct"], kpi_rows),
              [("KPI","string"),("Value","string"),("Unit","string"),
               ("AsOf","string"),("YoY_Pct","double","0.0%")]),
    ]

    relationships = [
        {"name":"Fund-NAV","fromTable":"Fund_Scorecard","fromColumn":"SchemeCode",
         "toTable":"SIP_Monthly","toColumn":"Period",
         "crossFilteringBehavior":"oneDirection"},
        {"name":"AMC-Fund","fromTable":"AMC_AUM_Snapshot","fromColumn":"FundHouse",
         "toTable":"Fund_Scorecard","toColumn":"FundHouse",
         "crossFilteringBehavior":"oneDirection"},
        {"name":"Cat-Fund","fromTable":"Category_Inflows","fromColumn":"Category",
         "toTable":"Fund_Scorecard","toColumn":"Category",
         "crossFilteringBehavior":"bothDirections"},
        {"name":"State-Age","fromTable":"Txn_By_State","fromColumn":"State",
         "toTable":"Age_Avg_SIP","toColumn":"AgeGroup",
         "crossFilteringBehavior":"oneDirection"},
    ]

    bim = {
        "name": "BluestockMFModel",
        "compatibilityLevel": 1567,
        "model": {
            "culture": "en-IN",
            "tables": tables,
            "relationships": relationships,
            "annotations": [
                {"name": "PBIDesktopVersion", "value": "2.136.0"},
                {"name": "ClientCompatibilityLevel", "value": "700"},
            ],
        },
    }
    return bim

# ═════════════════════════════════════════════════════════════════════════════
# 3.  REPORT LAYOUT  (pbi-tools page JSON files)
# ═════════════════════════════════════════════════════════════════════════════

THEME_COLORS = ["#1a56db","#10b981","#f59e0b","#ef4444","#8b5cf6","#3b82f6","#60a5fa"]

def card_visual(x, y, w, h, title, measure, table_name, fmt=""):
    return {
        "name": title.replace(" ", "_"),
        "type": "card",
        "position": {"x": x, "y": y, "width": w, "height": h},
        "config": json.dumps({
            "version": "5.1.0",
            "themeCollection": {"baseTheme": {"name": "CY22SU10"}},
            "visualType": "card",
            "displayName": title,
            "dataRoles": [
                {"role": "Fields", "items": [
                    {"type": "measure",
                     "measure": measure,
                     "table": table_name,
                     "displayName": title}
                ]}
            ],
            "objects": {
                "labels": [{"properties": {
                    "fontSize": {"solid": {"color": "#0f172a"}},
                    "fontFamily": "Segoe UI",
                }}],
                "title": [{"properties": {
                    "text": {"expr": {"Literal": {"Value": f"'{title}'"}}},
                    "show": {"expr": {"Literal": {"Value": "true"}}},
                    "fontSize": {"expr": {"Literal": {"Value": "10"}}},
                    "fontColor": {"solid": {"color": "#64748b"}},
                }}],
            },
        }),
    }

def chart_visual(x, y, w, h, vis_type, display_name, config_extra):
    return {
        "name": display_name.replace(" ", "_"),
        "type": vis_type,
        "position": {"x": x, "y": y, "width": w, "height": h},
        "config": json.dumps({
            "version": "5.1.0",
            "themeCollection": {"baseTheme": {"name": "CY22SU10"}},
            "visualType": vis_type,
            "displayName": display_name,
            **config_extra,
        }),
    }

def page(name, display, width, height, visuals, filters=None):
    return {
        "name": name,
        "displayName": display,
        "width": width,
        "height": height,
        "defaultFilterAction": "None",
        "visualContainers": visuals,
        "filters": json.dumps(filters or []),
        "config": json.dumps({
            "version": "5.1.0",
            "themeCollection": {"baseTheme": {"name": "CY22SU10"}},
        }),
    }

def build_report_layout():
    # ── Reusable chart config builder ─────────────────────────────────────────
    def line_cfg(table, axis_col, value_cols, colors=None):
        colors = colors or THEME_COLORS
        return {
            "dataRoles": [
                {"role": "Category", "items": [{"type":"column","table":table,"column":axis_col}]},
                {"role": "Y", "items": [
                    {"type":"column","table":table,"column":c} for c in value_cols
                ]},
            ],
            "objects": {
                "dataPoint": [{"properties": {
                    "defaultColor": {"solid": {"color": colors[0]}},
                }}],
                "lineStyles": [{"id": {"calc":"RelativeValue"},"properties":{
                    "interpolation": {"enum": "cardinal"},
                }}],
            },
        }

    def bar_cfg(table, axis_col, value_cols, orient="vertical", colors=None):
        colors = colors or THEME_COLORS
        return {
            "dataRoles": [
                {"role": "Category",
                 "items": [{"type":"column","table":table,"column":axis_col}]},
                {"role": "Y",
                 "items": [{"type":"column","table":table,"column":c} for c in value_cols]},
            ],
            "objects": {
                "dataPoint": [{"properties": {
                    "defaultColor": {"solid": {"color": colors[0]}},
                }}],
            },
        }

    def donut_cfg(table, cat_col, val_col):
        return {
            "dataRoles": [
                {"role": "Category", "items":[{"type":"column","table":table,"column":cat_col}]},
                {"role": "Y",        "items":[{"type":"column","table":table,"column":val_col}]},
            ],
            "objects": {
                "dataPoint": [
                    {"id":{"data":[{"expr":{"Column":{"Expression":{"SourceRef":{"Entity":table}},
                                             "Property":cat_col}}}]},
                     "properties":{"fill":{"solid":{"color":c}}}}
                    for c in THEME_COLORS[:3]
                ],
            },
        }

    def scatter_cfg():
        return {
            "dataRoles": [
                {"role": "Category",    "items":[{"type":"column","table":"Fund_Scorecard","column":"SchemeName"}]},
                {"role": "X",           "items":[{"type":"column","table":"Fund_Scorecard","column":"Return3Y"}]},
                {"role": "Y",           "items":[{"type":"column","table":"Fund_Scorecard","column":"StdDev"}]},
                {"role": "Size",        "items":[{"type":"column","table":"Fund_Scorecard","column":"AUM_Crore"}]},
                {"role": "Play",        "items":[]},
            ],
            "objects": {
                "xAxisReferenceLine": [{"properties": {"value": {"expr": {"Literal": {"Value": "0D"}}}}}],
            },
        }

    def matrix_cfg():
        return {
            "dataRoles": [
                {"role": "Rows", "items": [
                    {"type":"column","table":"Fund_Scorecard","column":"SchemeName"},
                    {"type":"column","table":"Fund_Scorecard","column":"FundHouse"},
                    {"type":"column","table":"Fund_Scorecard","column":"Category"},
                    {"type":"column","table":"Fund_Scorecard","column":"Plan"},
                    {"type":"column","table":"Fund_Scorecard","column":"Return1Y"},
                    {"type":"column","table":"Fund_Scorecard","column":"Return3Y"},
                    {"type":"column","table":"Fund_Scorecard","column":"SharpeRatio"},
                    {"type":"column","table":"Fund_Scorecard","column":"StdDev"},
                    {"type":"column","table":"Fund_Scorecard","column":"AUM_Crore"},
                    {"type":"column","table":"Fund_Scorecard","column":"Rating"},
                    {"type":"column","table":"Fund_Scorecard","column":"Alpha"},
                    {"type":"column","table":"Fund_Scorecard","column":"RiskGrade"},
                ]},
            ],
            "objects": {
                "grid": [{"properties":{
                    "gridVertical":     {"expr":{"Literal":{"Value":"false"}}},
                    "rowPadding":       {"expr":{"Literal":{"Value":"4"}}},
                    "outlineColor":     {"solid":{"color":"#e2e8f0"}},
                }}],
                "columnHeaders": [{"properties":{
                    "fontColor":        {"solid":{"color":"#64748b"}},
                    "backColor":        {"solid":{"color":"#f8fafc"}},
                    "fontSize":         {"expr":{"Literal":{"Value":"11"}}},
                }}],
            },
        }

    def slicer_cfg(table, col):
        return {
            "dataRoles": [
                {"role": "Field","items":[{"type":"column","table":table,"column":col}]},
            ],
            "objects": {
                "selection":  [{"properties":{"selectAllCheckboxEnabled":{"expr":{"Literal":{"Value":"true"}}}}}],
                "header":     [{"properties":{"fontColor":{"solid":{"color":"#64748b"}},
                                              "fontSize":{"expr":{"Literal":{"Value":"11"}}}}}],
                "items":      [{"properties":{"fontColor":{"solid":{"color":"#0f172a"}},
                                              "fontSize":{"expr":{"Literal":{"Value":"12"}}}}}],
            },
        }

    # ── Page 1: Industry Overview ────────────────────────────────────────────
    p1_visuals = [
        # KPI Row
        card_visual(20,  20, 220, 88, "Total AUM",          "Latest Industry AUM",  "AUM_Trend"),
        card_visual(256, 20, 220, 88, "SIP Inflows",        "Latest SIP Inflow",    "SIP_Monthly"),
        card_visual(492, 20, 220, 88, "Total Folios",       "Latest Total Folios",  "Folio_Growth"),
        card_visual(728, 20, 220, 88, "SIP Accounts",       "Latest SIP Accounts",  "SIP_Accounts"),
        card_visual(964, 20, 220, 88, "Total Schemes",      "Total Schemes",        "Fund_Scorecard"),
        # Charts
        chart_visual(20,  124, 780, 260, "lineChart",
                     "Industry AUM Trend 2022–2025",
                     line_cfg("AUM_Trend","Period",["AUM_LakhCrore"])),
        chart_visual(816, 124, 388, 260, "barChart",
                     "AUM by Fund House (Dec 2025)",
                     bar_cfg("AMC_AUM_Snapshot","FundHouse",["AUM_LakhCrore"],orient="horizontal")),
        chart_visual(20,  400, 580, 220, "hundredPercentStackedBarChart",
                     "Folio Growth by Type",
                     bar_cfg("Folio_Growth","Period",["Equity","Debt","Hybrid"])),
        chart_visual(616, 400, 588, 220, "areaChart",
                     "SIP Account Growth",
                     line_cfg("SIP_Accounts","Period",["ActiveAccounts"],colors=["#8b5cf6"])),
    ]

    # ── Page 2: Fund Performance ─────────────────────────────────────────────
    p2_visuals = [
        card_visual(20,  20, 192, 80, "Avg 1Y Return",       "Avg 1Y Return",          "Fund_Scorecard"),
        card_visual(228, 20, 192, 80, "Avg 3Y Return",       "Avg 3Y Return",          "Fund_Scorecard"),
        card_visual(436, 20, 192, 80, "Avg Sharpe",          "Avg Sharpe Ratio",       "Fund_Scorecard"),
        card_visual(644, 20, 192, 80, "Total AUM",           "Total AUM Selected",     "Fund_Scorecard"),
        card_visual(852, 20, 192, 80, "+Alpha Funds",        "Funds Positive Alpha Pct","Fund_Scorecard"),
        card_visual(1060,20, 192, 80, "High Risk",           "High Risk Count",        "Fund_Scorecard"),
        chart_visual(20,  116, 560, 300, "scatterChart",
                     "Risk vs Return (Bubble = AUM)", scatter_cfg()),
        chart_visual(596, 116, 608, 300, "lineChart",
                     "NAV Trend vs NIFTY 50",
                     line_cfg("SIP_Monthly","Period",["SIP_Inflows_Cr","NIFTY50"],
                               colors=["#1a56db","#f59e0b"])),
        chart_visual(20,  432, 1184, 480, "tableEx",
                     "Fund Scorecard", matrix_cfg()),
        # Slicers
        chart_visual(20,  928, 260, 60, "slicer",
                     "FundHouse Filter",
                     slicer_cfg("Fund_Scorecard","FundHouse")),
        chart_visual(296, 928, 200, 60, "slicer",
                     "Category Filter",
                     slicer_cfg("Fund_Scorecard","Category")),
        chart_visual(512, 928, 160, 60, "slicer",
                     "Plan Filter",
                     slicer_cfg("Fund_Scorecard","Plan")),
        chart_visual(688, 928, 160, 60, "slicer",
                     "Risk Filter",
                     slicer_cfg("Fund_Scorecard","RiskGrade")),
    ]

    # ── Page 3: Investor Analytics ───────────────────────────────────────────
    p3_visuals = [
        card_visual(20,  20, 224, 80, "Total Txns",    "Total Transactions", "Txn_By_Type"),
        card_visual(260, 20, 224, 80, "SIP Share %",   "SIP Share Pct",      "Txn_By_Type"),
        card_visual(500, 20, 224, 80, "Avg SIP Ticket","Avg SIP Ticket",      "Age_Avg_SIP"),
        card_visual(740, 20, 224, 80, "T30 Share %",   "T30 Txn Share Pct",  "Txn_By_State"),
        card_visual(980, 20, 224, 80, "Peak Monthly",  "Peak Monthly Txn",   "Monthly_Txn_Vol"),
        chart_visual(20,  116, 580, 300, "barChart",
                     "Txn Amount by State (Top 10)",
                     bar_cfg("Txn_By_State","State",["TxnAmount"],orient="horizontal")),
        chart_visual(616, 116, 588, 300, "donutChart",
                     "Transaction Type Split",
                     donut_cfg("Txn_By_Type","TxnType","Count")),
        chart_visual(20,  432, 560, 240, "barChart",
                     "Age Group vs Avg SIP Amount",
                     bar_cfg("Age_Avg_SIP","AgeGroup",["AvgSIPAmt"])),
        chart_visual(600, 432, 604, 240, "lineChart",
                     "Monthly Transaction Volume 2024",
                     line_cfg("Monthly_Txn_Vol","Month",["TxnCount"],colors=["#8b5cf6"])),
        chart_visual(20,  688, 240, 60, "slicer",
                     "State Filter",   slicer_cfg("Txn_By_State","State")),
        chart_visual(276, 688, 200, 60, "slicer",
                     "CityTier Filter",slicer_cfg("Txn_By_State","CityTier")),
    ]

    # ── Page 4: SIP & Market Trends ──────────────────────────────────────────
    p4_visuals = [
        card_visual(20,  20, 224, 80, "SIP CAGR 3Y",      "SIP AUM CAGR 3Y",          "SIP_Growth"),
        card_visual(260, 20, 224, 80, "Latest YoY Growth","Latest SIP YoY Growth",     "SIP_Growth"),
        card_visual(500, 20, 224, 80, "FY25 Net Inflow",  "Net Category Inflow FY25",  "Category_Inflows"),
        card_visual(740, 20, 224, 80, "Liquid Outflow",   "Liquid Net Outflow",        "Category_Inflows"),
        card_visual(980, 20, 224, 80, "Total Schemes",    "Total Schemes",             "Fund_Scorecard"),
        chart_visual(20,  116, 1164, 280, "lineClusteredColumnComboChart",
                     "SIP Inflows vs NIFTY 50",
                     line_cfg("SIP_Monthly","Period",["SIP_Inflows_Cr","NIFTY50"],
                               colors=["#1a56db","#10b981"])),
        chart_visual(20,  412, 560, 260, "tableEx",
                     "Category Inflow Heatmap FY25",
                     {"dataRoles": [{"role":"Rows","items":[
                         {"type":"column","table":"Category_Inflows","column":"Category"},
                         {"type":"column","table":"Category_Inflows","column":"Month"},
                         {"type":"column","table":"Category_Inflows","column":"NetInflow_Cr"},
                     ]}]}),
        chart_visual(600, 412, 584, 260, "barChart",
                     "Top 5 Categories by Net Inflow",
                     bar_cfg("Category_Inflows","Category",["NetInflow_Cr"])),
        chart_visual(20,  688, 1164, 220, "lineChart",
                     "SIP YoY Growth vs SIP AUM",
                     line_cfg("SIP_Growth","Period",["SIP_AUM_LCr","YoY_Growth_Pct"],
                               colors=["#8b5cf6","#f59e0b"])),
        chart_visual(20,  924, 260, 60, "slicer",
                     "Category Filter",slicer_cfg("Category_Inflows","Category")),
    ]

    report = {
        "id": "bluestock-mf-analytics",
        "resourcePackages": [],
        "config": json.dumps({
            "version": "5.1.0",
            "themeCollection": {
                "baseTheme": {"name": "CY22SU10"},
                "customTheme": {
                    "name": "Bluestock Blue",
                    "dataColors": THEME_COLORS,
                    "background": "#f8fafc",
                    "foreground": "#0f172a",
                    "tableAccent": "#1a56db",
                },
            },
        }),
        "sections": [
            page("p1","Industry Overview",   1204, 760, p1_visuals),
            page("p2","Fund Performance",    1204, 1000, p2_visuals),
            page("p3","Investor Analytics",  1204, 760, p3_visuals),
            page("p4","SIP & Market Trends", 1204, 1000, p4_visuals),
        ],
    }
    return report

# ═════════════════════════════════════════════════════════════════════════════
# 4.  WRITE ALL pbi-tools SOURCE FILES
# ═════════════════════════════════════════════════════════════════════════════

def write_sources():
    clean()

    # ── model.bim ──────────────────────────────────────────────────────────────
    bim = build_model_bim()
    bim_path = ROOT / "Model" / "database.json"
    bim_path.parent.mkdir(parents=True, exist_ok=True)
    bim_path.write_text(json.dumps(bim, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"  ✓  Model/database.json ({len(bim['model']['tables'])} tables, "
          f"{sum(len(t.get('measures',[])) for t in bim['model']['tables'])} measures)")

    # ── Report/Layout ──────────────────────────────────────────────────────────
    layout = build_report_layout()
    layout_path = REPORT / "Layout"
    layout_path.write_text(json.dumps(layout, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"  ✓  Report/Layout ({len(layout['sections'])} pages, "
          f"{sum(len(p['visualContainers']) for p in layout['sections'])} visuals)")

    # ── Report/StaticResources ─────────────────────────────────────────────────
    (REPORT / "StaticResources" / "SharedResources" / "BaseThemes").mkdir(parents=True, exist_ok=True)

    # ── .pbi/localSettings.json ───────────────────────────────────────────────
    SETTINGS.mkdir(parents=True, exist_ok=True)
    (SETTINGS / "localSettings.json").write_text(
        json.dumps({"version":"1.0","settings":{}}, indent=2), encoding="utf-8")

    # ── Version ────────────────────────────────────────────────────────────────
    (ROOT / "Version").write_text("1.0", encoding="utf-8")

    # ── [Content_Types].xml ────────────────────────────────────────────────────
    (ROOT / "[Content_Types].xml").write_text(textwrap.dedent("""\
        <?xml version="1.0" encoding="utf-8"?>
        <Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
          <Default Extension="json" ContentType="application/json"/>
          <Default Extension="xml"  ContentType="application/xml"/>
          <Override PartName="/Report/Layout"
                    ContentType="application/json"/>
          <Override PartName="/Model/database.json"
                    ContentType="application/json"/>
        </Types>"""), encoding="utf-8")

    # ── SecurityBindings (empty required by pbi-tools) ─────────────────────────
    (ROOT / "SecurityBindings").write_bytes(b"")

    # ── Mashup / M query (empty — data is embedded via DATATABLE) ─────────────
    mashup_m = textwrap.dedent("""\
        section Section1;
        // Data is embedded directly in the model as calculated DAX tables.
        // No external data source connection required.
        """)
    mashup_path = MASHUP / "Package" / "Formulas" / "Section1.m"
    mashup_path.parent.mkdir(parents=True, exist_ok=True)
    mashup_path.write_text(mashup_m, encoding="utf-8")
    print(f"  ✓  All source files written to: {ROOT.resolve()}")

# ═════════════════════════════════════════════════════════════════════════════
# 5.  COMPILE WITH pbi-tools
# ═════════════════════════════════════════════════════════════════════════════

def find_pbitools():
    """Locate pbi-tools executable: dotnet global tool or standalone."""
    # Try dotnet global tool (cross-platform)
    for name in ["pbi-tools", "pbi-tools.exe"]:
        p = shutil.which(name)
        if p:
            return [p]
    # Try dotnet run approach
    if shutil.which("dotnet"):
        return ["dotnet", "pbi-tools"]
    return None

def compile_pbix():
    tool = find_pbitools()
    if tool is None:
        print("\n⚠  pbi-tools not found on PATH.")
        print("   Install it with:\n")
        print("     dotnet tool install -g pbi-tools")
        print("\n   Then re-run this script, OR compile manually:")
        print(f"     pbi-tools compile \"{ROOT.resolve()}\" -outPath \"{PBIX.resolve()}\" -overwrite\n")
        return False

    cmd = tool + ["compile", str(ROOT), "-outPath", str(PBIX), "-overwrite"]
    print(f"\n  Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode == 0:
        size_kb = PBIX.stat().st_size // 1024
        print(f"\n✅  Compiled: {PBIX.resolve()}  ({size_kb} KB)")
        return True
    else:
        print("\n❌  pbi-tools compile failed:")
        print(result.stdout[-2000:] if result.stdout else "")
        print(result.stderr[-2000:] if result.stderr else "")
        print(f"\n   Source files are in: {ROOT.resolve()}")
        print("   Try compiling manually:")
        print(f"     pbi-tools compile \"{ROOT}\" -outPath \"{PBIX}\" -overwrite")
        return False

# ═════════════════════════════════════════════════════════════════════════════
# 6.  MAIN
# ═════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("═"*66)
    print("  BLUESTOCK MF ANALYTICS — Power BI .pbix Builder")
    print("═"*66)
    print("\n[1/2] Generating pbi-tools source files...")
    write_sources()

    print("\n[2/2] Compiling .pbix with pbi-tools...")
    ok = compile_pbix()

    print("\n" + "═"*66)
    if ok:
        print("  DONE — open bluestock_mf_analytics.pbix in Power BI Desktop")
    else:
        print("  SOURCE FILES READY — install pbi-tools then compile")
        print("  Full install guide: https://pbi.tools/cli/installation.html")
    print("═"*66)

    # ── Summarise what was built ──────────────────────────────────────────────
    bim = build_model_bim()
    layout = build_report_layout()
    n_tables   = len(bim["model"]["tables"])
    n_measures = sum(len(t.get("measures",[])) for t in bim["model"]["tables"])
    n_rels     = len(bim["model"]["relationships"])
    n_pages    = len(layout["sections"])
    n_visuals  = sum(len(p["visualContainers"]) for p in layout["sections"])
    print(f"""
  📊  Data tables    : {n_tables}   (all embedded as DAX DATATABLE — no Excel needed)
  📐  Report pages   : {n_pages}
  📈  Visuals        : {n_visuals}  (cards, line, bar, scatter, donut, matrix, slicers)
  🎯  DAX measures   : {n_measures}
  🔀  Relationships  : {n_rels}
  📁  Source folder  : {ROOT.resolve()}
""")
