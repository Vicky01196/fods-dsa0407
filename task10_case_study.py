# %% Step 1 - Read and inspect the raw dataset
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

pd.set_option("display.width", 112)
pd.set_option("display.max_columns", None)

raw = pd.read_csv("data/student_performance_raw.csv")
print("Shape:", raw.shape)
print("\nMissing values:", raw.isnull().sum()[raw.isnull().sum() > 0].to_dict())
print("Duplicate rows:", raw.duplicated().sum())
print("Distinct department labels:", raw["Department"].nunique())
print(sorted(raw["Department"].unique()))
print("Internal_Marks range:", raw["Internal_Marks"].min(), "to", raw["Internal_Marks"].max())
print("Online_Activity_Hrs dtype:", raw["Online_Activity_Hrs"].dtype)

# %% Step 2 - Select the columns needed for analysis
# Student_Name is not needed for analysis -> dropped to keep the analysis anonymous
analysis_cols = ["Student_ID", "Department", "Attendance_Pct", "Internal_Marks",
                 "Assignment_Score", "Online_Activity_Hrs"]
df = raw[analysis_cols].copy()
print("Selected columns:", ", ".join(df.columns))

# %% Step 3 - Clean: duplicates, inconsistent entries, types, invalid values, missing values
log = {}

# 3a. Duplicates (assumption: identical rows are double entries of the same student)
log["duplicates_removed"] = int(df.duplicated().sum())
df = df.drop_duplicates().reset_index(drop=True)

# 3b. Inconsistent department names (assumption: all variants refer to 4 departments)
dept_map = {"CSE": "CSE", "COMPUTER SCIENCE": "CSE", "ECE": "ECE", "MECH": "MECH",
            "MECHANICAL": "MECH", "AIDS": "AI&DS", "AI&DS": "AI&DS", "AI & DS": "AI&DS"}
df["Department"] = df["Department"].str.strip().str.upper().map(dept_map).astype("category")

# 3c. Text hours -> numeric
df["Online_Activity_Hrs"] = df["Online_Activity_Hrs"].str.extract(r"(\d+\.?\d*)")[0].astype(float)

# 3d. Invalid marks (assumption: marks outside 0-100 are data-entry errors)
invalid = ~df["Internal_Marks"].between(0, 100) & df["Internal_Marks"].notna()
log["invalid_marks_set_to_NaN"] = df.loc[invalid, "Student_ID"].tolist()
df.loc[invalid, "Internal_Marks"] = np.nan

# 3e. Missing values (median for attendance/marks, mean for assignment score)
log["missing_before_imputation"] = df.isnull().sum()[df.isnull().sum() > 0].to_dict()
df["Attendance_Pct"] = df["Attendance_Pct"].fillna(df["Attendance_Pct"].median())
df["Internal_Marks"] = df["Internal_Marks"].fillna(df["Internal_Marks"].median())
df["Assignment_Score"] = df["Assignment_Score"].fillna(round(df["Assignment_Score"].mean(), 1))

for k, v in log.items():
    print(f"{k:28}: {v}")
print("Clean shape:", df.shape, "| missing values left:", int(df.isnull().sum().sum()))

# %% Step 4 - Derived measures
df["Percentage"] = ((df["Internal_Marks"] + df["Assignment_Score"]) / 150 * 100).round(2)
df["At_Risk"] = np.where((df["Attendance_Pct"] < 75) & (df["Internal_Marks"] < 50), "Yes", "No")
print(df.head().to_string(index=False))

# %% Step 5 - Grouping, sorting and ranking summaries
summary = (df.groupby("Department", observed=True)
             .agg(Students=("Student_ID", "count"),
                  Avg_Attendance=("Attendance_Pct", "mean"),
                  Avg_Internal=("Internal_Marks", "mean"),
                  Avg_Percentage=("Percentage", "mean"),
                  At_Risk=("At_Risk", lambda s: (s == "Yes").sum()))
             .round(2)
             .sort_values("Avg_Percentage", ascending=False))
