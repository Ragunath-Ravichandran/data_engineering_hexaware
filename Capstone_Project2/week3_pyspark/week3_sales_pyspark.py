# Week 3 - PySpark for Store-Level Insights
# Files needed in this folder: sales.csv, products.csv, stores.csv
# Steps: load -> clean -> find underperforming products -> average monthly revenue by store

import os
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

# step 1: start spark session
spark = SparkSession.builder.appName("SalesAnalysis").master("local[*]").getOrCreate()
spark.sparkContext.setLogLevel("ERROR")
# wrong values should become null instead of giving error
spark.conf.set("spark.sql.ansi.enabled", "false")

# step 2: load the data (read everything as text first, then change types)
sales = spark.read.csv("sales.csv", header=True)
products = spark.read.csv("products.csv", header=True)
stores = spark.read.csv("stores.csv", header=True)
print("Total rows in sales file:", sales.count())

# step 3: clean the data
# sale_id is unique, so remove duplicate sale ids
sales = sales.dropDuplicates(["sale_id"])

# change data types (wrong values like "abc" become null)
sales = sales.withColumn("store_id", F.col("store_id").cast("double").cast("int"))
sales = sales.withColumn("product_id", F.col("product_id").cast("int"))
sales = sales.withColumn("quantity", F.col("quantity").cast("int"))
sales = sales.withColumn("discount_pct", F.col("discount_pct").cast("double"))
sales = sales.withColumn("returned", F.col("returned").cast("int"))

products = products.withColumn("product_id", F.col("product_id").cast("int"))
stores = stores.withColumn("store_id", F.col("store_id").cast("int"))
products = products.withColumn("price", F.col("price").cast("double"))
products = products.withColumn("cost", F.col("cost").cast("double"))

# date should look like yyyy-MM-dd, otherwise it is wrong (example: "not a date")
sales = sales.withColumn(
    "sale_date",
    F.when(F.col("sale_date").rlike("^[0-9]{4}-[0-9]{2}-[0-9]{2}$"), F.to_date("sale_date", "yyyy-MM-dd")))

# missing discount means no discount
sales = sales.fillna({"discount_pct": 0})

# remove rows with missing important values and wrong quantity
sales = sales.dropna(subset=["sale_date", "store_id", "quantity"])
sales = sales.filter(F.col("quantity") > 0)

print("Rows after cleaning:", sales.count())

# step 4: join with products and calculate revenue and profit
sales = sales.join(products, on="product_id", how="left")
sales = sales.dropna(subset=["price", "cost"])

sales = sales.withColumn(
    "revenue", F.round(F.col("quantity") * F.col("price") * (1 - F.col("discount_pct") / 100), 2))
sales = sales.withColumn(
    "profit", F.round(F.col("revenue") - F.col("quantity") * F.col("cost"), 2))

# step 5: find underperforming products
product_summary = sales.groupBy("product_id", "product_name").agg(
    F.sum("quantity").alias("total_units_sold"),
    F.sum("revenue").cast("decimal(18,2)").alias("total_revenue"),
    F.count("*").alias("total_orders"),
    F.sum("returned").alias("returned_orders"))

product_summary = product_summary.withColumn(
    "return_rate_pct",
    F.round(F.col("returned_orders") / F.col("total_orders") * 100, 2))

print("\n--- Product summary ---")
product_summary.orderBy("total_units_sold").show()

# average units sold across all products
avg_units = product_summary.agg(F.avg("total_units_sold")).collect()[0][0]
print("Average units sold per product:", round(avg_units, 2))

# underperforming = low sales (below average units) OR high returns (return rate above 7%)
underperforming = product_summary.filter(
    (F.col("total_units_sold") < avg_units) | (F.col("return_rate_pct") > 7))

underperforming = underperforming.withColumn(
    "reason",
    F.when((F.col("total_units_sold") < avg_units) & (F.col("return_rate_pct") > 7), "low sales and high returns")
     .when(F.col("return_rate_pct") > 7, "high returns")
     .otherwise("low sales"))

print("\n--- Underperforming products ---")
underperforming.orderBy("total_units_sold").show(truncate=False)

# step 6: average monthly revenue by store
sales = sales.withColumn("month", F.date_format("sale_date", "yyyy-MM"))

monthly_revenue = sales.groupBy("store_id", "month").agg(
    F.sum("revenue").alias("monthly_revenue"))

# add store name and region
monthly_revenue = monthly_revenue.join(stores, on="store_id", how="left")

store_summary = monthly_revenue.groupBy("store_id", "store_name", "region").agg(
    F.avg("monthly_revenue").cast("decimal(18,2)").alias("avg_monthly_revenue"))
store_summary = store_summary.orderBy(F.col("avg_monthly_revenue").desc())

print("\n--- Average monthly revenue by store ---")
store_summary.show()

# step 7: save the output
# (on Windows, spark write needs winutils, so I convert the small results to pandas and save)
os.makedirs("output", exist_ok=True)
underperforming.toPandas().to_csv("output/underperforming_products.csv", index=False)
store_summary.toPandas().to_csv("output/store_monthly_revenue.csv", index=False)
print("Saved in output/underperforming_products.csv and output/store_monthly_revenue.csv")

spark.stop()