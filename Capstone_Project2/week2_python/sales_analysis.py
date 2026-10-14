import os
import pandas as pd

os.makedirs("output", exist_ok=True)  # create output folder if it doesn't exist
import numpy as np
import requests


sales = pd.read_csv("sales.csv")

products = pd.read_csv("products.csv")
stores = pd.read_csv("stores.csv")

print("Sales rows:", len(sales))
print("Missing values in sales:")
print(sales.isnull().sum())

# remove duplicate rows
sales = sales.drop_duplicates(subset="sale_id")
products = products.drop_duplicates(subset="product_id")
print("Sales rows after removing duplicates:", len(sales))

# convert columns to correct data types
sales["sale_date"] = pd.to_datetime(sales["sale_date"], errors="coerce")
sales["quantity"] = pd.to_numeric(sales["quantity"], errors="coerce")
sales["discount_pct"] = pd.to_numeric(sales["discount_pct"], errors="coerce")
sales["store_id"] = pd.to_numeric(sales["store_id"], errors="coerce")
sales["product_id"] = pd.to_numeric(sales["product_id"], errors="coerce")
products["price"] = pd.to_numeric(products["price"], errors="coerce")
products["cost"] = pd.to_numeric(products["cost"], errors="coerce")

# missing discount means no discount
sales["discount_pct"] = sales["discount_pct"].fillna(0)

# remove rows with missing or wrong values
rows_before = len(sales)
sales = sales.dropna(subset=["sale_date", "quantity", "store_id", "product_id"])
sales = sales[sales["quantity"] > 0]
print("Rows removed because of wrong or missing data:", rows_before - len(sales))

sales["store_id"] = sales["store_id"].astype(int)
sales["product_id"] = sales["product_id"].astype(int)
sales["quantity"] = sales["quantity"].astype(int)

# join sales with product and store details
df = pd.merge(sales, products, on="product_id")
df = pd.merge(df, stores, on="store_id")

# revenue, profit and margin using numpy
df["gross_revenue"] = np.multiply(df["quantity"], df["price"])
df["discount_amount"] = df["gross_revenue"] * df["discount_pct"] / 100
df["revenue"] = df["gross_revenue"] - df["discount_amount"]
df["total_cost"] = np.multiply(df["quantity"], df["cost"])
df["profit"] = df["revenue"] - df["total_cost"]
df["discount_percentage"] = np.where(df["gross_revenue"] > 0, df["discount_amount"] / df["gross_revenue"] * 100, 0)
df["profit_margin"] = np.where(df["revenue"] > 0, df["profit"] / df["revenue"] * 100, 0)

df = df.round({"gross_revenue": 2, "discount_amount": 2, "revenue": 2, "total_cost": 2, "profit": 2, "discount_percentage": 2, "profit_margin": 2})
df.to_csv("output/cleaned_sales.csv", index=False)
print("Cleaned rows:", len(df))

print("")
print("Total revenue:", round(df["revenue"].sum(), 2))
print("Total profit:", round(df["profit"].sum(), 2))

# summary by product
revenue_by_product = df.groupby(["product_id", "product_name", "category"]).agg(
    units_sold=("quantity", "sum"),
    revenue=("revenue", "sum"),
    profit=("profit", "sum"),
    avg_discount=("discount_percentage", "mean"),
    returns=("returned", "sum")
).reset_index()
revenue_by_product["profit_margin"] = revenue_by_product["profit"] / revenue_by_product["revenue"] * 100
revenue_by_product = revenue_by_product.round(2)
revenue_by_product = revenue_by_product.sort_values("revenue", ascending=False)

# summary by store
revenue_by_store = df.groupby(["store_id", "store_name", "region"]).agg(
    units_sold=("quantity", "sum"),
    revenue=("revenue", "sum"),
    profit=("profit", "sum"),
    avg_discount=("discount_percentage", "mean"),
    returns=("returned", "sum")
).reset_index()
revenue_by_store["profit_margin"] = revenue_by_store["profit"] / revenue_by_store["revenue"] * 100
revenue_by_store = revenue_by_store.round(2)
revenue_by_store = revenue_by_store.sort_values("revenue", ascending=False)

# revenue for each product in each store
revenue_by_product_store = df.groupby(["store_name", "product_name"])["revenue"].sum().round(2).reset_index()

revenue_by_product.to_csv("output/revenue_by_product.csv", index=False)
revenue_by_store.to_csv("output/revenue_by_store.csv", index=False)
revenue_by_product_store.to_csv("output/revenue_by_product_store.csv", index=False)

print("")
print("REVENUE BY PRODUCT")
print(revenue_by_product.to_string(index=False))
print("")
print("REVENUE BY STORE")
print(revenue_by_store.to_string(index=False))
print("")
print("Files saved in output folder")
