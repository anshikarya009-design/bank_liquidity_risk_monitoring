# Bank Liquidity Risk Monitoring & Early Warning System

An end-to-end data analytics portfolio project that simulates a bank
liquidity risk monitoring workflow using **Python, SQL, PostgreSQL,
Excel and Power BI**.

The project demonstrates how balance-sheet data can be inspected,
cleaned, analysed and transformed into liquidity indicators, rule-based
risk classifications and an interactive monitoring dashboard.

> **Data and scope disclaimer:** This is an independent portfolio
> simulation built with synthetic data. It does not use JPMorgan Chase
> or any other bank's internal data, systems, policies or risk limits.
> The liquidity proxy and thresholds in this project are illustrative
> and are not an official regulatory Liquidity Coverage Ratio (LCR)
> calculation or regulatory guidance.

------------------------------------------------------------------------

## 1. Project Overview

Liquidity risk is the risk that a financial institution may be unable to
meet its cash obligations when they fall due without incurring
unacceptable losses.

This project builds a simplified monitoring workflow around two
balance-sheet inputs:

-   High-Quality Liquid Assets (HQLA)
-   Net cash outflows over a 30-day period

A liquidity coverage proxy is calculated to support basic monitoring and
rule-based classification. Data-quality checks are also included so that
records with missing or invalid inputs can be flagged for review rather
than silently treated as normal.

### Business objective

Build a repeatable analytical workflow that can:

1.  Inspect and profile synthetic balance-sheet data.
2.  Identify missing, invalid or inconsistent values.
3.  Clean and prepare data for analysis.
4.  Calculate a liquidity coverage proxy.
5.  Classify records using clearly labelled illustrative thresholds.
6.  Query and summarise results using PostgreSQL.
7.  Present key indicators and record-level details in Power BI.

------------------------------------------------------------------------

## 2. Technology Stack

  -----------------------------------------------------------------------
  Tool                                Purpose
  ----------------------------------- -----------------------------------
  Python                              Data inspection, profiling,
                                      cleaning, analysis and
                                      visualisation

  Pandas                              Tabular data processing

  SQL                                 Data-quality checks, calculations,
                                      classification and summaries

  PostgreSQL                          Relational database for structured
                                      analysis

  pgAdmin                             Database administration and query
                                      execution

  Microsoft Excel                     Initial data review and
                                      data-quality inspection

  Power BI                            Interactive dashboard and reporting
  -----------------------------------------------------------------------

------------------------------------------------------------------------

## 3. Project Workflow

``` text
Synthetic Source Data
        |
        v
Excel Review and Data Inspection
        |
        v
Python: Profiling and Cleaning
        |
        +------> Data Quality Log
        |
        v
Cleaned CSV Outputs
        |
        +----------------------+
        |                      |
        v                      v
PostgreSQL Database       Python Analysis
        |                      |
        v                      v
SQL Risk Queries          Analysis Reports and Charts
        |                      |
        +-----------+----------+
                    |
                    v
             Power BI Dashboard
```

------------------------------------------------------------------------

## 4. Liquidity Coverage Proxy

The project calculates an illustrative liquidity coverage proxy:

\[ `\text{Liquidity Coverage Proxy (\%)}`{=tex} =
`\frac{\text{HQLA}}{\text{30-day Net Cash Outflows}}`{=tex}
`\times 100`{=tex} \]

Where:

-   **HQLA** represents the synthetic high-quality liquid assets amount.
-   **30-day net cash outflows** represents the synthetic net cash
    outflows over 30 days.

### Illustrative classification rules

  Liquidity Coverage Proxy   Project classification
  -------------------------- ------------------------
  Below 100%                 HIGH RISK
  100% to below 120%         WARNING
  120% or above              NORMAL
  Missing or invalid input   DATA REVIEW REQUIRED

These cut-offs are used only to demonstrate rule-based classification in
this portfolio project. They must not be interpreted as JPMorgan Chase
thresholds, internal bank policy, or a complete regulatory LCR
methodology.

Records with missing or invalid inputs, including non-positive outflows
or negative HQLA, should be reviewed rather than assigned a misleading
ratio.

------------------------------------------------------------------------

## 5. Data Quality and Analysis

The workflow uses Python scripts to inspect, profile, clean and analyse
the synthetic data. Outputs include cleaned datasets, a data-quality
log, liquidity analysis results and chart files.

The SQL analysis is organised into separate query files for tasks such
as:

-   Data-quality checks
-   Liquidity proxy calculation
-   Risk classification
-   Latest entity status
-   Monthly liquidity trends
-   Early-warning signals
-   Dataset summaries
-   Latest risk summary

The Power BI report combines summary KPIs, trend analysis, risk-status
distribution, record-level details and date/entity filters.

------------------------------------------------------------------------

## 6. Dashboard Preview

Add your exported Power BI screenshot to the `dashboard` folder using
the filename `dashboard_preview.png`.

Once the image is uploaded, this section will display it on GitHub:

![Bank Liquidity Risk Monitoring
Dashboard](dashboard/dashboard_preview.png)

**Dashboard components:**

-   High-risk record count
-   Warning record count
-   Records requiring data review
-   Total records
-   Average liquidity coverage proxy
-   Monthly liquidity proxy trend
-   Risk-status distribution
-   Detailed liquidity risk records
-   Reporting-date and entity filters

> Dashboard values are based on the synthetic dataset and may change if
> the data or calculation logic is updated.

------------------------------------------------------------------------

