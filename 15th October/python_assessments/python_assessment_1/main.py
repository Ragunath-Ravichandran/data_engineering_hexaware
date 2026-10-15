import csv
import json

with open("orders.csv", "r") as f:
    order_rows = list(csv.DictReader(f))

with open("products.json", "r") as f:
    product_rows = json.load(f)

price = int(order_rows[0]["unit_price"])
quantity = int(order_rows[0]["quantity"])

# Q56
print("retail_utils.py has: calculate_order_total, calculate_discount, check_stock")

# Q57
import retail_utils

print("Module imported:", retail_utils.__name__)

# Q58
total = retail_utils.calculate_order_total(price, quantity)
print(total)
print(retail_utils.calculate_discount(total))
print(retail_utils.check_stock(product_rows[0]["stock"]))

# Q59
from retail_utils import check_stock

print(check_stock(product_rows[1]["stock"]))

# Q60
import retail_utils as ru

print(ru.calculate_discount(total))
