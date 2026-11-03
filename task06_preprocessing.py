# %% Step 1 - Read the raw data and detect duplicate records
import numpy as np
import pandas as pd

pd.set_option("display.width", 112)
pd.set_option("display.max_columns", None)

raw = pd.read_csv("data/student_performance_raw.csv")
df = raw.copy()
print("Raw shape:", df.shape)

print("\nExact duplicate rows:", df.duplicated().sum())
print("Repeated Student_IDs :", df.duplicated(subset="Student_ID").sum())
print("\nAll copies of the duplicated records:")
print(df[df.duplicated(keep=False)].sort_values("Student_ID"))

df = df.drop_duplicates(keep="first").reset_index(drop=True)
assert df["Student_ID"].is_unique          # each student now appears once
print("\nShape after removing duplicates:", df.shape)

# %% Step 2 - Standardise inconsistent department names
print("Department values before cleaning:")
print(df["Department"].unique().tolist())

dept_map = {
    "CSE": "CSE", "COMPUTER SCIENCE": "CSE",
    "ECE": "ECE",
    "MECH": "MECH", "MECHANICAL": "MECH",
    "AIDS": "AI&DS", "AI&DS": "AI&DS", "AI & DS": "AI&DS",
}
df["Department"] = df["Department"].str.strip().str.upper().map(dept_map)
assert df["Department"].notna().all()      # every value was matched

print("Department values after cleaning:")
print(sorted(df["Department"].unique()))
print("\nStudents per department:")
print(df["Department"].value_counts())

# %% Step 3 - Correct data types
print("Online_Activity_Hrs before:", df["Online_Activity_Hrs"].tolist()[:6],
      "| dtype:", df["Online_Activity_Hrs"].dtype)

# keep only the numeric part of entries such as '2 hrs' or '5.5 hrs'
df["Online_Activity_Hrs"] = (df["Online_Activity_Hrs"].astype(str)
                             .str.extract(r"(\d+\.?\d*)")[0].astype(float))

num_cols = ["Attendance_Pct", "Internal_Marks", "Assignment_Score", "Online_Activity_Hrs"]
df[num_cols] = df[num_cols].apply(pd.to_numeric, errors="coerce")
df["Department"] = df["Department"].astype("category")

print("Online_Activity_Hrs after :", df["Online_Activity_Hrs"].tolist()[:6],
      "| dtype:", df["Online_Activity_Hrs"].dtype)
print("\nData types after conversion:")
print(df.dtypes)

# %% Step 4 - Validate ranges and treat invalid values
valid_range = {
    "Attendance_Pct": (0, 100),
    "Internal_Marks": (0, 100),
    "Assignment_Score": (0, 50),
    "Online_Activity_Hrs": (0, 40),
}
for col, (low, high) in valid_range.items():
    invalid = df[col].notna() & ~df[col].between(low, high)
    if invalid.any():
        print(f"Invalid values in {col} (allowed {low}-{high}):")
        print(df.loc[invalid, ["Student_ID", "Student_Name", col]].to_string(index=False))
        df.loc[invalid, col] = np.nan      # impossible value -> treated as missing
print("\nMissing values after invalid entries were set to NaN:")
print(df[num_cols].isnull().sum())

# %% Step 5 - Handle missing values
fill_values = {
    "Attendance_Pct": float(df["Attendance_Pct"].median()),
    "Internal_Marks": float(df["Internal_Marks"].median()),
    "Assignment_Score": round(float(df["Assignment_Score"].mean()), 1),
}
print("Fill values:", fill_values)
df = df.fillna(value=fill_values)
print("Remaining missing values:", int(df.isnull().sum().sum()))

# %% Step 6 - Flag unusually high or low (but valid) marks using the IQR rule
q1, q3 = df["Internal_Marks"].quantile([0.25, 0.75])
iqr = q3 - q1
low_fence, high_fence = q1 - 1.5 * iqr, q3 + 1.5 * iqr
print(f"Q1 = {q1}, Q3 = {q3}, IQR = {iqr}, fences = ({low_fence}, {high_fence})")
outliers = ~df["Internal_Marks"].between(low_fence, high_fence)
print("Students outside the IQR fences:", int(outliers.sum()))
print("\nLowest and highest internal marks (kept - they are valid):")
print(df.nsmallest(2, "Internal_Marks")[["Student_ID", "Internal_Marks"]].to_string(index=False))
print(df.nlargest(2, "Internal_Marks")[["Student_ID", "Internal_Marks"]].to_string(index=False))

# %% Step 7 - Final check and save the clean dataset
print("Clean dataset shape:", df.shape)
print(df.to_string(index=False))
df.to_csv("data/student_clean.csv", index=False)
print("\nSaved: data/student_clean.csv")
