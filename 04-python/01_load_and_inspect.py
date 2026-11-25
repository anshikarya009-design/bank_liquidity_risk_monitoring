
from pathlib import Path
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parent
file_path = PROJECT_DIR / "data" / "bank_liquidity_risk_final.xlsx"

print("Looking for file:", file_path)

if not file_path.exists():
    raise FileNotFoundError(
        f"File not found: {file_path}\n"
        "Check whether the filename or extension is different."
    )

print("Excel file found successfully!")

balance_sheet = pd.read_excel(
    file_path,
    sheet_name="Raw_Balance_Sheet"
)

cash_flows = pd.read_excel(
    file_path,
    sheet_name="Raw_Cash_Flows"
)

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
