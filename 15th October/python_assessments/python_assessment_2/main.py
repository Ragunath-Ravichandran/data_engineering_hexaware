import csv

with open("shipments.csv", "r") as f:
    shipment_rows = list(csv.DictReader(f))

weight = float(shipment_rows[0]["weight"])
cost = int(shipment_rows[0]["cost"])

# Q33
print("shipment_utils.py has: calculate_shipping_cost, get_shipment_category, calculate_cost_per_kg")

# Q34
import shipment_utils

print(shipment_utils.calculate_shipping_cost(weight, cost / weight))
print(shipment_utils.get_shipment_category(weight))
print(shipment_utils.calculate_cost_per_kg(cost, weight))

# Q35
from shipment_utils import get_shipment_category

for row in shipment_rows:
    print(row["shipment_id"], get_shipment_category(float(row["weight"])))
