from pathlib import Path
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parent
DATA_DIR = PROJECT_DIR.parent / "03-data"
OUTPUT_DIR = DATA_DIR / "cleaned"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

file_path = DATA_DIR / "bank_liquidity_risk_final.xlsx"
if not file_path.exists():
    raise FileNotFoundError(
        f"Source workbook not found: {file_path}. "
        "Keep it inside the repository's 03-data folder."
    )

balance_sheet = pd.read_excel(file_path, sheet_name="Raw_Balance_Sheet")
cash_flows = pd.read_excel(file_path, sheet_name="Raw_Cash_Flows")

print("Original balance sheet shape:", balance_sheet.shape)
print("Original cash flows shape:", cash_flows.shape)

# Standardise text fields without changing numeric source values.
for df in (balance_sheet, cash_flows):
    if "currency" in df.columns:
        df["currency"] = df["currency"].astype("string").str.strip().str.upper()

# Remove exact duplicates only; retain other exceptions for investigation.
bs_duplicates = int(balance_sheet.duplicated().sum())
cf_duplicates = int(cash_flows.duplicated().sum())
balance_sheet = balance_sheet.drop_duplicates().copy()
cash_flows = cash_flows.drop_duplicates().copy()

issues = []

def add_missing_value_issues(df, dataset_name):
    for column in df.columns:
        count = int(df[column].isna().sum())
        if count:
            issues.append({
                "dataset": dataset_name,
                "issue": "Missing values",
                "column": column,
                "count": count,
                "action": "Retained as missing; investigate source"
            })

add_missing_value_issues(balance_sheet, "Balance Sheet")
add_missing_value_issues(cash_flows, "Cash Flows")

if bs_duplicates:
    issues.append({
        "dataset": "Balance Sheet", "issue": "Exact duplicate rows",
        "column": "All columns", "count": bs_duplicates,
        "action": "Removed exact duplicates from cleaned copy"
    })
if cf_duplicates:
    issues.append({
        "dataset": "Cash Flows", "issue": "Exact duplicate rows",
        "column": "All columns", "count": cf_duplicates,
        "action": "Removed exact duplicates from cleaned copy"
    })

# Build one unambiguous quality status per row.
balance_sheet["data_quality_flag"] = "OK"
checks = [
    (balance_sheet["hqla_gbp_m"].isna(), "MISSING_HQLA"),
    (balance_sheet["hqla_gbp_m"].lt(0), "NEGATIVE_HQLA"),
    (balance_sheet["net_cash_outflows_30d_gbp_m"].isna(), "MISSING_OUTFLOWS"),
    (balance_sheet["net_cash_outflows_30d_gbp_m"].le(0), "NON_POSITIVE_OUTFLOWS"),
]
for mask, flag in checks:
    balance_sheet.loc[mask, "data_quality_flag"] = flag
    count = int(mask.sum())
    if count:
        issues.append({
            "dataset": "Balance Sheet",
            "issue": flag,
            "column": "hqla_gbp_m" if "HQLA" in flag else "net_cash_outflows_30d_gbp_m",
            "count": count,
            "action": "Flagged for investigation; source value not changed"
        })

cash_flows["data_quality_flag"] = "OK"
cash_flows.loc[cash_flows["cash_outflows_gbp_m"].isna(), "data_quality_flag"] = (
    "MISSING_CASH_OUTFLOWS"
)

# Calculate the proxy only when both inputs are valid.
valid_proxy_inputs = (
    balance_sheet["hqla_gbp_m"].notna()
    & balance_sheet["hqla_gbp_m"].ge(0)
    & balance_sheet["net_cash_outflows_30d_gbp_m"].notna()
    & balance_sheet["net_cash_outflows_30d_gbp_m"].gt(0)
)
balance_sheet["lcr_proxy_pct"] = pd.NA
balance_sheet.loc[valid_proxy_inputs, "lcr_proxy_pct"] = (
    balance_sheet.loc[valid_proxy_inputs, "hqla_gbp_m"]
    / balance_sheet.loc[valid_proxy_inputs, "net_cash_outflows_30d_gbp_m"]
    * 100
)

balance_sheet["liquidity_surplus_proxy_gbp_m"] = (
    balance_sheet["hqla_gbp_m"] - balance_sheet["net_cash_outflows_30d_gbp_m"]
)

balance_sheet["wholesale_funding_share_pct"] = (
    balance_sheet["wholesale_funding_gbp_m"]
    .div(balance_sheet["total_liabilities_gbp_m"].where(
        balance_sheet["total_liabilities_gbp_m"].gt(0)
    ))
    * 100
)

cash_flows["calculated_net_cash_flow_gbp_m"] = (
    cash_flows["cash_inflows_gbp_m"] - cash_flows["cash_outflows_gbp_m"]
)
cash_flows["reconciliation_difference_gbp_m"] = (
    cash_flows["net_cash_flow_gbp_m"] - cash_flows["calculated_net_cash_flow_gbp_m"]
)

balance_sheet.to_csv(OUTPUT_DIR / "clean_balance_sheet.csv", index=False)
cash_flows.to_csv(OUTPUT_DIR / "clean_cash_flows.csv", index=False)
pd.DataFrame(issues, columns=[
    "dataset", "issue", "column", "count", "action"
]).to_csv(OUTPUT_DIR / "data_quality_log.csv", index=False)

print("\nCleaned files saved to:", OUTPUT_DIR)
print("Clean balance sheet shape:", balance_sheet.shape)
print("Clean cash flows shape:", cash_flows.shape)
print("\nData quality log:")
print(pd.DataFrame(issues).to_string(index=False))
print("\nDATA CLEANING COMPLETED")
