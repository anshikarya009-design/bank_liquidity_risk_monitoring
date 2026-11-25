from pathlib import Path
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parent
CLEAN_DIR = PROJECT_DIR.parent / "03-data" / "cleaned"
OUTPUT_DIR = PROJECT_DIR.parent / "06-reports"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

bs_file = CLEAN_DIR / "clean_balance_sheet.csv"
if not bs_file.exists():
    raise FileNotFoundError(
        f"Cleaned balance sheet not found: {bs_file}. "
        "Run 03_clean_data.py first."
    )

df = pd.read_csv(bs_file, parse_dates=["report_date"])

required_columns = [
    "report_date", "entity_id", "hqla_gbp_m",
    "net_cash_outflows_30d_gbp_m", "wholesale_funding_gbp_m",
    "total_liabilities_gbp_m",
]
missing_columns = [col for col in required_columns if col not in df.columns]
if missing_columns:
    raise ValueError(f"Missing required columns: {missing_columns}")

# Validity checks prevent negative HQLA or non-positive outflows
# from producing misleading ratios.
valid_proxy_inputs = (
    df["hqla_gbp_m"].notna()
    & df["hqla_gbp_m"].ge(0)
    & df["net_cash_outflows_30d_gbp_m"].notna()
    & df["net_cash_outflows_30d_gbp_m"].gt(0)
)
df["lcr_proxy_pct"] = float("nan")
df.loc[valid_proxy_inputs, "lcr_proxy_pct"] = (
    df.loc[valid_proxy_inputs, "hqla_gbp_m"]
    / df.loc[valid_proxy_inputs, "net_cash_outflows_30d_gbp_m"]
    * 100
)

df["liquidity_surplus_proxy_gbp_m"] = (
    df["hqla_gbp_m"] - df["net_cash_outflows_30d_gbp_m"]
)
df["wholesale_funding_share_pct"] = (
    df["wholesale_funding_gbp_m"]
    .div(df["total_liabilities_gbp_m"].where(df["total_liabilities_gbp_m"].gt(0)))
    * 100
)

# Project-only illustrative thresholds, not regulatory or bank limits.
df["liquidity_status"] = "NORMAL"
df.loc[df["lcr_proxy_pct"].lt(120) & df["lcr_proxy_pct"].ge(100), "liquidity_status"] = "WARNING"
df.loc[df["lcr_proxy_pct"].lt(100), "liquidity_status"] = "HIGH RISK"
df.loc[~valid_proxy_inputs, "liquidity_status"] = "DATA REVIEW REQUIRED"

df = df.sort_values(["entity_id", "report_date"]).copy()
df["previous_lcr_proxy_pct"] = df.groupby("entity_id")["lcr_proxy_pct"].shift(1)
df["lcr_change_percentage_points"] = (
    df["lcr_proxy_pct"] - df["previous_lcr_proxy_pct"]
)

print("\nLATEST LIQUIDITY POSITION BY ENTITY")
latest = (
    df.sort_values("report_date")
    .groupby("entity_id", group_keys=False)
    .tail(1)
)
print(latest[[
    "report_date", "entity_id", "lcr_proxy_pct",
    "liquidity_surplus_proxy_gbp_m",
    "wholesale_funding_share_pct", "liquidity_status"
]].to_string(index=False))

print("\nRISK STATUS COUNTS")
print(df["liquidity_status"].value_counts(dropna=False))

print("\nRECORDS REQUIRING REVIEW OR ATTENTION")
attention = df[df["liquidity_status"] != "NORMAL"]
print(attention[[
    "report_date", "entity_id", "lcr_proxy_pct", "liquidity_status"
]].to_string(index=False))

df.to_csv(OUTPUT_DIR / "liquidity_risk_analysis.csv", index=False)
latest.to_csv(OUTPUT_DIR / "latest_entity_risk_summary.csv", index=False)

print("\nReports saved in:", OUTPUT_DIR)
print("LIQUIDITY RISK ANALYSIS COMPLETED")
