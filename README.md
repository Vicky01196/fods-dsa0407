# DSA04 – Assignment 2 (CO2): Student Performance Data Preparation and Visualization Using Python

**Name:** Vigneshwaran B  **Register Number:** 192324022  **Department:** AI & Data Science

The dataset is **synthetic** – all names and values were invented for this assignment. It contains no real student personal information.

## Folder structure

```
StudentPerformance_DSA04/
├── code/
│   ├── task00_create_dataset.py     creates data/student_performance_raw.csv
│   ├── task01_read_inspect.py       Task 1  – reading and inspecting
│   ├── task02_select_filter.py      Task 2  – selection and filtering
│   ├── task03_missing_data.py       Task 3  – missing values (deletion, median/mean, mode)
│   ├── task04_sort_group_rank.py    Task 4  – sorting, grouping, ranking
│   ├── task05_manipulation.py       Task 5  – Pandas/NumPy manipulation -> student_prepared.csv
│   ├── task06_preprocessing.py      Task 6  – full preprocessing workflow -> student_clean.csv
│   ├── task07_visualization.py      Task 7  – bar chart, histogram, scatter plot
│   ├── task08_libraries.py          Task 8  – one activity per library
│   ├── task09_academic_support.py   Task 9  – patterns and support charts
│   ├── task10_case_study.py         Task 10 – integrated case study (stand-alone)
│   ├── flowcharts.py                flowcharts for Tasks 6 and 10
│   └── run_all.py                   runs everything in the correct order
├── data/                            raw, clean, prepared and final CSV files
├── charts/                          all generated charts and flowcharts (PNG)
└── requirements.txt
```

## How to run

From inside the `StudentPerformance_DSA04` folder:

```
pip install -r requirements.txt
python code/run_all.py
```

Run order matters because Tasks 4, 5, 8 and 9 read `data/student_clean.csv` (made by Task 6),
and Tasks 7 and 9 read `data/student_prepared.csv` (made by Task 5). `run_all.py` handles this.
Each script can also be run on its own once the files it needs exist, e.g. `python code/task07_visualization.py`.

The `# %%` comments split each script into the parts shown in the report; they can also be run
cell-by-cell in VS Code or Spyder.

Outputs in the report were produced with Python 3.13, pandas 3.0, NumPy 2.5, SciPy 1.18,
scikit-learn 1.9 and Matplotlib 3.11. With pandas 2.x, text columns are displayed as `object`
instead of `str`; all other results are the same. Matplotlib 3.9 or newer is needed for the
`tick_labels` argument used in the Task 10 box plot.
