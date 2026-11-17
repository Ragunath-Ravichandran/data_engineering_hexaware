cat > factory_quality_dag.py <<'EOF'
import csv
import os
from datetime import datetime

from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator

# ---- Input data embedded in this file (CSV is created automatically) ----
CSV_PATH = "/opt/airflow/dags/factory_batches.csv"
CSV_DATA = """batch_id,units_produced,defective_units,value_per_unit
B501,100,2,350
B502,80,7,420
B503,120,4,300
B504,60,0,550
B505,90,6,400
"""

os.makedirs(os.path.dirname(CSV_PATH), exist_ok=True)
with open(CSV_PATH, "w", newline="") as f:
    f.write(CSV_DATA)


# Task 1: starter function (provided)
def load_batches():
    with open("/opt/airflow/dags/factory_batches.csv", newline="") as file:
        rows = list(csv.DictReader(file))
    print("Batches loaded:", len(rows))
    return rows


# Task 2: batches where defective units exceed 5% of units produced
def check_quality(ti):
    batches = ti.xcom_pull(task_ids="load_batches")
    review_ids = []
    for b in batches:
        units = int(b["units_produced"])
        defective = int(b["defective_units"])
        if defective > 0.05 * units:
            review_ids.append(b["batch_id"])
    print("Batches needing review:", review_ids)
    return review_ids


# Task 3: total production value = units_produced * value_per_unit
def calculate_value(ti):
    batches = ti.xcom_pull(task_ids="load_batches")
    total_value = sum(
        int(b["units_produced"]) * int(b["value_per_unit"]) for b in batches
    )
    print("Total production value:", total_value)
    return total_value


# Task 4: final report
def generate_report(ti):
    batches = ti.xcom_pull(task_ids="load_batches")
    review_ids = ti.xcom_pull(task_ids="check_quality")
    total_value = ti.xcom_pull(task_ids="calculate_value")

    print("===== MANUFACTURING BATCH QUALITY REPORT =====")
    print("Total batches:", len(batches))
    print("Batch IDs requiring review:", review_ids)
    print("Total production value:", total_value)
    print("==============================================")


with DAG(
    dag_id="factory_quality_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
) as dag:

    t1 = PythonOperator(task_id="load_batches", python_callable=load_batches)
    t2 = PythonOperator(task_id="check_quality", python_callable=check_quality)
    t3 = PythonOperator(task_id="calculate_value", python_callable=calculate_value)
    t4 = PythonOperator(task_id="generate_report", python_callable=generate_report)

    t1 >> [t2, t3] >> t4
EOF