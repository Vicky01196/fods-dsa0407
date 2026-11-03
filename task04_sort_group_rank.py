# %% (a) Load the prepared (clean) dataset and sort in descending order
import pandas as pd

pd.set_option("display.width", 112)
pd.set_option("display.max_columns", None)

# student_clean.csv is produced by the preprocessing workflow (task06_preprocessing.py)
df = pd.read_csv("data/student_clean.csv")
cols = ["Student_ID", "Student_Name", "Department", "Attendance_Pct", "Internal_Marks"]

by_marks = df.sort_values("Internal_Marks", ascending=False)[cols]
print("Students sorted by internal marks (highest first):")
print(by_marks.to_string(index=False))

# %% (b) Sort by attendance, using internal marks to break ties
by_att = df.sort_values(["Attendance_Pct", "Internal_Marks"], ascending=[False, False])[cols]
print("Top 5 students by attendance:")
print(by_att.head().to_string(index=False))

# %% (c) Group by department - average attendance and internal marks
dept_summary = (df.groupby("Department")
                  .agg(Students=("Student_ID", "count"),
                       Avg_Attendance=("Attendance_Pct", "mean"),
                       Avg_Internal=("Internal_Marks", "mean"),
                       Min_Internal=("Internal_Marks", "min"),
                       Max_Internal=("Internal_Marks", "max"))
                  .round(2)
                  .sort_values("Avg_Internal", ascending=False))
print("Department-wise summary:")
print(dept_summary)

# %% (d) Rank students on internal marks (overall and within department)
df["Overall_Rank"] = df["Internal_Marks"].rank(ascending=False, method="min").astype(int)
df["Dept_Rank"] = (df.groupby("Department")["Internal_Marks"]
                     .rank(ascending=False, method="min").astype(int))

ranked = df.sort_values("Overall_Rank")[["Overall_Rank", "Student_Name", "Department",
                                          "Internal_Marks", "Dept_Rank"]]
print("Ranking of students by internal marks:")
print(ranked.to_string(index=False))
