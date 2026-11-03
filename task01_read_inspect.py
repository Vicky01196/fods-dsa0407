# %% (a) Read the CSV file into a DataFrame
import pandas as pd

pd.set_option("display.width", 112)        # wider console output
pd.set_option("display.max_columns", None)  # show every column

df = pd.read_csv("data/student_performance_raw.csv")
print("Dataset loaded successfully.")
print("\nFirst five records:")
print(df.head())

# %% (b) Last five records
print("Last five records:")
print(df.tail())

# %% (c) Dimensions, column names and data types
print("Dataset dimensions (rows, columns):", df.shape)
print("\nColumn names:")
print(", ".join(df.columns))
print("\nData types:")
print(df.dtypes)

# %% (d) Identify numerical and categorical columns
numerical_cols = df.select_dtypes(include="number").columns.tolist()
categorical_cols = df.select_dtypes(exclude="number").columns.tolist()
print("Numerical columns  :", numerical_cols)
print("Categorical columns:", categorical_cols)

print("\nUnique values in Department:")
print(df["Department"].unique().tolist())

# %% (e) Quick data-quality checks for the analysis
print("Missing values per column:")
print(df.isnull().sum())
print("\nNumber of exact duplicate rows:", df.duplicated().sum())
print("\nSummary statistics of numerical columns:")
print(df.describe().round(2))
print("\nSample Online_Activity_Hrs values:", df["Online_Activity_Hrs"].unique()[:6].tolist())
