cat > atm_cash_dag.py <<'EOF'
import csv
import os
from datetime import datetime

from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator

# ---- Input data embedded in this file (CSV is created automatically) ----
CSV_PATH = "/opt/airflow/dags/atm_cash.csv"
CSV_DATA = """atm_id,location,cash_available,daily_demand
ATM101,North,90000,45000
ATM102,South,25000,40000
ATM103,East,120000,50000
ATM104,West,30000,60000
ATM105,Central,70000,30000
"""

os.makedirs(os.path.dirname(CSV_PATH), exist_ok=True)
with open(CSV_PATH, "w", newline="") as f:
    f.write(CSV_DATA)


# Task 1: starter function (provided)
def load_atms():
    with open('/opt/airflow/dags/atm_cash.csv', newline='') as file:
        records = list(csv.DictReader(file))
    print('ATM records loaded:', len(records))
    return records


# Task 2: ATMs where cash_available < daily_demand
def identify_low_cash(ti):
    atms = ti.xcom_pull(task_ids="load_atms")
    low_cash_ids = [
        a["atm_id"]
        for a in atms
        if int(a["cash_available"]) < int(a["daily_demand"])
    ]
    print("Low-cash ATMs:", low_cash_ids)
    return low_cash_ids


# Task 3: sum of cash_available
def calculate_total_cash(ti):
    atms = ti.xcom_pull(task_ids="load_atms")
    total_cash = sum(int(a["cash_available"]) for a in atms)
    print("Total available cash:", total_cash)
    return total_cash


# Task 4: final report
def generate_report(ti):
    atms = ti.xcom_pull(task_ids="load_atms")
    low_cash_ids = ti.xcom_pull(task_ids="identify_low_cash")
    total_cash = ti.xcom_pull(task_ids="calculate_total_cash")

    print("===== ATM CASH REPLENISHMENT REPORT =====")
    print("Number of ATMs:", len(atms))
    print("Low-cash ATM IDs:", low_cash_ids)
    print("Total available cash:", total_cash)
    print("=========================================")


with DAG(
    dag_id="atm_cash_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
) as dag:

    t1 = PythonOperator(task_id="load_atms", python_callable=load_atms)
    t2 = PythonOperator(task_id="identify_low_cash", python_callable=identify_low_cash)
    t3 = PythonOperator(task_id="calculate_total_cash", python_callable=calculate_total_cash)
    t4 = PythonOperator(task_id="generate_report", python_callable=generate_report)

    t1 >> [t2, t3] >> t4
EOF