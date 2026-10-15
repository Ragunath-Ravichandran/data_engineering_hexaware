import csv
import json
import numpy as np
import pandas as pd

with open("customers.csv", "r") as f:
    customer_rows = list(csv.DictReader(f))

with open("orders.csv", "r") as f:
    order_rows = list(csv.DictReader(f))

for row in order_rows:
    row["quantity"] = int(row["quantity"])
    row["unit_price"] = int(row["unit_price"])

with open("products.json", "r") as f:
    product_rows = json.load(f)

# Q1
product_name = input("Enter product name: ")
unit_price = float(input("Enter unit price: "))
quantity = int(input("Enter quantity: "))

# Q2
total_amount = unit_price * quantity
print("Total amount:", total_amount)

# Q3
if total_amount >= 50000:
    discount = total_amount * 0.10
else:
    discount = total_amount * 0.05
print("Discount:", discount)

# Q4
final_amount = total_amount - discount
print(f"Product: {product_name}")
print(f"Original amount: {total_amount}")
print(f"Discount: {discount}")
print(f"Final amount: {final_amount}")

# Q5
stock = int(input("Enter stock quantity: "))
if stock > 20:
    print("High Stock")
elif stock >= 1:
    print("Low Stock")
else:
    print("Out of Stock")

# Q6
for i in range(1, 11):
    print(i)

# Q7
stock_left = 5
while stock_left >= 0:
    print(stock_left)
    stock_left = stock_left - 1

# Q8
for i in range(1, 11):
    if i == 5:
        continue
    print(i)

# Q9
for i in range(1, 15):
    if i == 8:
        break
    print(i)

sales = []
for row in order_rows[:7]:
    sales.append(row["quantity"] * row["unit_price"])

# Q10
total = sum(sales)
print("Total sales:", total)

# Q11
print("Highest sale:", max(sales))
print("Lowest sale:", min(sales))

# Q12
for s in sales:
    if s > 20000:
        print(s)

# Q13
sorted_sales = sorted(sales, reverse=True)
print(sorted_sales)

# Q14
cities = ["Hyderabad", "Mumbai", "Delhi", "Hyderabad", "Pune", "Mumbai"]
unique_cities = set(cities)
print(unique_cities)

# Q15
first_product = product_rows[0]
product_tuple = (first_product["product_id"], first_product["product_name"], first_product["category"], first_product["price"])
pid, pname, pcategory, pprice = product_tuple
print(pid, pname, pcategory, pprice)

# Q16
first_customer = customer_rows[0]
order_count = 0
for o in order_rows:
    if o["customer_id"] == first_customer["customer_id"]:
        order_count = order_count + 1
customer = {
    "id": first_customer["customer_id"],
    "name": first_customer["customer_name"],
    "city": first_customer["city"],
    "orders": order_count,
    "active": first_customer["active"] == "True"
}
print(customer)

# Q17
customer["city"] = "Chennai"
print(customer)

# Q18
customer["orders"] = customer["orders"] + 1
print(customer)

# Q19
customer["email"] = "northstar@email.com"
print(customer)

# Q20
for key, value in customer.items():
    print(key, ":", value)

# Q21
def calculate_total(price, quantity):
    return price * quantity


print(calculate_total(order_rows[1]["unit_price"], order_rows[1]["quantity"]))

# Q22
def calculate_discount(amount):
    if amount >= 50000:
        return amount * 0.10
    else:
        return amount * 0.05


print(calculate_discount(sales[0]))

# Q23
def total_sales(sales_list):
    total = 0
    for s in sales_list:
        total = total + s
    return total


print(total_sales(sales))

# Q24
def check_availability(product):
    if product["stock"] > 0:
        return "Available"
    else:
        return "Out of Stock"


for p in product_rows:
    print(p["product_name"], check_availability(p))

# Q25
square = lambda x: x * x
print(square(6))

# Q26
high_sales = list(filter(lambda x: x > 20000, sales))
print(high_sales)

# Q27
customer_list = customer_rows
customer_cities = list(map(lambda c: c["city"], customer_list))
print(customer_cities)

# Q28
print(set(customer_cities))

# Q29
product_list = product_rows
sorted_products = sorted(product_list, key=lambda p: p["price"])
print(sorted_products)


class Product:
    # Q30
    def __init__(self, product_id, product_name, price, stock):
        self.product_id = product_id
        self.product_name = product_name
        self.price = price
        self.stock = stock

    # Q31
    def display_product(self):
        print(f"ID: {self.product_id}, Name: {self.product_name}, Price: {self.price}, Stock: {self.stock}")

    # Q32
    def calculate_value(self):
        return self.price * self.stock


# Q33
first_p = product_rows[0]
second_p = product_rows[3]
p1 = Product(first_p["product_id"], first_p["product_name"], first_p["price"], first_p["stock"])
p2 = Product(second_p["product_id"], second_p["product_name"], second_p["price"], second_p["stock"])
print("Objects created:", p1.product_name, "and", p2.product_name)

# Q30
print(p1.product_id, p1.product_name, p1.price, p1.stock)
print(p2.product_id, p2.product_name, p2.price, p2.stock)

# Q31
p1.display_product()
p2.display_product()

# Q32
print(p1.calculate_value())
print(p2.calculate_value())


