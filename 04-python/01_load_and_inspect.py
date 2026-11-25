from pathlib import Path
import pandas as pd

# Repository layout:
# 03-data/bank_liquidity_risk_final.xlsx
# 04-python/01_load_and_inspect.py
PROJECT_DIR = Path(__file__).resolve().parent
DATA_DIR = PROJECT_DIR.parent / "03-data"
file_path = DATA_DIR / "bank_liquidity_risk_final.xlsx"

print("Looking for file:", file_path)

if not file_path.exists():
    raise FileNotFoundError(
        f"Source workbook not found: {file_path}\n"
        "Keep bank_liquidity_risk_final.xlsx inside the repository's 03-data folder."
    )

balance_sheet = pd.read_excel(file_path, sheet_name="Raw_Balance_Sheet")
cash_flows = pd.read_excel(file_path, sheet_name="Raw_Cash_Flows")

print("\nBALANCE SHEET DATA")
print(balance_sheet.head())
print("\nCASH FLOW DATA")
print(cash_flows.head())

print("\nDATASET SIZES")
print("Balance sheet:", balance_sheet.shape)
print("Cash flows:", cash_flows.shape)

print("\nBALANCE SHEET INFORMATION")
balance_sheet.info()
print("\nCASH FLOW INFORMATION")
cash_flows.info()
