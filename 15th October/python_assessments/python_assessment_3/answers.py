import csv
import json
import pandas as pd

with open("registrations.csv", "r") as f:
    registration_rows = list(csv.DictReader(f))

for row in registration_rows:
    row["tickets"] = int(row["tickets"])
    row["amount"] = int(row["amount"])

with open("events.csv", "r") as f:
    event_rows = list(csv.DictReader(f))

for row in event_rows:
    row["capacity"] = int(row["capacity"])

# Q1
attendee_name = input("Enter attendee name: ")
tickets = int(input("Enter number of tickets: "))
ticket_price = float(input("Enter ticket price: "))

# Q2
total_amount = tickets * ticket_price
print("Total amount:", total_amount)

# Q3
if total_amount >= 10000:
    discount = total_amount * 0.10
else:
    discount = total_amount * 0.05
final_amount = total_amount - discount
print("Discount:", discount)

# Q4
print(f"Attendee: {attendee_name}")
print(f"Tickets: {tickets}")
print(f"Total amount: {total_amount}")
print(f"Discount: {discount}")
print(f"Final amount: {final_amount}")

# Q5
capacity = int(input("Enter event capacity: "))
registered = int(input("Enter registered participants: "))

# Q6
if registered == capacity:
    print("Full")
elif registered < capacity:
    print("Seats Available")
else:
    print("Invalid Data")

# Q7
for i in range(1, 16):
    print(i)

# Q8
for i in range(1, 16):
    if i % 3 == 0:
        print(i)

# Q9
count = 10
while count >= 1:
    print(count)
    count = count - 1

# Q10
for i in range(1, 11):
    if i == 4:
        continue
    if i == 8:
        break
    print(i)

booking_amounts = []
for row in registration_rows[:8]:
    booking_amounts.append(row["amount"])

# Q11
print("Total:", sum(booking_amounts))

# Q12
print("Average:", sum(booking_amounts) / len(booking_amounts))

# Q13
print("Highest:", max(booking_amounts))
print("Lowest:", min(booking_amounts))

# Q14
for a in booking_amounts:
    if a > 5000:
        print(a)

# Q15
print(sorted(booking_amounts, reverse=True))

cities = ["Hyderabad", "Mumbai", "Pune", "Hyderabad", "Delhi", "Mumbai"]

# Q16
unique_cities = set(cities)
print(unique_cities)

# Q17
unique_cities.add("Chennai")
print(unique_cities)

# Q18
print(len(unique_cities))

# Q19
first_event = event_rows[0]
event_tuple = (first_event["event_id"], first_event["event_name"], first_event["venue_city"], first_event["capacity"])
print(event_tuple)

# Q20
event_id, event_name, venue, event_capacity = event_tuple
print(event_id, event_name, venue, event_capacity)

# Q21
first_registration = registration_rows[0]
registration = {
    "registration_id": first_registration["registration_id"],
    "attendee_name": first_registration["attendee_name"],
    "city": first_registration["city"],
    "tickets": first_registration["tickets"],
    "status": first_registration["status"],
    "amount": first_registration["amount"]
}
print(registration)

# Q22
registration["status"] = "Pending"
print(registration)

# Q23
registration["tickets"] = registration["tickets"] + 1
print(registration)

# Q24
registration["email"] = "aarav@email.com"
print(registration)

# Q25
for key, value in registration.items():
    print(key, ":", value)

# Q26
def calculate_booking(ticket_price, tickets):
    return ticket_price * tickets


first_price = first_registration["amount"] / first_registration["tickets"]
print(calculate_booking(first_price, first_registration["tickets"]))

# Q27
def calculate_discount(amount):
    if amount >= 10000:
        return amount * 0.10
    else:
        return amount * 0.05


for a in booking_amounts:
    print(a, calculate_discount(a))

# Q28
def is_active(status):
    if status == "Cancelled":
        return False
    else:
        return True


