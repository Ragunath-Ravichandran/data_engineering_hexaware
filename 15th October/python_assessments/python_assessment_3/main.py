import csv

with open("registrations.csv", "r") as f:
    registration_rows = list(csv.DictReader(f))

with open("events.csv", "r") as f:
    event_rows = list(csv.DictReader(f))

reg = registration_rows[7]
tickets = int(reg["tickets"])
amount = int(reg["amount"])
ticket_price = amount / tickets

event = event_rows[0]
registered = 0
for r in registration_rows:
    if r["event_id"] == event["event_id"]:
        registered = registered + int(r["tickets"])

# Q75
print("event_utils.py has: calculate_booking_amount, calculate_discount, check_event_capacity")

# Q76
import event_utils

print("Module imported:", event_utils.__name__)

# Q77
print(event_utils.calculate_booking_amount(ticket_price, tickets))
print(event_utils.calculate_discount(amount))
print(event_utils.check_event_capacity(int(event["capacity"]), registered))

# Q78
from event_utils import calculate_discount

print(calculate_discount(int(registration_rows[0]["amount"])))

# Q79
import event_utils as eu

print(eu.check_event_capacity(int(event_rows[2]["capacity"]), 200))
