# %% (a) Identify missing values and report the count for each column
import pandas as pd

pd.set_option("display.width", 112)
pd.set_option("display.max_columns", None)

df = pd.read_csv("data/student_performance_raw.csv")

missing_summary = pd.DataFrame({
    "Missing_Count": df.isnull().sum(),
    "Missing_%": (df.isnull().mean() * 100).round(2),
})
print("Missing-value summary:")
print(missing_summary)
print("\nTotal missing cells:", int(df.isnull().sum().sum()))

print("\nRecords that contain at least one missing value:")
print(df[df.isnull().any(axis=1)])

# %% (b) Method 1 - Deletion (listwise deletion with dropna)
df_deleted = df.dropna()
print("Rows before deletion:", len(df))
print("Rows after deletion :", len(df_deleted))
print("Rows lost           :", len(df) - len(df_deleted),
      f"({(len(df) - len(df_deleted)) / len(df) * 100:.1f}% of the data)")

# %% (c) Method 2 - Replacement using median / mean
df_imputed = df.copy()

att_median = df_imputed["Attendance_Pct"].median()      # robust to skew
marks_median = df_imputed["Internal_Marks"].median()    # robust to extreme marks (112, -4)
assign_mean = round(df_imputed["Assignment_Score"].mean(), 1)  # no extreme values

df_imputed["Attendance_Pct"] = df_imputed["Attendance_Pct"].fillna(att_median)
df_imputed["Internal_Marks"] = df_imputed["Internal_Marks"].fillna(marks_median)
df_imputed["Assignment_Score"] = df_imputed["Assignment_Score"].fillna(assign_mean)

print("Values used for replacement:")
print(f"  Attendance_Pct   -> median = {att_median}")
print(f"  Internal_Marks   -> median = {marks_median}")
print(f"  Assignment_Score -> mean   = {assign_mean}")
print("\nMissing values after imputation:")
print(df_imputed.isnull().sum())

# %% (d) Method 3 (for reference) - Mode replacement for a categorical column
dept_mode = df["Department"].mode()[0]
print("Mode of Department (would be used if a department were missing):", dept_mode)

# %% (e) Compare the dataset before and after treatment
treated_rows = df.isnull().any(axis=1)
show = ["Student_ID", "Attendance_Pct", "Internal_Marks", "Assignment_Score"]
print("Treated records - BEFORE:")
print(df.loc[treated_rows, show])
print("\nTreated records - AFTER (imputation):")
print(df_imputed.loc[treated_rows, show])

cols = ["Attendance_Pct", "Internal_Marks", "Assignment_Score"]
counts = pd.DataFrame({"Before": df[cols].count(),
                       "After_Deletion": df_deleted[cols].count(),
                       "After_Imputation": df_imputed[cols].count()})
stats = pd.DataFrame({"Mean_Before": df[cols].mean(),
                      "Mean_Deleted": df_deleted[cols].mean(),
                      "Mean_Imputed": df_imputed[cols].mean(),
                      "Std_Before": df[cols].std(),
                      "Std_Imputed": df_imputed[cols].std()}).round(2)
print("\nNumber of usable values per column:")
print(counts)
print("\nMean and standard deviation before and after treatment:")
print(stats)
