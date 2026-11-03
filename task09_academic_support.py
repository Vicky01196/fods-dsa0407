# %% Pattern 1 - Low attendance is linked with low internal marks
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

pd.set_option("display.width", 112)
pd.set_option("display.max_columns", None)

df = pd.read_csv("data/student_prepared.csv")
df["Attendance_Group"] = np.where(df["Attendance_Pct"] < 75, "Below 75%", "75% and above")

group_summary = (df.groupby("Attendance_Group")
                   .agg(Students=("Student_ID", "count"),
                        Avg_Attendance=("Attendance_Pct", "mean"),
                        Avg_Internal=("Internal_Marks", "mean"),
                        Avg_Percentage=("Percentage", "mean"))
                   .round(2))
print("Performance by attendance group:")
print(group_summary)

r, p = stats.pearsonr(df["Attendance_Pct"], df["Internal_Marks"])
print(f"\nPearson r = {r:.3f}  (p-value = {p:.5f})")

at_risk = df[df["At_Risk"] == "Yes"].sort_values("Internal_Marks")
print("\nStudents flagged At-Risk (attendance < 75% and internal marks < 50):")
print(at_risk[["Student_ID", "Student_Name", "Department", "Attendance_Pct",
               "Internal_Marks", "Online_Activity_Hrs", "Performance_Band"]].to_string(index=False))

# Quadrant scatter plot for faculty
fig, ax = plt.subplots(figsize=(7.2, 4.8))
colors = np.where(df["At_Risk"] == "Yes", "#C0392B", "#2E5A88")
ax.scatter(df["Attendance_Pct"], df["Internal_Marks"], c=colors, s=70,
           edgecolor="black", linewidth=0.5)
ax.axvline(75, color="grey", linestyle="--", linewidth=1)
ax.axhline(50, color="grey", linestyle="--", linewidth=1)
ax.axvspan(50, 75, ymin=0, ymax=0.5, color="#C0392B", alpha=0.08)
for _, row in at_risk.iterrows():
    ax.annotate(row["Student_ID"], (row["Attendance_Pct"], row["Internal_Marks"]),
                textcoords="offset points", xytext=(6, -3), fontsize=9)
ax.text(51, 3, "Support zone:\nattendance < 75% and marks < 50", fontsize=9, color="#C0392B")
ax.scatter([], [], c="#C0392B", s=70, edgecolor="black", label="At-risk student")
ax.scatter([], [], c="#2E5A88", s=70, edgecolor="black", label="Other student")
ax.set_xlim(50, 100)
ax.set_ylim(0, 100)
ax.set_title("Identifying Students Who Need Academic Support", fontsize=13, fontweight="bold")
ax.set_xlabel("Attendance (%)")
ax.set_ylabel("Internal marks (out of 100)")
ax.legend(loc="upper left")
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("charts/task9_support_quadrant.png", dpi=200)
plt.close()

# %% Pattern 2 - Differences in department averages
dept = (df.groupby("Department")
          .agg(Avg_Attendance=("Attendance_Pct", "mean"),
               Avg_Internal=("Internal_Marks", "mean"),
               Avg_Assignment_Pct=("Assignment_Score", lambda s: s.mean() / 50 * 100),
               At_Risk_Count=("At_Risk", lambda s: (s == "Yes").sum()))
          .round(2)
          .sort_values("Avg_Internal", ascending=False))
print("Department comparison (assignment converted to %):")
print(dept)

fig, ax = plt.subplots(figsize=(7.2, 4.4))
x = np.arange(len(dept))
w = 0.26
metrics = [("Avg_Attendance", "Attendance %", "#2E5A88"),
           ("Avg_Internal", "Internal marks", "#E07B39"),
           ("Avg_Assignment_Pct", "Assignment %", "#3A9D7A")]
for i, (col, label, color) in enumerate(metrics):
    b = ax.bar(x + (i - 1) * w, dept[col], w, label=label, color=color)
    ax.bar_label(b, fmt="%.0f", fontsize=8, padding=2)
ax.set_xticks(x, dept.index)
ax.set_ylim(0, 105)
ax.set_title("Department-wise Comparison of Academic Indicators", fontsize=13, fontweight="bold")
ax.set_xlabel("Department")
ax.set_ylabel("Average score (%)")
ax.legend(loc="upper right", ncol=3, fontsize=9)
ax.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.savefig("charts/task9_department_comparison.png", dpi=200)
plt.close()

# %% Pattern 3 - Online learning activity and overall performance
df["Engagement"] = np.where(df["Online_Activity_Hrs"] < 3,
                            "Low (< 3 hrs/week)", "Regular (>= 3 hrs/week)")
engagement = (df.groupby("Engagement")
                .agg(Students=("Student_ID", "count"),
                     Avg_Online_Hrs=("Online_Activity_Hrs", "mean"),
                     Avg_Percentage=("Percentage", "mean"))
                .round(2))
print("Overall percentage by online learning engagement:")
print(engagement)
r2, p2 = stats.pearsonr(df["Online_Activity_Hrs"], df["Percentage"])
print(f"\nPearson r (online hours vs percentage) = {r2:.3f}  (p-value = {p2:.5f})")
