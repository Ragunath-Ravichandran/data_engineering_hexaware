# Week 3 - PySpark for Attendance Analysis
# Files needed in this folder: attendance.csv, tasks.csv
# Steps: load -> clean -> filter late logins and absences -> group by department

import os
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

# step 1: start spark session
spark = SparkSession.builder.appName("AttendanceAnalysis").master("local[*]").getOrCreate()
spark.sparkContext.setLogLevel("ERROR")
# wrong values should become null instead of giving error
spark.conf.set("spark.sql.ansi.enabled", "false")

# step 2: load the data (read everything as text first, then change types)
attendance = spark.read.csv("attendance.csv", header=True)
tasks = spark.read.csv("tasks.csv", header=True)
print("Total rows in attendance file:", attendance.count())

# step 3: clean the data
attendance = attendance.dropDuplicates()

attendance = attendance.withColumn("break_minutes", F.col("break_minutes").cast("double"))
attendance = attendance.withColumn("clock_in", F.to_timestamp("clock_in", "yyyy-MM-dd HH:mm:ss"))
attendance = attendance.withColumn("clock_out", F.to_timestamp("clock_out", "yyyy-MM-dd HH:mm:ss"))
tasks = tasks.withColumn("tasks_assigned", F.col("tasks_assigned").cast("int"))
tasks = tasks.withColumn("tasks_completed", F.col("tasks_completed").cast("double"))

# negative break time is wrong, so make it null
attendance = attendance.withColumn(
    "break_minutes",
    F.when(F.col("break_minutes") >= 0, F.col("break_minutes")))

# fill missing break time with the median break
median_break = attendance.approxQuantile("break_minutes", [0.5], 0.01)[0]
attendance = attendance.fillna({"break_minutes": median_break})
print("Median break used for missing values:", median_break)

print("Rows after removing duplicates:", attendance.count())

# separate absent rows and working rows (PRESENT or LATE)
absent = attendance.filter(F.col("status") == "ABSENT")
worked = attendance.filter(F.col("status").isin("PRESENT", "LATE"))

# remove working rows with missing time or clock out before clock in
worked = worked.dropna(subset=["clock_in", "clock_out"])
worked = worked.filter(F.col("clock_out") > F.col("clock_in"))

# step 4: calculate work hours and productivity
worked = worked.withColumn(
    "work_hours",
    F.round((F.unix_timestamp("clock_out") - F.unix_timestamp("clock_in")) / 3600
            - F.col("break_minutes") / 60, 2))
worked = worked.filter(F.col("work_hours") > 0)

# add task data (join on employee and date)
worked = worked.join(tasks, on=["employee_id", "work_date"], how="left")

# productivity = tasks completed per work hour
worked = worked.withColumn(
    "productivity_score",
    F.round(F.col("tasks_completed") / F.col("work_hours"), 2))

# completion rate = tasks completed out of tasks assigned (only when tasks were assigned)
worked = worked.withColumn(
    "completion_pct",
    F.when(F.col("tasks_assigned") > 0, F.round(F.col("tasks_completed") / F.col("tasks_assigned") * 100, 2)))

print("Clean working rows:", worked.count())
print("Absent rows:", absent.count())

# step 5: filter late logins (status is already LATE in the file)
late_logins = worked.filter(F.col("status") == "LATE")
print("Late logins:", late_logins.count())

# step 6: group by department
total_by_dept = attendance.groupBy("department").agg(
    F.count("*").alias("total_records"))

avg_by_dept = worked.groupBy("department").agg(
    F.round(F.avg("work_hours"), 2).alias("avg_work_hours"),
    F.round(F.avg("productivity_score"), 2).alias("avg_productivity"),
    F.round(F.avg("completion_pct"), 2).alias("avg_completion_pct"))

late_by_dept = late_logins.groupBy("department").agg(
    F.count("*").alias("late_login_count"))

absent_by_dept = absent.groupBy("department").agg(
    F.count("*").alias("absent_count"))

# combine all results into one table
result = total_by_dept.join(avg_by_dept, on="department", how="left")
result = result.join(late_by_dept, on="department", how="left")
result = result.join(absent_by_dept, on="department", how="left")
result = result.fillna(0)
result = result.withColumn("absent_rate_pct", F.round(F.col("absent_count") / F.col("total_records") * 100, 2))
result = result.withColumn("late_rate_pct", F.round(F.col("late_login_count") / F.col("total_records") * 100, 2))
result = result.orderBy(F.col("absent_count").desc())

print("\n--- Attendance issues by department ---")
result.show()

# step 7: save the output
# (on Windows, spark write needs winutils, so I convert the small result to pandas and save)
os.makedirs("output", exist_ok=True)
result.toPandas().to_csv("output/attendance_issues_by_department.csv", index=False)
print("Saved in output/attendance_issues_by_department.csv")

spark.stop()