from pathlib import Path
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parent
DATA_DIR = PROJECT_DIR.parent / "03-data"
file_path = DATA_DIR / "bank_liquidity_risk_final.xlsx"

if not file_path.exists():
    raise FileNotFoundError(
        f"Source workbook not found: {file_path}. "
        "Keep it inside the repository's 03-data folder."
    )

balance_sheet = pd.read_excel(file_path, sheet_name="Raw_Balance_Sheet")
cash_flows = pd.read_excel(file_path, sheet_name="Raw_Cash_Flows")

print("=" * 50)
print("1. DATASET SIZES")
print("=" * 50)
print("Balance sheet:", balance_sheet.shape)
print("Cash flows:", cash_flows.shape)

print("\n2. MISSING VALUES")
print("\nBalance sheet:")
print(balance_sheet.isna().sum())
print("\nCash flows:")
print(cash_flows.isna().sum())

print("\n3. DUPLICATE ROWS")
print("Balance sheet duplicates:", balance_sheet.duplicated().sum())
print("Cash flow duplicates:", cash_flows.duplicated().sum())

print("\n4. CURRENCY VALUES")
print("Balance sheet:", balance_sheet["currency"].dropna().unique())
print("Cash flows:", cash_flows["currency"].dropna().unique())

print("\n5. INVALID BALANCE-SHEET VALUES")
invalid_outflows = balance_sheet["net_cash_outflows_30d_gbp_m"].le(0)
negative_hqla = balance_sheet["hqla_gbp_m"].lt(0)
print("Non-positive net outflows:", int(invalid_outflows.sum()))
print("Negative HQLA:", int(negative_hqla.sum()))
print(
    balance_sheet.loc[
        invalid_outflows | negative_hqla,
        ["report_date", "entity_id", "hqla_gbp_m", "net_cash_outflows_30d_gbp_m"]
    ].to_string(index=False)
)

print("\n6. CASH FLOW RECONCILIATION")
cash_flows["calculated_net_cash_flow"] = (
    cash_flows["cash_inflows_gbp_m"] - cash_flows["cash_outflows_gbp_m"]
)
cash_flows["reconciliation_difference"] = (
    cash_flows["net_cash_flow_gbp_m"] - cash_flows["calculated_net_cash_flow"]
)
reconciliation_issues = cash_flows["reconciliation_difference"].abs().gt(0.01)
print("Rows with reconciliation differences:", int(reconciliation_issues.sum()))

print("\n7. DATA TYPES")
print(balance_sheet.dtypes)
print("\nCash flows:")
print(cash_flows.dtypes)

print("\nDATA PROFILING COMPLETED")