## 7. Current Project Snapshot

The current dashboard snapshot shows:

  Indicator                         Result
  ------------------------------- --------
  Total records                         36
  Normal records                        34
  Records requiring data review          2
  High-risk records                      0
  Warning records                        0

The two records requiring review are retained as data-quality
exceptions. The absence of high-risk or warning classifications reflects
the current synthetic dataset and the illustrative classification rules;
it is not evidence about any real bank's liquidity position.

------------------------------------------------------------------------

## 8. Repository Structure

The structure below is a recommended layout. Update folder names or
paths if your local repository uses a different arrangement.

``` text
bank-liquidity-risk-monitoring/
│
├── README.md
│
├── dashboard/
│   ├── Bank_Liquidity_Risk_Dashboard.pbix
│   └── dashboard_preview.png
│
├── data/
│   ├── raw/
│   └── cleaned/
│       ├── clean_balance_sheet.csv
│       ├── clean_cash_flows.csv
│       └── data_quality_log.csv
│
├── python/
│   ├── 01_load_and_inspect.py
│   ├── 02_profile_data.py
│   ├── 03_clean_data.py
│   ├── 04_liquidity_risk_analysis.py
│   └── 05_visualize_risk.py
│
├── sql/
│   ├── 01_data_quality_checks.sql
│   ├── 02_liquidity_proxy_calculation.sql
│   ├── 03_risk_classification.sql
│   ├── 04_latest_entity_status.sql
│   ├── 05_monthly_liquidity_trends.sql
│   ├── 06_early_warning_signals.sql
│   ├── 07_dataset_summary.sql
│   └── 08_latest_risk_summary.sql
│
└── reports/
    ├── liquidity_risk_analysis.csv
    ├── latest_entity_risk_summary.csv
    └── charts/
```

Only include files and folders that are actually present in your
repository. Do not upload database credentials, local configuration
files, temporary files or unrelated personal documents.

------------------------------------------------------------------------

## 9. How to Run the Project

The following is a general execution sequence. Adjust paths and
filenames to match the repository.

### Prerequisites

-   Python 3
-   PostgreSQL
-   pgAdmin (optional, for a graphical database interface)
-   Microsoft Power BI Desktop
-   Python packages used by the scripts, such as `pandas` and
    `matplotlib`

### Step 1: Clone the repository

``` bash
git clone https://github.com/<your-username>/bank-liquidity-risk-monitoring.git
cd bank-liquidity-risk-monitoring
```

Replace `<your-username>` with your GitHub username.

### Step 2: Install Python dependencies

If a `requirements.txt` file is provided:

``` bash
pip install -r requirements.txt
```

If the repository does not contain a requirements file, install the
packages imported by the scripts. For example:

``` bash
pip install pandas matplotlib openpyxl
```

### Step 3: Run the Python workflow

Run the scripts in sequence, after checking their input and output
paths:

``` bash
python python/01_load_and_inspect.py
python python/02_profile_data.py
python python/03_clean_data.py
python python/04_liquidity_risk_analysis.py
python python/05_visualize_risk.py
```

The scripts may require source data files in the expected `data`
directory. Check the paths at the top of each script before running them
on another computer.

### Step 4: Set up PostgreSQL

1.  Create a PostgreSQL database.
2.  Import the cleaned balance-sheet data into the expected table.
3.  Open the SQL files in pgAdmin or another SQL client.
4.  Execute the queries in sequence, checking table and column names
    against your database schema.

The original local database connection settings are not included in this
repository. Configure your own local connection securely.

### Step 5: Open the Power BI dashboard

Open `dashboard/Bank_Liquidity_Risk_Dashboard.pbix` in Power BI Desktop.

If the report uses a PostgreSQL connection, update the data-source
connection to your own local database and refresh the data.

------------------------------------------------------------------------

## 10. Key Learning Outcomes

Through this project, I practised:

-   Building an end-to-end data analytics workflow.
-   Profiling and cleaning structured financial-style data.
-   Creating data-quality checks and exception logs.
-   Writing SQL queries for risk classification and reporting.
-   Working with PostgreSQL tables and analytical queries.
-   Developing calculated columns, measures, KPI cards, charts and
    slicers in Power BI.
-   Translating a business problem into measurable indicators and an
    interactive report.

------------------------------------------------------------------------

## 11. Limitations and Future Improvements

This is a simplified portfolio simulation. Potential future enhancements
include:

-   Adding more entities and longer reporting histories.
-   Building more robust validation and exception-handling tests.
-   Adding configurable thresholds rather than hard-coded illustrative
    cut-offs.
-   Comparing period-over-period liquidity movements.
-   Adding automated data refresh and scheduled reporting.
-   Introducing unit tests and a reproducible dependency file.
-   Extending the analysis with additional liquidity and funding
    indicators.

------------------------------------------------------------------------

## 12. Disclaimer

This project is intended solely for educational and portfolio
demonstration purposes. All data is synthetic. The liquidity coverage
proxy, classification thresholds and early-warning rules are simplified
examples created for this project. They are not official regulatory
calculations, financial advice, or representations of any financial
institution's internal methodology, risk appetite or liquidity position.

------------------------------------------------------------------------

## Author

**\[Your Name\]**

Aspiring Data Analyst \| Financial Risk Analytics \| Python \| SQL \|
PostgreSQL \| Power BI

-   GitHub: \[Add your GitHub profile URL\]
-   LinkedIn: \[Add your LinkedIn profile URL\]
