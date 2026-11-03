"""Runs every task script in the correct order. Execute from the project folder:
    python code/run_all.py
"""
import subprocess
import sys

ORDER = [
    "task00_create_dataset.py",   # creates data/student_performance_raw.csv
    "task01_read_inspect.py",
    "task02_select_filter.py",
    "task03_missing_data.py",
    "task06_preprocessing.py",    # creates data/student_clean.csv (needed by 4, 5, 7, 8, 9)
    "task04_sort_group_rank.py",
    "task05_manipulation.py",     # creates data/student_prepared.csv (needed by 7, 9)
    "task07_visualization.py",
    "task08_libraries.py",
    "task09_academic_support.py",
    "task10_case_study.py",       # stand-alone: starts again from the raw CSV
    "flowcharts.py",
]

for script in ORDER:
    print("=" * 30, script, "=" * 30)
    result = subprocess.run([sys.executable, f"code/{script}"])
    if result.returncode != 0:
        sys.exit(f"Stopped: {script} failed")
print("\nAll scripts completed. Charts are in charts/, datasets in data/.")