print("Department summary (sorted by average percentage):")
print(summary)

df["Rank"] = df["Percentage"].rank(ascending=False, method="min").astype(int)
print("\nTop 5 students by overall percentage:")
top5 = df.nsmallest(5, "Rank")[["Rank", "Student_ID", "Department", "Percentage"]]
print(top5.to_string(index=False))
print("\nBottom 5 students by overall percentage:")
print(df.nlargest(5, "Rank")[["Rank", "Student_ID", "Department", "Attendance_Pct",
                              "Percentage", "At_Risk"]].to_string(index=False))

# %% Step 6 - Visualisation 1: department labels before and after cleaning
before = raw["Department"].value_counts()
after = df["Department"].value_counts().reindex(["CSE", "ECE", "MECH", "AI&DS"])

fig, axes = plt.subplots(1, 2, figsize=(9, 3.8), gridspec_kw={"width_ratios": [1.6, 1]})
axes[0].barh([repr(s) for s in before.index[::-1]], before.values[::-1], color="#B0B7C3")
axes[0].set_title("Before cleaning: 11 labels", fontweight="bold")
axes[0].set_xlabel("Number of rows")
b = axes[1].bar(after.index, after.values, color=["#E07B39", "#3A9D7A", "#8E6BB8", "#2E5A88"])
axes[1].bar_label(b, padding=2)
axes[1].set_title("After cleaning: 4 departments", fontweight="bold")
axes[1].set_ylabel("Number of students")
axes[1].set_ylim(0, 6.5)
fig.suptitle("Effect of Standardising Department Names", fontsize=13, fontweight="bold")
plt.tight_layout()
plt.savefig("charts/task10_dept_before_after.png", dpi=200)
plt.close()

# %% Step 7 - Visualisation 2: box plot of overall percentage by department
order = summary.index.tolist()
data = [df.loc[df["Department"] == d, "Percentage"] for d in order]
fig, ax = plt.subplots(figsize=(7, 4.3))
bp = ax.boxplot(data, tick_labels=order, patch_artist=True, widths=0.5)
for patch, color in zip(bp["boxes"], ["#2E5A88", "#E07B39", "#3A9D7A", "#8E6BB8"]):
    patch.set_facecolor(color)
    patch.set_alpha(0.75)
for i, d in enumerate(data, start=1):
    ax.scatter(np.full(len(d), i), d, color="black", s=14, zorder=3)
ax.axhline(50, color="#C0392B", linestyle="--", linewidth=1, label="50% (minimum expected)")
ax.set_title("Spread of Overall Percentage by Department", fontsize=13, fontweight="bold")
ax.set_xlabel("Department")
ax.set_ylabel("Overall percentage (%)")
ax.legend(loc="lower left")
ax.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.savefig("charts/task10_boxplot_percentage.png", dpi=200)
plt.close()

# %% Step 8 - Visualisation 3: online activity vs overall percentage
fig, ax = plt.subplots(figsize=(7, 4.3))
for flag, color, label in [("No", "#2E5A88", "Not at risk"), ("Yes", "#C0392B", "At risk")]:
    part = df[df["At_Risk"] == flag]
    ax.scatter(part["Online_Activity_Hrs"], part["Percentage"], s=65, color=color,
               edgecolor="black", linewidth=0.5, label=label)
r = df["Online_Activity_Hrs"].corr(df["Percentage"])
ax.set_title(f"Online Learning Activity vs Overall Percentage (r = {r:.2f})",
             fontsize=12, fontweight="bold")
ax.set_xlabel("Online learning activity (hours per week)")
ax.set_ylabel("Overall percentage (%)")
ax.legend(loc="upper left")
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("charts/task10_online_vs_percentage.png", dpi=200)
plt.close()
print(f"Correlation between online hours and percentage: r = {r:.3f}")

# %% Step 9 - Save the final analysis-ready dataset
df.to_csv("data/student_case_study_final.csv", index=False)
print("Saved: data/student_case_study_final.csv | shape:", df.shape)