# Q34
class DiscountedProduct(Product):
    # Q35
    def __init__(self, product_id, product_name, price, stock, discount_percent):
        # Q36
        super().__init__(product_id, product_name, price, stock)
        self.discount_percent = discount_percent

    # Q37
    def display_product(self):
        super().display_product()
        print(f"Discount: {self.discount_percent}%")


# Q38
class PremiumProduct(Product):
    def display_product(self):
        print(f"Premium Product -> {self.product_name} costs {self.price}")


# Q39
chair = product_rows[2]
monitor = product_rows[1]
d1 = DiscountedProduct(chair["product_id"], chair["product_name"], chair["price"], chair["stock"], 10)
pr1 = PremiumProduct(monitor["product_id"], monitor["product_name"], monitor["price"], monitor["stock"])
all_products = [p1, d1, pr1]
for item in all_products:
    item.display_product()

# Q34
print("DiscountedProduct inherits from Product:", issubclass(DiscountedProduct, Product))

# Q35
print("Discount percent:", d1.discount_percent)

# Q36
print(d1.product_id, d1.product_name, d1.price, d1.stock)

# Q37
d1.display_product()

# Q38
pr1.display_product()

# Q40
with open("activity.txt", "w") as f:
    pass
print("activity.txt created")

# Q41
with open("activity.txt", "w") as f:
    f.write("Order processing started\n")
    f.write("Orders validated\n")
    f.write("Orders packed\n")
print("3 processing messages written to activity.txt")

# Q42
with open("activity.txt", "a") as f:
    f.write("Orders shipped\n")
print("1 more message appended to activity.txt")

# Q43
with open("activity.txt", "r") as f:
    print(f.read())

# Q44
with open("customers.csv", "r") as f:
    reader = csv.DictReader(f)
    rows_read = list(reader)
print("Columns read:", reader.fieldnames)

# Q45
customers_data = []
for row in rows_read:
    customers_data.append(row)
print(customers_data)

# Q46
for c in customers_data:
    if c["active"] == "True":
        print(c)

# Q47
for c in customers_data:
    if c["city"] == "Hyderabad":
        print(c)

# Q48
with open("products.json", "r") as f:
    products = json.load(f)
print("products.json read, products loaded:", len(products))

# Q49
for p in products:
    print(p["product_name"])

# Q50
for p in products:
    if p["price"] > 10000:
        print(p["product_name"], p["price"])

# Q51
for p in products:
    print(p["supplier"]["name"], p["supplier"]["city"])

# Q52
all_colors = []
for p in products:
    for color in p["colors"]:
        all_colors.append(color)
print(all_colors)

# Q53
print(set(all_colors))

# Q54
for p in products:
    if p["product_id"] == 202:
        p["stock"] = p["stock"] + 10
print(products)

# Q55
with open("products_updated.json", "w") as f:
    json.dump(products, f, indent=4)
print("products_updated.json saved")

# Q61
orders = pd.read_csv("orders.csv")
print("orders.csv loaded into DataFrame, rows:", len(orders))

# Q62
print(orders.head())

# Q63
print(orders.columns)
print(orders.dtypes)

# Q64
print(orders.shape)

# Q65
delivered_orders = orders.query("status == 'Delivered'")
print(delivered_orders)

# Q66
print(orders[orders["quantity"] > 2])

# Q67
orders["order_value"] = orders["quantity"] * orders["unit_price"]
print(orders)

# Q68
print(orders["status"].value_counts())

# Q69
orders["order_date"] = pd.to_datetime(orders["order_date"])
print(orders["order_date"].dtype)

# Q70
orders["month"] = orders["order_date"].dt.month
print(orders[["order_date", "month"]].head())

# Q71
print(orders.groupby(["month", "status"]).size())

# Q72
print(orders.groupby("category")["order_value"].sum())

# Q73
print(orders.groupby("category")["order_value"].mean())

# Q74
print(orders.sort_values("order_value", ascending=False))

# Q75
customers_df = pd.read_csv("customers.csv")
orders_df = pd.read_csv("orders.csv")
orders_df["order_value"] = orders_df["quantity"] * orders_df["unit_price"]
merged = pd.merge(orders_df, customers_df, on="customer_id", how="inner")
print(merged)

# Q76
print(merged[["order_id", "customer_name", "city", "product", "status", "order_value"]])

# Q77
print(merged.query("status == 'Delivered' and city == 'Hyderabad'"))

# Q78
city_summary = merged.groupby("city").agg(
    total_orders=("order_id", "count"),
    total_sales=("order_value", "sum"),
    average_order_value=("order_value", "mean")
).reset_index()
print(city_summary)

# Q79
city_summary = city_summary.sort_values("total_sales", ascending=False)
print(city_summary)

# Q80
city_summary.to_csv("city_sales_summary.csv", index=False)
print("city_sales_summary.csv saved")

# Q81
city_summary.to_json("city_sales_summary.json", orient="records", indent=4)
print("city_sales_summary.json saved")

# Q82
merged["order_size"] = np.where(
    merged["order_value"] >= 50000, "High",
    np.where(merged["order_value"] >= 15000, "Medium", "Low")
)
print(merged[["order_id", "order_value", "order_size"]])

# Q83
merged["priority_customer"] = np.where(merged["segment"] == "Corporate", "Priority", "Normal")
print(merged[["order_id", "segment", "priority_customer"]])

# Q84
merged.to_csv("enriched_orders.csv", index=False)
print(merged)
