
from pathlib import Path
import pandas as pd

# 1. Locate cleaned data
PROJECT_DIR = Path(__file__).resolve().parent
CLEAN_DIR = PROJECT_DIR / "data" / "cleaned"
OUTPUT_DIR = PROJECT_DIR / "reports"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

bs_file = CLEAN_DIR / "clean_balance_sheet.csv"

if not bs_file.exists():
    raise FileNotFoundError(
        "Cleaned balance sheet not found. "
        "Run 03_clean_data.py first."
    )

df = pd.read_csv(bs_file, parse_dates=["report_date"])

# 2. Check whether required columns exist
required_columns = [
    "report_date",
    "entity_id",
    "hqla_gbp_m",
    "net_cash_outflows_30d_gbp_m",
    "wholesale_funding_gbp_m",
    "total_liabilities_gbp_m",
]

missing_columns = [
    col for col in required_columns if col not in df.columns
]

if missing_columns:
    raise ValueError(f"Missing columns: {missing_columns}")

# 3. Calculate liquidity indicators
df["lcr_proxy_pct"] = (
    df["hqla_gbp_m"]
    / df["net_cash_outflows_30d_gbp_m"]
    * 100
)

df.loc[
    df["net_cash_outflows_30d_gbp_m"] <= 0,
    "lcr_proxy_pct"
] = float("nan")

df["liquidity_surplus_proxy_gbp_m"] = (
    df["hqla_gbp_m"]
    - df["net_cash_outflows_30d_gbp_m"]
)

df["wholesale_funding_share_pct"] = (
    df["wholesale_funding_gbp_m"]
    / df["total_liabilities_gbp_m"]
    * 100
)

# 4. Apply illustrative warning thresholds
# These are project assumptions, NOT JPMorgan limits.
def classify_liquidity(row):
    if pd.isna(row["lcr_proxy_pct"]):
        return "DATA REVIEW REQUIRED"
    elif row["lcr_proxy_pct"] < 100:
        return "HIGH RISK"
    elif row["lcr_proxy_pct"] < 120:
        return "WARNING"
    else:
        return "NORMAL"

df["liquidity_status"] = df.apply(
    classify_liquidity, axis=1
)

# Flag missing key inputs separately
missing_inputs = (
    df["hqla_gbp_m"].isna()
    | df["net_cash_outflows_30d_gbp_m"].isna()
)

df.loc[missing_inputs, "liquidity_status"] = (
    "DATA REVIEW REQUIRED"
)

# 5. Sort records chronologically
df = df.sort_values(["entity_id", "report_date"])

# 6. Calculate month-to-month liquidity proxy movement
df["previous_lcr_proxy_pct"] = (
    df.groupby("entity_id")["lcr_proxy_pct"].shift(1)
)

df["lcr_change_percentage_points"] = (
    df["lcr_proxy_pct"] - df["previous_lcr_proxy_pct"]
)

# 7. Print key results
print("\nLATEST LIQUIDITY POSITION BY ENTITY")
latest = (
    df.sort_values("report_date")
    .groupby("entity_id")
    .tail(1)
)

print(
    latest[
        [
            "report_date",
            "entity_id",
            "lcr_proxy_pct",
            "liquidity_surplus_proxy_gbp_m",
            "wholesale_funding_share_pct",
            "liquidity_status",
        ]
    ].to_string(index=False)
)

print("\nRISK STATUS COUNTS")
print(df["liquidity_status"].value_counts())

print("\nRECORDS REQUIRING REVIEW")
review = df[
    df["liquidity_status"] != "NORMAL"
]

print(
    review[
        [
            "report_date",
            "entity_id",
            "lcr_proxy_pct",
            "liquidity_status",
        ]
    ].to_string(index=False)
)

# 8. Export results
df.to_csv(
    OUTPUT_DIR / "liquidity_risk_analysis.csv",
    index=False
)

latest.to_csv(
    OUTPUT_DIR / "latest_entity_risk_summary.csv",
    index=False
)

print("\nReports saved in:", OUTPUT_DIR)
print("LIQUIDITY RISK ANALYSIS COMPLETED")
