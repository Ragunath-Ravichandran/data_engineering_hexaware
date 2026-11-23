# weekly_attendance_report.py
# Weekly report for the Employee Attendance and Productivity Tracker
# This script is run by GitHub Actions every Monday (see .github/workflows/project1-weekly-report.yml)
#
# Input files (same folder): attendance.csv, tasks.csv
# Output files (output folder): department_kpis.csv, top5_absentees.csv, summary.md

import os
import sys
from datetime import datetime, timezone

import numpy as np
import pandas as pd

OUTPUT_FOLDER = "output"


def to_markdown_table(df):
    # small helper to write a dataframe as a markdown table
    columns = list(df.columns)
    lines = ["| " + " | ".join(columns) + " |", "|" + "---|" * len(columns)]
    for _, row in df.iterrows():
        lines.append("| " + " | ".join(str(value) for value in row) + " |")
    return "\n".join(lines)


# step 1: check that the input files are there (fail clearly if not)
for file_name in ["attendance.csv", "tasks.csv"]:
    if not os.path.exists(file_name):
        print("ERROR: missing input file:", file_name)
        sys.exit(1)

attendance = pd.read_csv("attendance.csv", dtype=str)
tasks = pd.read_csv("tasks.csv", dtype=str)
print("Attendance rows:", len(attendance))
print("Task rows:", len(tasks))

# step 2: clean the attendance data
attendance = attendance.drop_duplicates().copy()

attendance["break_minutes"] = pd.to_numeric(attendance["break_minutes"], errors="coerce")
attendance["clock_in"] = pd.to_datetime(attendance["clock_in"], format="%Y-%m-%d %H:%M:%S", errors="coerce")
attendance["clock_out"] = pd.to_datetime(attendance["clock_out"], format="%Y-%m-%d %H:%M:%S", errors="coerce")

# negative break is wrong, make it empty and fill with the median break
attendance.loc[attendance["break_minutes"] < 0, "break_minutes"] = np.nan
median_break = attendance["break_minutes"].median()
attendance["break_minutes"] = attendance["break_minutes"].fillna(median_break)

# clean the tasks data
tasks = tasks.drop_duplicates(subset=["employee_id", "work_date"]).copy()
tasks["tasks_assigned"] = pd.to_numeric(tasks["tasks_assigned"], errors="coerce")
tasks["tasks_completed"] = pd.to_numeric(tasks["tasks_completed"], errors="coerce")

# step 3: separate absent rows and working rows (PRESENT or LATE)
absent = attendance[attendance["status"] == "ABSENT"].copy()
worked = attendance[attendance["status"].isin(["PRESENT", "LATE"])].copy()

# remove working rows with missing time or clock out before clock in
worked = worked.dropna(subset=["clock_in", "clock_out"])
worked = worked[worked["clock_out"] > worked["clock_in"]].copy()

# step 4: work hours, productivity and completion rate
hours = (worked["clock_out"] - worked["clock_in"]).dt.total_seconds() / 3600
worked["work_hours"] = (hours - worked["break_minutes"] / 60).round(2)
worked = worked[worked["work_hours"] > 0].copy()

worked = worked.merge(tasks, on=["employee_id", "work_date"], how="left")
worked["productivity_score"] = (worked["tasks_completed"] / worked["work_hours"]).round(2)
worked["completion_pct"] = np.where(
    worked["tasks_assigned"] > 0,
    (worked["tasks_completed"] / worked["tasks_assigned"] * 100).round(2),
    np.nan)

print("Working rows:", len(worked))
print("Absent rows:", len(absent))

# step 5: department report
dept = pd.DataFrame({"total_records": attendance.groupby("department").size()})
dept["absent_count"] = absent.groupby("department").size()
dept["late_login_count"] = worked[worked["status"] == "LATE"].groupby("department").size()
dept["avg_work_hours"] = worked.groupby("department")["work_hours"].mean()
dept["avg_productivity"] = worked.groupby("department")["productivity_score"].mean()
dept["avg_completion_pct"] = worked.groupby("department")["completion_pct"].mean()
dept[["absent_count", "late_login_count"]] = dept[["absent_count", "late_login_count"]].fillna(0).astype(int)
dept["absent_rate_pct"] = dept["absent_count"] / dept["total_records"] * 100
dept["late_rate_pct"] = dept["late_login_count"] / dept["total_records"] * 100
dept = dept.round(2).reset_index()

# lowest performing department = lowest average productivity
dept = dept.sort_values("avg_productivity")

# step 6: top 5 absentees
employees = attendance[["employee_id", "employee_name", "department"]].drop_duplicates("employee_id").copy()
employees["absent_days"] = employees["employee_id"].map(absent.groupby("employee_id").size()).fillna(0).astype(int)
employees["late_logins"] = employees["employee_id"].map(
    worked[worked["status"] == "LATE"].groupby("employee_id").size()).fillna(0).astype(int)
employees["employee_number"] = pd.to_numeric(employees["employee_id"], errors="coerce")
employees = employees.sort_values(["absent_days", "late_logins", "employee_number"],
                                  ascending=[False, False, True])
top5 = employees.head(5)[["employee_id", "employee_name", "department", "absent_days", "late_logins"]]
top5 = top5.reset_index(drop=True)
top5.insert(0, "rank", range(1, len(top5) + 1))

# step 7: print the results (they appear in the pipeline log)
print("\n===== DEPARTMENTS (lowest productivity first) =====")
print(dept.to_string(index=False))
print("\n===== TOP 5 ABSENTEES =====")
print(top5.to_string(index=False))

# step 8: save the report files
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
dept.to_csv(f"{OUTPUT_FOLDER}/department_kpis.csv", index=False)
top5.to_csv(f"{OUTPUT_FOLDER}/top5_absentees.csv", index=False)

run_time = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
summary_columns = ["department", "avg_productivity", "avg_work_hours", "absent_rate_pct", "late_rate_pct"]
with open(f"{OUTPUT_FOLDER}/summary.md", "w") as f:
    f.write("# Weekly Attendance Report\n\n")
    f.write(f"Generated: {run_time}\n\n")
    f.write("## Departments (lowest productivity first)\n\n")
    f.write(to_markdown_table(dept[summary_columns]) + "\n\n")
    f.write("## Top 5 absentees\n\n")
    f.write(to_markdown_table(top5) + "\n")

print(f"\nReport saved in the '{OUTPUT_FOLDER}' folder")
