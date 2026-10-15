import csv
import json
import numpy as np
import pandas as pd

with open("shipments.csv", "r") as f:
    shipment_rows = list(csv.DictReader(f))

for row in shipment_rows:
    row["weight"] = float(row["weight"])
    row["cost"] = int(row["cost"])

# Q1
weight = float(input("Enter shipment weight: "))
cost = float(input("Enter shipment cost: "))

# Q2
cost_per_kg = cost / weight
print(f"Cost per kg: {cost_per_kg:.2f}")

# Q3
if weight > 20:
    print("Heavy")
elif weight >= 10:
    print("Medium")
else:
    print("Light")

# Q4
for i in range(1, 21):
    print(i)

# Q5
for i in range(1, 21):
    if i % 2 == 0:
        print(i)

# Q6
attempt = 1
while attempt <= 5:
    print("Processing attempt", attempt)
    attempt = attempt + 1

# Q7
shipment_costs = []
for row in shipment_rows:
    shipment_costs.append(row["cost"])
print("Shipment costs:", shipment_costs)

# Q8
print("Total:", sum(shipment_costs))
print("Average:", sum(shipment_costs) / len(shipment_costs))
print("Minimum:", min(shipment_costs))
print("Maximum:", max(shipment_costs))

# Q9
destinations = []
for row in shipment_rows:
    destinations.append(row["destination"])
unique_destinations = set(destinations)
print(unique_destinations)

# Q10
shipment = shipment_rows[0]
print(shipment)

# Q11
shipments = shipment_rows
print("Number of shipments stored:", len(shipments))
for s in shipments:
    print(s)

# Q12
for s in shipments:
    if s["status"] == "Delivered":
        print(s)

# Q13
def calculate_shipping_cost(weight, rate_per_kg):
    return weight * rate_per_kg


rate_per_kg = shipment["cost"] / shipment["weight"]
print(calculate_shipping_cost(shipment["weight"], rate_per_kg))

# Q14
def get_shipment_category(weight):
    if weight > 20:
        return "Heavy"
    elif weight >= 10:
        return "Medium"
    else:
        return "Light"


for row in shipment_rows:
    print(row["shipment_id"], get_shipment_category(row["weight"]))

# Q15
delivered = list(filter(lambda s: s["status"] == "Delivered", shipments))
print(delivered)

# Q16
all_destinations = list(map(lambda s: s["destination"], shipments))
print(all_destinations)

# Q17
sorted_shipments = sorted(shipments, key=lambda s: s["cost"])
print(sorted_shipments)


# Q18
class Shipment:
    # Q19
    def __init__(self, shipment_id, destination, weight, cost):
        self.shipment_id = shipment_id
        self.destination = destination
        self.weight = weight
        self.cost = cost

    # Q20
    def display(self):
        print(f"Shipment {self.shipment_id} to {self.destination}, weight {self.weight}, cost {self.cost}")

    def get_total_cost(self):
        return self.cost


# Q21
class ExpressShipment(Shipment):
    # Q22
    def get_total_cost(self):
        surcharge = 300
        return self.cost + surcharge

    def display(self):
        print(f"Express Shipment {self.shipment_id} to {self.destination}, total cost {self.get_total_cost()}")


# Q23
first = shipment_rows[0]
second = shipment_rows[1]
normal = Shipment(first["shipment_id"], first["destination"], first["weight"], first["cost"])
express = ExpressShipment(second["shipment_id"], second["destination"], second["weight"], second["cost"])
for sh in [normal, express]:
    sh.display()
    print(sh.get_total_cost())

# Q18
print("Class created:", Shipment.__name__)

# Q19
print(normal.shipment_id, normal.destination, normal.weight, normal.cost)

# Q20
normal.display()

# Q21
print("ExpressShipment inherits from Shipment:", issubclass(ExpressShipment, Shipment))

