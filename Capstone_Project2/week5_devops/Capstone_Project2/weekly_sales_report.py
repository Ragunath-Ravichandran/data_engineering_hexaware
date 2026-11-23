# weekly_sales_report.py
# Weekly report for the Retail Sales Performance Dashboard
# This script is run by GitHub Actions every Monday (see .github/workflows/project2-weekly-report.yml)
#
# Input files (same folder): sales.csv, products.csv, stores.csv
# Output files (output folder): store_performance.csv, underperforming_products.csv, summary.md

import os
import sys
from datetime import datetime, timezone

import pandas as pd

OUTPUT_FOLDER = "output"
HIGH_RETURN_RATE = 7      # return rate (%) above this is "high returns"


def to_markdown_table(df):
    # small helper to write a dataframe as a markdown table
    columns = list(df.columns)
    lines = ["| " + " | ".join(columns) + " |", "|" + "---|" * len(columns)]
    for _, row in df.iterrows():
        lines.append("| " + " | ".join(str(value) for value in row) + " |")
    return "\n".join(lines)


# step 1: check that the input files are there (fail clearly if not)
for file_name in ["sales.csv", "products.csv", "stores.csv"]:
    if not os.path.exists(file_name):
        print("ERROR: missing input file:", file_name)
        sys.exit(1)

sales = pd.read_csv("sales.csv", dtype=str)
products = pd.read_csv("products.csv", dtype=str)
stores = pd.read_csv("stores.csv", dtype=str)
print("Sales rows:", len(sales))

# step 2: clean the sales data
sales = sales.drop_duplicates(subset=["sale_id"]).copy()

sales["store_id"] = pd.to_numeric(sales["store_id"], errors="coerce")
sales["product_id"] = pd.to_numeric(sales["product_id"], errors="coerce")
sales["quantity"] = pd.to_numeric(sales["quantity"], errors="coerce")
sales["discount_pct"] = pd.to_numeric(sales["discount_pct"], errors="coerce").fillna(0)
sales["returned"] = pd.to_numeric(sales["returned"], errors="coerce").fillna(0)
sales["sale_date"] = pd.to_datetime(sales["sale_date"], format="%Y-%m-%d", errors="coerce")

sales = sales.dropna(subset=["sale_date", "store_id", "product_id", "quantity"])
sales = sales[sales["quantity"] > 0].copy()
print("Sales rows after cleaning:", len(sales))

products["product_id"] = pd.to_numeric(products["product_id"], errors="coerce")
products["price"] = pd.to_numeric(products["price"], errors="coerce")
products["cost"] = pd.to_numeric(products["cost"], errors="coerce")
products = products.dropna(subset=["product_id", "price", "cost"]).drop_duplicates("product_id")

stores["store_id"] = pd.to_numeric(stores["store_id"], errors="coerce")
stores = stores.dropna(subset=["store_id"]).drop_duplicates("store_id")

# step 3: join and calculate revenue and profit
data = sales.merge(products, on="product_id", how="inner")
data = data.merge(stores, on="store_id", how="left")

data["revenue"] = data["quantity"] * data["price"] * (1 - data["discount_pct"] / 100)
data["profit"] = data["revenue"] - data["quantity"] * data["cost"]
data["month"] = data["sale_date"].dt.strftime("%Y-%m")

# step 4: store performance (average monthly revenue, lowest first)
monthly = data.groupby(["store_id", "store_name", "region", "month"], as_index=False)["revenue"].sum()
store_report = monthly.groupby(["store_id", "store_name", "region"], as_index=False).agg(
    avg_monthly_revenue=("revenue", "mean"))
totals = data.groupby("store_id", as_index=False).agg(
    total_revenue=("revenue", "sum"), total_profit=("profit", "sum"))
store_report = store_report.merge(totals, on="store_id")
store_report["store_id"] = store_report["store_id"].astype(int)
store_report = store_report.round(2).sort_values("avg_monthly_revenue").reset_index(drop=True)
store_report.insert(0, "rank_lowest_first", range(1, len(store_report) + 1))
lowest5 = store_report.head(5)

# step 5: underperforming products (low sales OR high returns)
product_report = data.groupby(["product_id", "product_name"], as_index=False).agg(
    total_units_sold=("quantity", "sum"),
    total_revenue=("revenue", "sum"),
    total_orders=("sale_id", "count"),
    returned_orders=("returned", "sum"))
product_report["return_rate_pct"] = product_report["returned_orders"] / product_report["total_orders"] * 100

average_units = product_report["total_units_sold"].mean()
low_sales = product_report["total_units_sold"] < average_units
high_returns = product_report["return_rate_pct"] > HIGH_RETURN_RATE

underperforming = product_report[low_sales | high_returns].copy()
underperforming["reason"] = "low sales"
underperforming.loc[high_returns[underperforming.index], "reason"] = "high returns"
underperforming.loc[(low_sales & high_returns)[underperforming.index], "reason"] = "low sales and high returns"
underperforming["total_units_sold"] = underperforming["total_units_sold"].astype(int)
underperforming["returned_orders"] = underperforming["returned_orders"].astype(int)
underperforming = underperforming.round(2).sort_values("total_units_sold").reset_index(drop=True)

# step 6: print the results (they appear in the pipeline log)
print("\n===== LOWEST PERFORMING STORES (top 5, lowest first) =====")
print(lowest5.to_string(index=False))
print("\n===== UNDERPERFORMING PRODUCTS =====")
print(underperforming.to_string(index=False))

# step 7: save the report files
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
store_report.to_csv(f"{OUTPUT_FOLDER}/store_performance.csv", index=False)
underperforming.to_csv(f"{OUTPUT_FOLDER}/underperforming_products.csv", index=False)

run_time = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
with open(f"{OUTPUT_FOLDER}/summary.md", "w") as f:
    f.write("# Weekly Sales Report\n\n")
    f.write(f"Generated: {run_time}\n\n")
    f.write("## Top 5 lowest performing stores (average monthly revenue)\n\n")
    f.write(to_markdown_table(lowest5[["rank_lowest_first", "store_name", "region", "avg_monthly_revenue"]]) + "\n\n")
    f.write("## Underperforming products\n\n")
    f.write(to_markdown_table(underperforming[["product_name", "total_units_sold", "return_rate_pct", "reason"]]) + "\n")

print(f"\nReport saved in the '{OUTPUT_FOLDER}' folder")
