
from pathlib import Path
import pandas as pd

# 1. Set up file paths
PROJECT_DIR = Path(__file__).resolve().parent
DATA_DIR = PROJECT_DIR / "data"
OUTPUT_DIR = DATA_DIR / "cleaned"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

file_path = DATA_DIR / "bank_liquidity_risk_final.xlsx"

# 2. Load the original data
balance_sheet = pd.read_excel(
    file_path, sheet_name="Raw_Balance_Sheet"
)

cash_flows = pd.read_excel(
    file_path, sheet_name="Raw_Cash_Flows"
)

print("Original balance sheet shape:", balance_sheet.shape)
print("Original cash flows shape:", cash_flows.shape)

# 3. Standardise text and currency fields
for df in [balance_sheet, cash_flows]:
    df["currency"] = (
        df["currency"]
        .astype("string")
        .str.strip()
        .str.upper()
    )

# 4. Remove exact duplicate rows only
bs_duplicates = balance_sheet.duplicated().sum()
cf_duplicates = cash_flows.duplicated().sum()

balance_sheet = balance_sheet.drop_duplicates().copy()
cash_flows = cash_flows.drop_duplicates().copy()

print("\nExact duplicates removed:")
print("Balance sheet:", bs_duplicates)
print("Cash flows:", cf_duplicates)

# 5. Create a data quality log
issues = []

# Missing values
for column in balance_sheet.columns:
    count = balance_sheet[column].isna().sum()
    if count > 0:
        issues.append({
            "dataset": "Balance Sheet",
            "issue": "Missing values",
            "column": column,
            "count": int(count),
            "action": "Retained as missing; investigate source"
        })

for column in cash_flows.columns:
    count = cash_flows[column].isna().sum()
    if count > 0:
        issues.append({
            "dataset": "Cash Flows",
            "issue": "Missing values",
            "column": column,
            "count": int(count),
            "action": "Retained as missing; investigate source"
        })

# Duplicate rows
if bs_duplicates:
    issues.append({
        "dataset": "Balance Sheet",
        "issue": "Exact duplicate rows",
        "column": "All columns",
        "count": int(bs_duplicates),
        "action": "Removed exact duplicates from cleaned copy"
    })

if cf_duplicates:
    issues.append({
        "dataset": "Cash Flows",
        "issue": "Exact duplicate rows",
        "column": "All columns",
        "count": int(cf_duplicates),
        "action": "Removed exact duplicates from cleaned copy"
    })

# Negative outflows are flagged, not automatically changed
negative_outflows = (
    balance_sheet["net_cash_outflows_30d_gbp_m"] < 0
).sum()

if negative_outflows:
    issues.append({
        "dataset": "Balance Sheet",
        "issue": "Negative 30-day net cash outflow",
        "column": "net_cash_outflows_30d_gbp_m",
        "count": int(negative_outflows),
        "action": "Flagged for investigation; value not changed"
    })

# 6. Add data quality flags
balance_sheet["data_quality_flag"] = "OK"

balance_sheet.loc[
    balance_sheet["hqla_gbp_m"].isna(),
    "data_quality_flag"
] = "MISSING_HQLA"

balance_sheet.loc[
    balance_sheet["net_cash_outflows_30d_gbp_m"].isna(),
    "data_quality_flag"
] = "MISSING_OUTFLOWS"

balance_sheet.loc[
    balance_sheet["net_cash_outflows_30d_gbp_m"] < 0,
    "data_quality_flag"
] = "NEGATIVE_OUTFLOWS"

cash_flows["data_quality_flag"] = "OK"

cash_flows.loc[
    cash_flows["cash_outflows_gbp_m"].isna(),
    "data_quality_flag"
] = "MISSING_CASH_OUTFLOWS"

# 7. Calculate a simplified liquidity proxy
# This is an illustrative project metric, not regulatory LCR.
balance_sheet["lcr_proxy_pct"] = (
    balance_sheet["hqla_gbp_m"]
    / balance_sheet["net_cash_outflows_30d_gbp_m"]
    * 100
)

balance_sheet.loc[
    balance_sheet["net_cash_outflows_30d_gbp_m"] <= 0,
    "lcr_proxy_pct"
] = pd.NA

balance_sheet["liquidity_surplus_proxy_gbp_m"] = (
    balance_sheet["hqla_gbp_m"]
    - balance_sheet["net_cash_outflows_30d_gbp_m"]
)

balance_sheet["wholesale_funding_share_pct"] = (
    balance_sheet["wholesale_funding_gbp_m"]
    / balance_sheet["total_liabilities_gbp_m"]
    * 100
)

# 8. Reconciliation check for cash flows
cash_flows["calculated_net_cash_flow_gbp_m"] = (
    cash_flows["cash_inflows_gbp_m"]
    - cash_flows["cash_outflows_gbp_m"]
)

cash_flows["reconciliation_difference_gbp_m"] = (
    cash_flows["net_cash_flow_gbp_m"]
    - cash_flows["calculated_net_cash_flow_gbp_m"]
)

# 9. Export cleaned data and log
balance_sheet.to_csv(
    OUTPUT_DIR / "clean_balance_sheet.csv", index=False
)

cash_flows.to_csv(
    OUTPUT_DIR / "clean_cash_flows.csv", index=False
)

pd.DataFrame(issues).to_csv(
    OUTPUT_DIR / "data_quality_log.csv", index=False
)

print("\nCleaned files saved to:", OUTPUT_DIR)
print("Clean balance sheet shape:", balance_sheet.shape)
print("Clean cash flows shape:", cash_flows.shape)
print("\nData quality log:")
print(pd.DataFrame(issues).to_string(index=False))
print("\nDATA CLEANING COMPLETED")
