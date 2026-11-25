# Bank Liquidity Risk Monitoring & Early Warning System

An end-to-end data analytics portfolio project that simulates a simplified bank liquidity monitoring workflow using **Python, SQL, PostgreSQL, Excel and Power BI**.

The project demonstrates data inspection, data-quality validation, cleaning, liquidity proxy calculations, rule-based classification, SQL analysis and interactive reporting.

> **Scope and data disclaimer:** This is an independent portfolio simulation using synthetic data. It does not use JPMorgan Chase or any other bank's internal data, systems, policies or risk limits. The liquidity proxy and thresholds are illustrative and are not an official regulatory Liquidity Coverage Ratio (LCR) calculation.

## Business problem

A risk analyst needs a repeatable way to review balance-sheet information, identify incomplete or invalid records, monitor a simplified liquidity indicator and communicate exceptions.

This project uses two key inputs:
- High-Quality Liquid Assets (HQLA)
- 30-day net cash outflows

## Objectives

1. Inspect and profile synthetic balance-sheet and cash-flow data.
2. Identify missing, duplicate and invalid values.
3. Preserve source exceptions and document them in a data-quality log.
4. Calculate a simplified liquidity coverage proxy.
5. Apply transparent, illustrative risk categories.
6. Query and summarise records in PostgreSQL.
7. Present KPIs, trends, classifications and record-level detail in Power BI.

## Technology stack

| Technology | Use |
|---|---|
| Python, Pandas | Data profiling, cleaning, calculations and charts |
| SQL | Validation, calculations, classification and summaries |
| PostgreSQL, pgAdmin | Relational storage and query execution |
| Excel | Source-data review |
| Power BI | Interactive reporting and dashboard |

## Workflow

```text
Synthetic Excel workbooks
        |
        v
Python inspection and profiling
        |
        v
Cleaning + data-quality log
        |
        +----------------------+
        |                      |
        v                      v
PostgreSQL + SQL          Python analysis
        |                      |
        +-----------+----------+
                    v
             Power BI dashboard
```

## Liquidity coverage proxy

`Liquidity Coverage Proxy (%) = (HQLA / 30-day Net Cash Outflows) * 100`

The proxy is calculated only when HQLA is present and non-negative and net cash outflows are positive.

### Illustrative project classifications

| Proxy value | Project status |
|---|---|
| Below 100% | HIGH RISK |
| 100% to below 120% | WARNING |
| 120% or above | NORMAL |
| Missing or invalid inputs | DATA REVIEW REQUIRED |

These are project assumptions for demonstration only. They are not JPMorgan Chase thresholds, internal bank policy or regulatory guidance.

## Repository structure

The repository uses the following numbered folders:

```text
bank_liquidity_risk_monitoring/
├── 02-dashboard/
│   └── Bank_Liquidity_Risk_Dashboard.pbix
├── 03-data/
│   ├── bank_liquidity_risk_final.xlsx
│   ├── bank_liquidity_risk_raw_data.xlsx
│   └── cleaned/
│       ├── clean_balance_sheet.csv
│       ├── clean_cash_flows.csv
│       └── data_quality_log.csv
├── 04-python/
│   ├── 01_load_and_inspect.py
│   ├── 02_profile_data.py
│   ├── 03_clean_data.py
│   ├── 04_liquidity_risk_analysis.py
│   └── 05_visualize_risk.py
├── 05-sql/
│   ├── 01_data_quality_checks.sql
│   ├── 02_liquidity_proxy_calculation.sql
│   ├── 03_risk_classification.sql
│   ├── 04_latest_entity_status.sql
│   ├── 05_monthly_liquidity_trends.sql
│   ├── 06_early_warning_signals.sql
│   ├── 07_dataset_summary.sql
│   └── 08_latest_risk_summary.sql
└── 06-reports/
    ├── liquidity_risk_analysis.csv
    ├── latest_entity_risk_summary.csv
    └── charts/
```

## How to run

### Prerequisites
- Python 3
- PostgreSQL (and pgAdmin, optional)
- Power BI Desktop
- Python packages: `pandas`, `openpyxl`, `matplotlib`

### 1. Clone the repository

```bash
git clone https://github.com/anshikarya009-design/bank_liquidity_risk_monitoring.git
cd bank_liquidity_risk_monitoring
```

### 2. Install Python dependencies

```bash
python -m pip install pandas openpyxl matplotlib
```

### 3. Run Python scripts in order

Run these commands from the repository root:

```bash
python 04-python/01_load_and_inspect.py
python 04-python/02_profile_data.py
python 04-python/03_clean_data.py
python 04-python/04_liquidity_risk_analysis.py
python 04-python/05_visualize_risk.py
```

The scripts read the source workbook from `03-data/`, write cleaned files to `03-data/cleaned/`, and write analysis outputs and charts to `06-reports/`.

### 4. PostgreSQL and SQL

Create a PostgreSQL database, import `03-data/cleaned/clean_balance_sheet.csv` into `public.balance_sheet`, then run the eight query files in `05-sql/`. Confirm that the imported column names and data types match the SQL queries. Use your own local database connection settings; do not commit passwords or credentials.

### 5. Power BI

Open `02-dashboard/Bank_Liquidity_Risk_Dashboard.pbix` in Power BI Desktop. If it connects to a local PostgreSQL database, update the data-source settings to your own database and refresh the report.

## Current dataset snapshot

The previously saved report snapshot contains 36 balance-sheet records: 34 Normal and 2 Data Review Required. It shows 0 High Risk and 0 Warning records. Re-run the Python workflow after any data or logic changes before treating these figures as current.

## Dashboard

The Power BI file is stored in `02-dashboard/`. Add an exported dashboard screenshot to the same folder as `dashboard_preview.png` and then uncomment the image below:

<!-- ![Power BI dashboard preview](02-dashboard/dashboard_preview.png) -->

## Key learning outcomes

- Built a multi-step data analytics workflow using Python and SQL.
- Profiled structured financial-style data and documented data-quality exceptions.
- Used PostgreSQL for repeatable analytical queries.
- Created calculated indicators and illustrative rule-based classifications.
- Designed a Power BI report with KPIs, trends, status distribution and filters.
- Translated a business monitoring question into measurable analytical outputs.

## Limitations and future improvements

- The dataset is synthetic and small.
- The proxy is simplified and is not a complete regulatory LCR methodology.
- Thresholds are hard-coded project assumptions.
- Future work could add automated tests, configurable thresholds, more entities, additional liquidity indicators and scheduled refresh.

## Disclaimer

This project is for educational and portfolio demonstration purposes only. All data is synthetic. The proxy, thresholds and early-warning rules are simplified examples and must not be interpreted as official regulatory calculations or any financial institution's internal methodology or actual liquidity position.

## Author

**Anshika Arya**  
Aspiring Data Analyst | Financial Risk Analytics | Python | SQL | PostgreSQL | Power BI

- GitHub: https://github.com/anshikarya009-design
- LinkedIn: Add your LinkedIn profile URL
