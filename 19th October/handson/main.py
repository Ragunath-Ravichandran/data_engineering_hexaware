from fastapi import FastAPI,HTTPException
from pydantic import BaseModel

app=FastAPI()

class Employee(BaseModel):
    id:int
    name:str
    department:str
    designation:str
    salary:float
    city:str

employees=[
    {
    "id": 101,
    "name": "Rahul Sharma",
    "department": "IT",
    "designation": "Developer",
    "salary": 65000,
    "city": "Hyderabad"
  },
  {
    "id": 102,
    "name": "Priya Nair",
    "department": "Finance",
    "designation": "Accountant",
    "salary": 72000,
    "city": "Chennai"
  },
  {
    "id": 103,
    "name": "Arjun Mehta",
    "department": "Marketing",
    "designation": "Marketing Executive",
    "salary": 58000,
    "city": "Mumbai"
  },
  {
    "id": 104,
    "name": "Sneha Reddy",
    "department": "HR",
    "designation": "HR Manager",
    "salary": 54000,
    "city": "Bengaluru"
  },
  {
    "id": 105,
    "name": "Karthik Iyer",
    "department": "Sales",
    "designation": "Sales Lead",
    "salary": 61000,
    "city": "Coimbatore"
  }
]

employees = [Employee(**employee) for employee in employees]

@app.post("/employees")
def add_employee(employee:Employee):
    employees.append(employee)
    return {"message":"Employee added successfully!"}

@app.get("/employees")
def get_employees():
    return employees

@app.get("/employees/{e_id}")
def get_employee(e_id:int):
    for e in employees:
        if e.id == e_id:
            return e
    raise HTTPException(status_code=404, detail="Employee not found")

@app.put("/employees/{e_id}")
def update_employee(e_id:int, employee:Employee):
    for i, e in enumerate(employees):
        if e.id==e_id:
            employees[i]=employee
            return {"message":"Employee updated successfully!"}
    raise HTTPException(status_code=404, detail="Employee not found")

@app.delete("/employees/{e_id}")
def delete_employee(e_id:int, employee:Employee):
    for i, e in enumerate(employees):
            if e.id==e_id:
                deleted_item=employees.pop(i)
                return get_employees
    raise HTTPException(status_code=404, detail="Employee not found")
