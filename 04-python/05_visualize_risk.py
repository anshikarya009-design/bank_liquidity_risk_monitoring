from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

PROJECT_DIR = Path(__file__).resolve().parent
REPORT_DIR = PROJECT_DIR.parent / "06-reports"
OUTPUT_DIR = REPORT_DIR / "charts"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

file_path = REPORT_DIR / "liquidity_risk_analysis.csv"
if not file_path.exists():
    raise FileNotFoundError(
        f"Risk analysis CSV not found: {file_path}. Run 04_liquidity_risk_analysis.py first."
    )

df = pd.read_csv(file_path, parse_dates=["report_date"])
required = ["report_date", "entity_id", "lcr_proxy_pct"]
missing = [col for col in required if col not in df.columns]
if missing:
    raise ValueError(f"Missing required columns: {missing}")

# Plot 1: Liquidity proxy trend by entity.
plt.figure(figsize=(10, 6))
for entity, group in df.groupby("entity_id"):
    group = group.sort_values("report_date")
    plt.plot(group["report_date"], group["lcr_proxy_pct"], marker="o", label=entity)

plt.axhline(y=100, linestyle="--", label="Illustrative 100% threshold")
plt.axhline(y=120, linestyle=":", label="Illustrative 120% threshold")
plt.title("Liquidity Proxy Trend by Entity")
plt.xlabel("Reporting Date")
plt.ylabel("Liquidity Proxy (%)")
plt.legend()
plt.grid(True, alpha=0.3)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "liquidity_proxy_trend.png", dpi=150)
plt.close()

# Plot 2: Latest valid liquidity proxy by entity.
latest = (
    df.sort_values("report_date")
    .groupby("entity_id", group_keys=False)
    .tail(1)
)
latest = latest.dropna(subset=["lcr_proxy_pct"])

plt.figure(figsize=(9, 5))
plt.bar(latest["entity_id"].astype(str), latest["lcr_proxy_pct"])
plt.axhline(y=100, linestyle="--", label="Illustrative 100% threshold")
plt.axhline(y=120, linestyle=":", label="Illustrative 120% threshold")
plt.title("Latest Liquidity Proxy by Entity")
plt.xlabel("Entity")
plt.ylabel("Liquidity Proxy (%)")
plt.legend()
plt.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "latest_liquidity_comparison.png", dpi=150)
plt.close()

print("Charts saved successfully in:", OUTPUT_DIR)
