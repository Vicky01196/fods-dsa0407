# %% Create the synthetic raw student performance dataset
# NOTE: All names and values are SYNTHETIC (invented for this assignment).
# No real student personal information is used.
import numpy as np
import pandas as pd

columns = ["Student_ID", "Student_Name", "Department", "Attendance_Pct",
           "Internal_Marks", "Assignment_Score", "Online_Activity_Hrs"]

# Internal_Marks out of 100, Assignment_Score out of 50,
# Online_Activity_Hrs = average LMS hours per week (stored as text, as exported)
records = [
    ("S101", "Arjun Mehta",     "CSE",              92,     88,     46,     "6.5"),
    ("S102", "Divya Ramesh",    "cse",              68,     42,     30,     "2 hrs"),
    ("S103", "Karthik Raja",    "ECE",              81,     74,     40,     "5"),
    ("S104", "Priya Nair",      "Computer Science", np.nan, 79,     42,     "4.5"),
    ("S105", "Rahul Verma",     "MECH",             59,     35,     22,     "1.5"),
    ("S106", "Sneha Iyer",      "ECE ",             88,     np.nan, 44,     "5.5 hrs"),
    ("S107", "Vikram Singh",    "Mechanical",       76,     61,     np.nan, "3"),
    ("S108", "Ananya Das",      "AIDS",             95,     112,    48,     "7"),
    ("S109", "Mohammed Faiz",   "AI&DS",            72,     48,     28,     "2.5"),
    ("S103", "Karthik Raja",    "ECE",              81,     74,     40,     "5"),
    ("S110", "Lakshmi Prasad",  "ECE",              np.nan, 66,     35,     "4 hrs"),
    ("S111", "Rohan Gupta",     "CSE",              84,     71,     38,     "5"),
    ("S112", "Meera Krishnan",  "mech",             64,     30,     20,     "1"),
    ("S113", "Aditya Rao",      "AI & DS",          90,     85,     np.nan, "6"),
    ("S114", "Kavya Menon",     "ECE",              79,     -4,     36,     "3.5"),
    ("S115", "Siddharth Jain",  "CSE",              70,     np.nan, 25,     "2"),
    ("S116", "Nithya Suresh",   "MECH",             np.nan, 58,     33,     "3 hrs"),
    ("S117", "Harish Kumar",    "AIDS",             86,     97,     47,     "8"),
    ("S118", "Pooja Shetty",    "ECE",              55,     18,     15,     "0.5"),
    ("S111", "Rohan Gupta",     "CSE",              84,     71,     38,     "5"),
]

raw = pd.DataFrame(records, columns=columns)
raw.to_csv("data/student_performance_raw.csv", index=False)
print("Raw dataset saved: data/student_performance_raw.csv")
print("Shape:", raw.shape)
