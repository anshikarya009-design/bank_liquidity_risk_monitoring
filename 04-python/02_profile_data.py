
from pathlib import Path
import pandas as pd

# Locate the project and final Excel workbook
PROJECT_DIR = Path(__file__).resolve().parent
file_path = PROJECT_DIR / "data" / "bank_liquidity_risk_final.xlsx"

# Load the raw worksheets
balance_sheet = pd.read_excel(
    file_path, sheet_name="Raw_Balance_Sheet"
)
cash_flows = pd.read_excel(
    file_path, sheet_name="Raw_Cash_Flows"
)

print("=" * 50)
print("1. DATASET SIZES")
print("=" * 50)
print("Balance sheet:", balance_sheet.shape)
print("Cash flows:", cash_flows.shape)

print("\n" + "=" * 50)
print("2. MISSING VALUES")
print("=" * 50)
print("\nBalance sheet:")
print(balance_sheet.isnull().sum())

print("\nCash flows:")
print(cash_flows.isnull().sum())

print("\n" + "=" * 50)
print("3. DUPLICATE ROWS")
print("=" * 50)
print("Balance sheet duplicates:", balance_sheet.duplicated().sum())
print("Cash flow duplicates:", cash_flows.duplicated().sum())

print("\n" + "=" * 50)
print("4. CURRENCY VALUES")
print("=" * 50)
print("Balance sheet:", balance_sheet["currency"].unique())
print("Cash flows:", cash_flows["currency"].unique())

print("\n" + "=" * 50)
print("5. NEGATIVE CASH OUTFLOWS")
print("=" * 50)
print(
    balance_sheet[
        balance_sheet["net_cash_outflows_30d_gbp_m"] < 0
    ][["report_date", "entity_id", "net_cash_outflows_30d_gbp_m"]]
)

print("\n" + "=" * 50)
print("6. CASH FLOW RECONCILIATION")
print("=" * 50)

cash_flows["calculated_net_cash_flow"] = (
    cash_flows["cash_inflows_gbp_m"]
    - cash_flows["cash_outflows_gbp_m"]
)

cash_flows["reconciliation_difference"] = (
    cash_flows["net_cash_flow_gbp_m"]
    - cash_flows["calculated_net_cash_flow"]
)

print(
    "Rows with reconciliation differences:",
    cash_flows["reconciliation_difference"]
    .abs()
    .gt(0.01)
    .sum()
)

print("\n" + "=" * 50)
print("7. DATA TYPES")
print("=" * 50)
print(balance_sheet.dtypes)
print("\nCash flows:")
print(cash_flows.dtypes)

print("\nDATA PROFILING COMPLETED")
