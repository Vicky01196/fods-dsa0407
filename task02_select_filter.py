# %% (a) Select student name, department, attendance and internal marks
import pandas as pd

pd.set_option("display.width", 112)
pd.set_option("display.max_columns", None)

df = pd.read_csv("data/student_performance_raw.csv")

selected_cols = ["Student_Name", "Department", "Attendance_Pct", "Internal_Marks"]
selected = df[selected_cols]          # column selection using a list of names
print("Selected columns (first 8 rows):")
print(selected.head(8))

# %% (b) Filter students whose attendance is below 75%
low_attendance = df.loc[df["Attendance_Pct"] < 75, selected_cols]
print("Students with attendance below 75%:")
print(low_attendance)
print("\nCount:", len(low_attendance))

# Rows with missing attendance are NOT returned by the condition (NaN < 75 is False)
print("\nRecords with missing attendance (cannot be classified yet):")
print(df.loc[df["Attendance_Pct"].isna(), ["Student_ID", "Student_Name"]])

# %% (c) Filter students with internal marks above a chosen threshold
MARKS_THRESHOLD = 75   # chosen threshold: internal marks > 75 out of 100
high_marks = df.loc[df["Internal_Marks"] > MARKS_THRESHOLD, selected_cols]
print(f"Students with internal marks above {MARKS_THRESHOLD}:")
print(high_marks)

# %% (d) Combined filter: students who may need academic support
support = df.query("Attendance_Pct < 75 and Internal_Marks < 50")[selected_cols]
print("Students with attendance < 75% AND internal marks < 50:")
print(support)
