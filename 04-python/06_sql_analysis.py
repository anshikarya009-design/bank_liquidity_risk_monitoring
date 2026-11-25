
from pathlib import Path
import pandas as pd
import sqlite3

PROJECT_DIR = Path(__file__).resolve().parent
CLEAN_DIR = PROJECT_DIR / "data" / "cleaned"
REPORT_DIR = PROJECT_DIR / "reports"

REPORT_DIR.mkdir(parents=True, exist_ok=True)

csv_file = CLEAN_DIR / "clean_balance_sheet.csv"
db_file = REPORT_DIR / "liquidity_risk.db"

if not csv_file.exists():
    raise FileNotFoundError(
        f"Cleaned CSV not found: {csv_file}"
    )

df = pd.read_csv(csv_file)

# Load cleaned data into a SQLite database
with sqlite3.connect(db_file) as conn:
    df.to_sql(
        "balance_sheet",
        conn,
        if_exists="replace",
        index=False
    )

    print("\n1. LATEST RECORD FOR EACH ENTITY")

    query1 = """
    SELECT entity_id, report_date,
           lcr_proxy_pct,
           liquidity_surplus_proxy_gbp_m
    FROM (
        SELECT *,
               ROW_NUMBER() OVER (
                   PARTITION BY entity_id
                   ORDER BY report_date DESC
               ) AS rn
        FROM balance_sheet
    )
    WHERE rn = 1
    ORDER BY entity_id;
    """

    print(pd.read_sql_query(query1, conn).to_string(index=False))

    print("\n2. RECORDS BELOW THE ILLUSTRATIVE 120% THRESHOLD")

    query2 = """
    SELECT entity_id, report_date, lcr_proxy_pct
    FROM balance_sheet
    WHERE lcr_proxy_pct < 120
    ORDER BY lcr_proxy_pct ASC;
    """

    print(pd.read_sql_query(query2, conn).to_string(index=False))

    print("\n3. MONTHLY AVERAGE LIQUIDITY PROXY")

    query3 = """
    SELECT report_date,
           ROUND(AVG(lcr_proxy_pct), 2) AS avg_lcr_proxy_pct
    FROM balance_sheet
    GROUP BY report_date
    ORDER BY report_date;
    """

    print(pd.read_sql_query(query3, conn).to_string(index=False))

    # Save query results for documentation
    pd.read_sql_query(query1, conn).to_csv(
        REPORT_DIR / "sql_latest_entity_summary.csv",
        index=False
    )

print("\nSQL analysis completed.")
print("Database saved at:", db_file)