for row in registration_rows:
    print(row["registration_id"], row["status"], is_active(row["status"]))

# Q29
def total_amount_of(amounts):
    total = 0
    for a in amounts:
        total = total + a
    return total


print(total_amount_of(booking_amounts))

# Q30
increase = lambda amount: amount * 1.10
for a in booking_amounts:
    print(a, increase(a))

# Q31
big_amounts = list(filter(lambda a: a > 6000, booking_amounts))
print(big_amounts)

# Q32
registrations_list = registration_rows
confirmed = list(filter(lambda r: r["status"] == "Confirmed", registrations_list))
print(confirmed)

# Q33
reg_cities = list(map(lambda r: r["city"], registrations_list))
print(reg_cities)

# Q34
print(set(map(lambda r: r["city"], registrations_list)))

# Q35
sorted_registrations = sorted(registrations_list, key=lambda r: r["amount"])
print(sorted_registrations)


class Event:
    # Q36
    def __init__(self, event_id, event_name, capacity, ticket_price):
        self.event_id = event_id
        self.event_name = event_name
        self.capacity = capacity
        self.ticket_price = ticket_price

    # Q37
    def display_event(self):
        print(f"Event {self.event_id}: {self.event_name}, capacity {self.capacity}, ticket price {self.ticket_price}")

    # Q38
    def calculate_revenue(self, tickets_sold):
        return self.ticket_price * tickets_sold


def get_ticket_price(event_id):
    for r in registration_rows:
        if r["event_id"] == event_id:
            return r["amount"] / r["tickets"]


def get_tickets_sold(event_id):
    sold = 0
    for r in registration_rows:
        if r["event_id"] == event_id and is_active(r["status"]):
            sold = sold + r["tickets"]
    return sold


# Q39
ev1 = event_rows[0]
ev2 = event_rows[1]
e1 = Event(ev1["event_id"], ev1["event_name"], ev1["capacity"], get_ticket_price(ev1["event_id"]))
e2 = Event(ev2["event_id"], ev2["event_name"], ev2["capacity"], get_ticket_price(ev2["event_id"]))
print("Created events:", e1.event_name, "and", e2.event_name)

# Q36
print(e1.event_id, e1.event_name, e1.capacity, e1.ticket_price)
print(e2.event_id, e2.event_name, e2.capacity, e2.ticket_price)

# Q37
e1.display_event()
e2.display_event()

# Q38
print(e1.calculate_revenue(get_tickets_sold(e1.event_id)))
print(e2.calculate_revenue(get_tickets_sold(e2.event_id)))


class OnlineEvent(Event):
    # Q40
    def __init__(self, event_id, event_name, capacity, ticket_price, platform):
        # Q41
        super().__init__(event_id, event_name, capacity, ticket_price)
        self.platform = platform

    # Q42
    def display_event(self):
        super().display_event()
        print("Platform:", self.platform)


class PhysicalEvent(Event):
    # Q43
    def __init__(self, event_id, event_name, capacity, ticket_price, venue):
        super().__init__(event_id, event_name, capacity, ticket_price)
        self.venue = venue

    # Q44
    def display_event(self):
        super().display_event()
        print("Venue:", self.venue)


# Q45
ev3 = event_rows[2]
ev4 = event_rows[3]
online_event = OnlineEvent(ev3["event_id"], ev3["event_name"], ev3["capacity"], get_ticket_price(ev3["event_id"]), "Zoom")
physical_event = PhysicalEvent(ev4["event_id"], ev4["event_name"], ev4["capacity"], get_ticket_price(ev4["event_id"]), ev4["venue_city"])
event_list = [online_event, physical_event]
print("Objects in list:", len(event_list))

# Q46
for ev in event_list:
    ev.display_event()

# Q40
print("Platform:", online_event.platform)

# Q41
print(online_event.event_id, online_event.event_name, online_event.capacity, online_event.ticket_price)

# Q42
online_event.display_event()

# Q43
print("Venue:", physical_event.venue)

