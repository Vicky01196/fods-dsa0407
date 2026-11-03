# %% Demonstration - one activity from each library on the student dataset
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import MinMaxScaler

# Pandas - reading, selecting, cleaning
raw = pd.read_csv("data/student_performance_raw.csv")
print("Pandas      : read_csv ->", raw.shape, "| drop_duplicates ->", raw.drop_duplicates().shape)

df = pd.read_csv("data/student_clean.csv")

# NumPy - fast numerical operations on arrays
att = df["Attendance_Pct"].to_numpy()
print("NumPy       : mean attendance =", np.round(np.mean(att), 2),
      "| students >= 75% =", int(np.sum(att >= 75)))

# SciPy - statistical testing
r, p = stats.pearsonr(df["Attendance_Pct"], df["Internal_Marks"])
print(f"SciPy       : pearsonr(attendance, marks) -> r = {r:.3f}, p-value = {p:.5f}")

# Scikit-learn - imputation and scaling for modelling
imputer = SimpleImputer(strategy="median")
filled = imputer.fit_transform(raw[["Attendance_Pct"]])
scaled = MinMaxScaler().fit_transform(df[["Internal_Marks"]])
print("Scikit-learn: SimpleImputer(median) filled", int(raw["Attendance_Pct"].isna().sum()),
      "values | MinMaxScaler range =", (round(float(scaled.min()), 2), round(float(scaled.max()), 2)))

# Matplotlib - visualisation
fig, ax = plt.subplots(figsize=(4, 3))
ax.boxplot(df["Internal_Marks"])
ax.set_title("Internal Marks")
plt.savefig("charts/task8_matplotlib_demo.png", dpi=120)
plt.close()
print("Matplotlib  : box plot saved -> charts/task8_matplotlib_demo.png")
