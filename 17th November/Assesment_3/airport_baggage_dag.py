cat > airport_baggage_dag.py <<'EOF'
import csv
import os
from datetime import datetime

from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator

# ---- Input data embedded in this file (CSV is created automatically) ----
CSV_PATH = "/opt/airflow/dags/airport_baggage.csv"
CSV_DATA = """bag_id,flight_no,weight_kg,screening_status
BG101,AI502,18,Clear
BG102,AI502,27,Clear
BG103,6E214,12,Review
BG104,6E214,22,Clear
BG105,UK812,25,Review
BG106,UK812,15,Clear
"""

os.makedirs(os.path.dirname(CSV_PATH), exist_ok=True)
with open(CSV_PATH, "w", newline="") as f:
    f.write(CSV_DATA)


# Task 1: starter function (provided)
def load_baggage():
    with open('/opt/airflow/dags/airport_baggage.csv', newline='') as file:
        records = list(csv.DictReader(file))
    print('Baggage records loaded:', len(records))
    return records


# Task 2: status is Review OR weight_kg > 23
def identify_review_bags(ti):
    bags = ti.xcom_pull(task_ids="load_baggage")
    review_ids = [
        b["bag_id"]
        for b in bags
        if b["screening_status"] == "Review" or int(b["weight_kg"]) > 23
    ]
    print("Bags requiring review:", review_ids)
    return review_ids


# Task 3: sum of weight_kg
def calculate_total_weight(ti):
    bags = ti.xcom_pull(task_ids="load_baggage")
    total_weight = sum(int(b["weight_kg"]) for b in bags)
    print("Total baggage weight (kg):", total_weight)
    return total_weight


# Task 4: final report
def generate_report(ti):
    bags = ti.xcom_pull(task_ids="load_baggage")
    review_ids = ti.xcom_pull(task_ids="identify_review_bags")
    total_weight = ti.xcom_pull(task_ids="calculate_total_weight")

    print("===== AIRPORT BAGGAGE SCREENING REPORT =====")
    print("Number of bags:", len(bags))
    print("Bag IDs requiring review:", review_ids)
    print("Total baggage weight (kg):", total_weight)
    print("============================================")


with DAG(
    dag_id="airport_baggage_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
) as dag:

    t1 = PythonOperator(task_id="load_baggage", python_callable=load_baggage)
    t2 = PythonOperator(task_id="identify_review_bags", python_callable=identify_review_bags)
    t3 = PythonOperator(task_id="calculate_total_weight", python_callable=calculate_total_weight)
    t4 = PythonOperator(task_id="generate_report", python_callable=generate_report)

    t1 >> [t2, t3] >> t4
EOF