# Q44
physical_event.display_event()

# Q47
with open("event_log.txt", "w") as f:
    f.write("Event registration started\n")
    f.write("Registrations validated\n")
    f.write("Tickets generated\n")
print("3 messages written to event_log.txt")

# Q48
with open("event_log.txt", "a") as f:
    f.write("Confirmation emails sent\n")
    f.write("Event report created\n")
print("2 messages appended to event_log.txt")

# Q49
with open("event_log.txt", "r") as f:
    content = f.read()
    print(content)

# Q50
with open("event_log.txt", "r") as f:
    for line in f:
        print(repr(line))

# Q51
with open("event_log.txt", "r") as f:
    for line in f:
        print(line.strip())

# Q52
with open("event_log.txt", "r") as f:
    all_lines = f.readlines()
    print("Total lines:", len(all_lines))

# Q53
with open("registrations.csv", "r") as f:
    reader = csv.DictReader(f)
    rows_read = list(reader)
print("Columns read:", reader.fieldnames)

# Q54
records = []
for row in rows_read:
    records.append(row)
print("Records stored in list:", len(records))

# Q55
for r in records:
    if r["status"] == "Confirmed":
        print(r)

# Q56
for r in records:
    if r["city"] == "Hyderabad":
        print(r)

# Q57
for r in records:
    r["amount"] = int(r["amount"])
print(records[0]["amount"], type(records[0]["amount"]))

# Q58
for r in records:
    if r["amount"] > 7000:
        print(r)

# Q59
total_registration_amount = 0
for r in records:
    total_registration_amount = total_registration_amount + r["amount"]
print("Total registration amount:", total_registration_amount)

# Q60
all_cities = []
for r in records:
    all_cities.append(r["city"])
print(set(all_cities))

# Q61
with open("staff.json", "r") as f:
    staff = json.load(f)
print("staff.json read, records loaded:", len(staff))

# Q62
print(type(staff))

# Q63
for s in staff:
    print(s["name"])

# Q64
for s in staff:
    if s["department"] == "Operations":
        print(s["name"])

# Q65
for s in staff:
    if s["salary"] > 75000:
        print(s["name"], s["salary"])

# Q66
for s in staff:
    if "Python" in s["skills"]:
        print(s["name"])

# Q67
for s in staff:
    print(s["name"], s["performance"]["rating"], s["performance"]["events_handled"])

# Q68
for s in staff:
    if s["performance"]["rating"] > 4.5:
        print(s["name"], s["performance"]["rating"])

# Q69
all_skills = []
for s in staff:
    for skill in s["skills"]:
        all_skills.append(skill)
print(all_skills)

# Q70
print(set(all_skills))

# Q71
by_salary = sorted(staff, key=lambda s: s["salary"], reverse=True)
for s in by_salary:
    print(s["name"], s["salary"])

# Q72
by_rating = sorted(staff, key=lambda s: s["performance"]["rating"], reverse=True)
for s in by_rating:
    print(s["name"], s["performance"]["rating"])

# Q73
for s in staff:
    if s["staff_id"] == 503:
        s["skills"].append("Pandas")
print(staff)

# Q74
with open("staff_updated.json", "w") as f:
    json.dump(staff, f, indent=4)
print("staff_updated.json saved")

# Q80
df = pd.read_csv("registrations.csv")
print("registrations.csv loaded, rows:", len(df))

# Q81
print(df.head())
print(df.tail())
print(df.shape)
print(df.columns)
print(df.dtypes)

# Q82
print(df[["attendee_name", "city", "status", "amount"]])

# Q83
print(df.query("status == 'Confirmed'"))

# Q84
print(df[df["amount"] > 6000])

# Q85
print(df.query("status == 'Confirmed' and city == 'Hyderabad'"))

# Q86
print(df["status"].value_counts())

# Q87
print(df.groupby("status")["amount"].sum())

# Q88
print(df.groupby("city")["amount"].mean())
