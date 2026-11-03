# %% (a) Convert inconsistent values and data types (raw data)
import numpy as np
import pandas as pd

pd.set_option("display.width", 112)
pd.set_option("display.max_columns", None)

raw = pd.read_csv("data/student_performance_raw.csv")
print("Before conversion:")
print(raw[["Student_ID", "Department", "Online_Activity_Hrs"]].head(6).to_string(index=False))
print("\ndtypes before:", raw[["Department", "Online_Activity_Hrs"]].dtypes.astype(str).to_dict())

converted = raw.copy()

# 1. Text -> number: '2 hrs' -> 2.0, '5.5 hrs' -> 5.5, '6.5' -> 6.5
converted["Online_Activity_Hrs"] = (converted["Online_Activity_Hrs"]
                                    .str.replace("hrs", "", regex=False)
                                    .str.strip()
                                    .astype(float))

# 2. Inconsistent labels -> one standard label, stored as a category
dept_map = {"CSE": "CSE", "COMPUTER SCIENCE": "CSE", "ECE": "ECE",
            "MECH": "MECH", "MECHANICAL": "MECH",
            "AIDS": "AI&DS", "AI&DS": "AI&DS", "AI & DS": "AI&DS"}
converted["Department"] = (converted["Department"].str.strip().str.upper()
                           .map(dept_map).astype("category"))

print("\nAfter conversion:")
print(converted[["Student_ID", "Department", "Online_Activity_Hrs"]].head(6).to_string(index=False))
print("\ndtypes after :", converted[["Department", "Online_Activity_Hrs"]].dtypes.astype(str).to_dict())
print("Department categories:", list(converted["Department"].cat.categories))
print("Mean online activity (now computable):",
      round(converted["Online_Activity_Hrs"].mean(), 2), "hrs/week")

# %% (b) Pandas - derived measures on the clean dataset
df = pd.read_csv("data/student_clean.csv")

# Total_Assessment = Internal_Marks (out of 100) + Assignment_Score (out of 50) -> out of 150
df["Total_Assessment"] = df["Internal_Marks"] + df["Assignment_Score"]
# Percentage = Total_Assessment / 150 x 100
df["Percentage"] = (df["Total_Assessment"] / 150 * 100).round(2)

print(df[["Student_ID", "Internal_Marks", "Assignment_Score",
          "Total_Assessment", "Percentage"]].head(8).to_string(index=False))

# %% (c) NumPy - numerical operations
marks = df["Internal_Marks"].to_numpy()

# 1. z-score standardisation: z = (x - mean) / std
df["Marks_ZScore"] = np.round((marks - np.mean(marks)) / np.std(marks), 2)

# 2. Performance band using np.select
conditions = [df["Percentage"] >= 75, df["Percentage"] >= 50]
df["Performance_Band"] = np.select(conditions, ["High", "Medium"], default="Low")

# 3. At-risk flag using np.where (low attendance AND low internal marks)
df["At_Risk"] = np.where((df["Attendance_Pct"] < 75) & (df["Internal_Marks"] < 50), "Yes", "No")

# 4. Correlation coefficient between attendance and internal marks
r = np.corrcoef(df["Attendance_Pct"], df["Internal_Marks"])[0, 1]

print(f"Mean internal marks = {np.mean(marks):.2f}, Std = {np.std(marks):.2f}")
print(f"Correlation (attendance vs internal marks) = {r:.3f}")
print()
print(df[["Student_ID", "Attendance_Pct", "Internal_Marks", "Percentage",
          "Marks_ZScore", "Performance_Band", "At_Risk"]].to_string(index=False))

# %% (d) Save the prepared dataset for visualisation
df.to_csv("data/student_prepared.csv", index=False)
print("Saved: data/student_prepared.csv  | shape:", df.shape)
print(df["Performance_Band"].value_counts())