# Q22
print("Normal cost:", normal.get_total_cost())
print("Express cost with surcharge:", express.get_total_cost())

# Q24
with open("employees.json", "r") as f:
    employees = json.load(f)
print("employees.json read, employees loaded:", len(employees))

# Q25
for e in employees:
    print(e["name"])

# Q26
for e in employees:
    if e["salary"] > 75000:
        print(e["name"], e["salary"])

# Q27
for e in employees:
    if "Python" in e["skills"]:
        print(e["name"])

# Q28
for e in employees:
    print(e["name"], e["performance"]["rating"])

# Q29
for e in employees:
    if e["performance"]["rating"] > 4.5:
        print(e["name"], e["performance"]["rating"])

# Q30
sorted_employees = sorted(employees, key=lambda e: e["performance"]["rating"], reverse=True)
for e in sorted_employees:
    print(e["name"], e["performance"]["rating"])

# Q31
for e in employees:
    if e["employee_id"] == 303:
        e["skills"].append("Python")
print(employees)

# Q32
with open("employees_updated.json", "w") as f:
    json.dump(employees, f, indent=4)
print("employees_updated.json saved")

# Q36
shipments_df = pd.read_csv("shipments.csv")
print(shipments_df)

# Q37
print(shipments_df[shipments_df["status"] == "Delivered"])

# Q38
print(shipments_df["status"].value_counts())

# Q39
shipments_df["shipment_date"] = pd.to_datetime(shipments_df["shipment_date"])
print(shipments_df["shipment_date"].dtype)

# Q40
shipments_df["month"] = shipments_df["shipment_date"].dt.month
print(shipments_df.groupby(["month", "status"]).size())

# Q41
print(shipments_df.groupby("destination")["cost"].mean())

# Q42
print(shipments_df.groupby("destination")["weight"].sum())

# Q43
columns_needed = ["shipment_id", "hub_id", "destination", "cost"]
selected_df = pd.read_csv("shipments.csv", usecols=columns_needed)
print(selected_df)

# Q44
hubs_df = pd.read_csv("hubs.csv")
print(hubs_df)

# Q45
merged = pd.merge(shipments_df, hubs_df, on="hub_id", how="inner")
print(merged)

# Q46
hub_cost = merged.groupby("hub_name")["cost"].sum()
print(hub_cost)

# Q47
hub_count = merged.groupby("hub_name")["shipment_id"].count()
print(hub_count)

# Q48
hub_summary = pd.DataFrame({"total_cost": hub_cost, "total_shipments": hub_count}).reset_index()
hub_summary = hub_summary.sort_values("total_cost", ascending=False)
print(hub_summary)

# Q49
hub_summary.to_csv("hub_summary.csv", index=False)
print("hub_summary.csv saved")

# Q50
hub_summary.to_json("hub_summary.json", orient="records", indent=4)
print("hub_summary.json saved")

# Q51
shipments_df["cost_per_kg"] = (shipments_df["cost"] / shipments_df["weight"]).round(2)
print(shipments_df[["shipment_id", "cost", "weight", "cost_per_kg"]])

# Q52
shipments_df["cost_type"] = np.where(shipments_df["cost"] >= 1200, "Expensive", "Normal")
print(shipments_df[["shipment_id", "cost", "cost_type"]])

# Q53
conditions = [
    (shipments_df["status"] == "Delivered") & (shipments_df["cost"] >= 1200),
    (shipments_df["status"] == "Delivered") & (shipments_df["cost"] < 1200),
    (shipments_df["status"] == "In Transit"),
    (shipments_df["status"] == "Pending")
]
categories = ["High Value Delivered", "Standard Delivered", "On The Way", "Needs Attention"]
shipments_df["performance_category"] = np.select(conditions, categories, default="Unknown")
print(shipments_df[["shipment_id", "status", "cost", "performance_category"]])

# Q54
shipments_df.to_csv("shipment_analysis.csv", index=False)
print(shipments_df)
