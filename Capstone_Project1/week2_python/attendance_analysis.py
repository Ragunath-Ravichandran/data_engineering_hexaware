import os
import pandas as pd
import numpy as np

os.makedirs("output", exist_ok=True)  # create output folder if it doesn't exist

# load the data
attendance = pd.read_csv("attendance.csv")
tasks = pd.read_csv("tasks.csv")

print("Attendance rows:", len(attendance))
print("Tasks rows:", len(tasks))
print("Missing values in attendance:")
print(attendance.isnull().sum())

# remove duplicate rows
attendance = attendance.drop_duplicates(subset=["employee_id", "work_date"])
tasks = tasks.drop_duplicates(subset=["employee_id", "work_date"])
print("Attendance rows after removing duplicates:", len(attendance))

# convert columns to correct data types
attendance["work_date"] = pd.to_datetime(attendance["work_date"], errors="coerce")
attendance["clock_in"] = pd.to_datetime(attendance["clock_in"], errors="coerce")
attendance["clock_out"] = pd.to_datetime(attendance["clock_out"], errors="coerce")
attendance["break_minutes"] = pd.to_numeric(attendance["break_minutes"], errors="coerce")
tasks["work_date"] = pd.to_datetime(tasks["work_date"], errors="coerce")

attendance = attendance.dropna(subset=["work_date"])

# fix missing and negative break values using median
present_only = attendance[attendance["status"] != "ABSENT"]
median_break = present_only["break_minutes"].median()
attendance["break_minutes"] = attendance["break_minutes"].fillna(median_break)
attendance["break_minutes"] = np.where(attendance["break_minutes"] < 0, median_break, attendance["break_minutes"])
attendance["break_minutes"] = np.where(attendance["status"] == "ABSENT", 0, attendance["break_minutes"])

# completed tasks cannot be more than assigned tasks
tasks["tasks_assigned"] = tasks["tasks_assigned"].fillna(0)
tasks["tasks_completed"] = tasks["tasks_completed"].fillna(0)
tasks["tasks_completed"] = np.where(tasks["tasks_completed"] > tasks["tasks_assigned"], tasks["tasks_assigned"], tasks["tasks_completed"])

# combine attendance and task data
df = pd.merge(attendance, tasks, on=["employee_id", "work_date"], how="left")
df["tasks_assigned"] = df["tasks_assigned"].fillna(0)
df["tasks_completed"] = df["tasks_completed"].fillna(0)

# remove rows with missing time or clock out before clock in
bad_rows = (df["status"] != "ABSENT") & (df["clock_in"].isnull() | df["clock_out"].isnull() | (df["clock_out"] <= df["clock_in"]))
print("Rows with wrong clock in/out removed:", bad_rows.sum())
df = df[~bad_rows]

# work hours and productivity using numpy
df["break_hours"] = df["break_minutes"] / 60
df["work_hours"] = (df["clock_out"] - df["clock_in"]).dt.total_seconds() / 3600 - df["break_hours"]
df["work_hours"] = df["work_hours"].fillna(0)
df["work_hours"] = np.where(df["work_hours"] < 0, 0, df["work_hours"])

df["productivity_score"] = np.where(df["work_hours"] > 0, df["tasks_completed"] / df["work_hours"], 0)
df["completion_rate"] = np.where(df["tasks_assigned"] > 0, df["tasks_completed"] / df["tasks_assigned"] * 100, 0)

# late if login is after 9:15 (555 minutes)
login_minutes = df["clock_in"].dt.hour * 60 + df["clock_in"].dt.minute
df["is_late"] = np.where(login_minutes > 555, 1, 0)
df["is_absent"] = np.where(df["status"] == "ABSENT", 1, 0)

df = df.round({"break_hours": 2, "work_hours": 2, "productivity_score": 2, "completion_rate": 2})
df.to_csv("output/cleaned_attendance.csv", index=False)
print("Cleaned rows:", len(df))

# summary for each employee
summary = df.groupby(["employee_id", "employee_name", "department"]).agg(
    days_recorded=("work_date", "count"),
    absences=("is_absent", "sum"),
    late_days=("is_late", "sum")
).reset_index()

worked = df[df["is_absent"] == 0]
averages = worked.groupby("employee_id").agg(
    avg_work_hours=("work_hours", "mean"),
    avg_break_hours=("break_hours", "mean"),
    avg_productivity=("productivity_score", "mean"),
    avg_completion_rate=("completion_rate", "mean")
).reset_index()

summary = pd.merge(summary, averages, on="employee_id", how="left")
summary = summary.fillna(0)
summary["absence_rate"] = summary["absences"] / summary["days_recorded"] * 100
summary = summary.round(2)
summary.to_csv("output/employee_summary.csv", index=False)

# top, bottom performers and frequent absentees
columns = ["employee_id", "employee_name", "department", "avg_work_hours", "avg_productivity", "absences", "late_days"]

top5 = summary.sort_values("avg_productivity", ascending=False).head(5)
bottom5 = summary.sort_values("avg_productivity", ascending=True).head(5)
absentees = summary.sort_values(["absences", "late_days"], ascending=False).head(5)

department_summary = summary.groupby("department").agg(
    employees=("employee_id", "count"),
    avg_work_hours=("avg_work_hours", "mean"),
    avg_productivity=("avg_productivity", "mean"),
    total_absences=("absences", "sum"),
    total_late_days=("late_days", "sum")
).round(2)

print("")
print("TOP 5 PERFORMERS")
print(top5[columns].to_string(index=False))
print("")
print("BOTTOM 5 PERFORMERS")
print(bottom5[columns].to_string(index=False))
print("")
print("FREQUENT ABSENTEES")
print(absentees[columns].to_string(index=False))
print("")
print("DEPARTMENT SUMMARY")
print(department_summary)

# save report to file
report = open("output/performance_report.txt", "w")
report.write("EMPLOYEE ATTENDANCE AND PRODUCTIVITY REPORT\n\n")
report.write("TOP 5 PERFORMERS\n")
report.write(top5[columns].to_string(index=False))
report.write("\n\nBOTTOM 5 PERFORMERS\n")
report.write(bottom5[columns].to_string(index=False))
report.write("\n\nFREQUENT ABSENTEES\n")
report.write(absentees[columns].to_string(index=False))
report.write("\n\nDEPARTMENT SUMMARY\n")
report.write(department_summary.to_string())
report.close()

print("")
print("Report saved in output folder")
