# %% (a) Bar chart - average internal marks by department
import matplotlib
matplotlib.use("Agg")                     # render charts to image files
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

df = pd.read_csv("data/student_prepared.csv")
DEPT_COLORS = {"AI&DS": "#2E5A88", "CSE": "#E07B39", "ECE": "#3A9D7A", "MECH": "#8E6BB8"}

avg_marks = df.groupby("Department")["Internal_Marks"].mean().sort_values(ascending=False)
overall = df["Internal_Marks"].mean()
print("Average internal marks by department:")
print(avg_marks.round(2))

fig, ax = plt.subplots(figsize=(7, 4.2))
bars = ax.bar(avg_marks.index, avg_marks.values,
              color=[DEPT_COLORS[d] for d in avg_marks.index], width=0.6, label="Department average")
ax.bar_label(bars, fmt="%.1f", padding=3, fontsize=10)
ax.axhline(overall, color="black", linestyle="--", linewidth=1,
           label=f"Overall average ({overall:.1f})")
ax.set_title("Average Internal Marks by Department", fontsize=13, fontweight="bold")
ax.set_xlabel("Department")
ax.set_ylabel("Average internal marks (out of 100)")
ax.set_ylim(0, 100)
ax.legend(loc="upper right")
ax.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.savefig("charts/task7_bar_avg_marks.png", dpi=200)
plt.close()

# %% (b) Histogram - distribution of attendance percentage
fig, ax = plt.subplots(figsize=(7, 4.2))
bins = np.arange(50, 101, 5)              # 50-55, 55-60, ... , 95-100
counts, edges, _ = ax.hist(df["Attendance_Pct"], bins=bins, color="#2E5A88",
                           edgecolor="white", label="Number of students")
ax.axvline(75, color="#C0392B", linestyle="--", linewidth=1.5, label="75% attendance requirement")
ax.axvline(df["Attendance_Pct"].mean(), color="black", linestyle=":", linewidth=1.5,
           label=f"Mean ({df['Attendance_Pct'].mean():.1f}%)")
ax.set_title("Distribution of Attendance Percentage", fontsize=13, fontweight="bold")
ax.set_xlabel("Attendance (%)")
ax.set_ylabel("Number of students")
ax.set_xticks(bins)
ax.legend(loc="upper left")
ax.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.savefig("charts/task7_hist_attendance.png", dpi=200)
plt.close()

print("Students per attendance band:")
for lo, c in zip(edges[:-1], counts):
    if c:
        print(f"  {lo:.0f}-{lo + 5:.0f}% : {int(c)}")
print("Students below 75% attendance:", int((df["Attendance_Pct"] < 75).sum()))

# %% (c) Scatter plot - attendance vs internal marks
fig, ax = plt.subplots(figsize=(7, 4.6))
for dept, group in df.groupby("Department"):
    ax.scatter(group["Attendance_Pct"], group["Internal_Marks"], s=60,
               color=DEPT_COLORS[dept], edgecolor="black", linewidth=0.5, label=dept)

slope, intercept = np.polyfit(df["Attendance_Pct"], df["Internal_Marks"], 1)   # line of best fit
x_line = np.linspace(df["Attendance_Pct"].min(), df["Attendance_Pct"].max(), 50)
ax.plot(x_line, slope * x_line + intercept, color="grey", linestyle="--", label="Trend line")

r = df["Attendance_Pct"].corr(df["Internal_Marks"])
ax.set_title(f"Attendance vs Internal Marks (r = {r:.2f})", fontsize=13, fontweight="bold")
ax.set_xlabel("Attendance (%)")
ax.set_ylabel("Internal marks (out of 100)")
ax.legend(title="Department", loc="upper left")
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("charts/task7_scatter_att_marks.png", dpi=200)
plt.close()

print(f"Pearson correlation r = {r:.3f}")
print(f"Trend line: Internal_Marks = {slope:.2f} x Attendance_Pct + ({intercept:.2f})")
