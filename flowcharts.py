"""Draws the labelled preprocessing flowcharts for Task 6 and Task 10 using Matplotlib."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

COLORS = {"io": "#DCE6F2", "process": "#FFFFFF", "decision": "#FDEBD0", "output": "#D5F0E3"}


def box(ax, x, y, w, h, text, kind="process", title=None):
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                                boxstyle="round,pad=0.02,rounding_size=0.08",
                                facecolor=COLORS[kind], edgecolor="#1F3B57", linewidth=1.3))
    if title:
        ax.text(x, y + h * 0.18, title, ha="center", va="center", fontsize=9.5, fontweight="bold")
        ax.text(x, y - h * 0.2, text, ha="center", va="center", fontsize=8)
    else:
        ax.text(x, y, text, ha="center", va="center", fontsize=9)


def arrow(ax, x1, y1, x2, y2):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=14,
                                 color="#1F3B57", linewidth=1.3))


def task6_flowchart(path):
    steps = [
        ("io", "START: Read raw CSV", "pd.read_csv() - 20 rows x 7 columns"),
        ("process", "1. Detect & remove duplicates", "duplicated(), drop_duplicates() -> 18 rows"),
        ("process", "2. Standardise department names", "strip() + upper() + map() -> 4 departments"),
        ("process", "3. Correct data types", "str.extract() -> float; Department -> category"),
        ("decision", "4. Validate value ranges", "Marks outside 0-100 (112, -4) -> NaN"),
        ("process", "5. Handle missing values", "Median: attendance, marks | Mean: assignment"),
        ("decision", "6. Check unusual marks (IQR)", "Valid extremes (18, 97) kept & reported"),
        ("output", "END: Save clean dataset", "student_clean.csv - 18 rows, 0 missing"),
    ]
    fig, ax = plt.subplots(figsize=(6.2, 9.2))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, len(steps) * 1.15 + 0.3)
    ax.axis("off")
    w, h = 7.4, 0.8
    ys = [len(steps) * 1.15 - i * 1.15 - 0.3 for i in range(len(steps))]
    for (kind, title, text), y in zip(steps, ys):
        box(ax, 5, y, w, h, text, kind, title)
    for y1, y2 in zip(ys[:-1], ys[1:]):
        arrow(ax, 5, y1 - h / 2, 5, y2 + h / 2)
    ax.set_title("Task 6 - Student Data Preprocessing Workflow", fontsize=12, fontweight="bold")
    plt.tight_layout()
    plt.savefig(path, dpi=200)
    plt.close()


def task10_flowchart(path):
    fig, ax = plt.subplots(figsize=(9.5, 7.6))
    ax.set_xlim(0, 15)
    ax.set_ylim(0, 12)
    ax.axis("off")
    w, h = 4.3, 1.15
    col = [2.6, 7.5, 12.4]
    # Stage A - Read & inspect (left column, top to bottom)
    a = [("io", "Read", "read_csv(raw CSV)"),
         ("process", "Inspect", "shape, dtypes, isnull,\nduplicated, unique"),
         ("process", "Select", "keep 6 analysis columns\n(drop Student_Name)")]
    # Stage B - Clean (middle column)
    b = [("process", "Remove duplicates", "drop_duplicates(): 20 -> 18"),
         ("process", "Fix inconsistent entries", "11 labels -> 4 departments;\n'2 hrs' -> 2.0"),
         ("decision", "Validate & impute", "invalid marks -> NaN;\nmedian / mean fill")]
    # Stage C - Analyse & present (right column)
    c = [("process", "Derive measures", "Percentage, At_Risk flag"),
         ("process", "Group, sort, rank", "dept summary, top/bottom 5"),
         ("output", "Visualise & decide", "bar, box, scatter plots ->\nsupport actions")]
    ys = [9.6, 6.9, 4.2]
    for x, stage in zip(col, [a, b, c]):
        for (kind, title, text), y in zip(stage, ys):
            box(ax, x, y, w, h, text, kind, title)
        for y1, y2 in zip(ys[:-1], ys[1:]):
            arrow(ax, x, y1 - h / 2, x, y2 + h / 2)
    # connectors between stages
    for x1, x2 in [(col[0], col[1]), (col[1], col[2])]:
        gap = (x1 + w / 2 + x2 - w / 2) / 2          # elbow connector through the gap
        ax.plot([x1 + w / 2, gap, gap], [ys[2], ys[2], ys[0]], color="#1F3B57", linewidth=1.3)
        arrow(ax, gap, ys[0], x2 - w / 2, ys[0])
    for x, label in zip(col, ["A. Read & Inspect", "B. Clean", "C. Analyse & Present"]):
        ax.text(x, 11.1, label, ha="center", fontsize=11, fontweight="bold", color="#1F3B57")
    # outputs strip
    box(ax, 7.5, 1.6, 13.5, 1.2,
        "student_case_study_final.csv  |  department summary  |  at-risk list  |  3 charts  ->  faculty decisions",
        "output", "Deliverables")
    arrow(ax, col[2], ys[2] - h / 2, col[2], 1.6 + 0.6)
    # legend
    for i, (k, lab) in enumerate([("io", "Input"), ("process", "Process"),
                                  ("decision", "Decision / check"), ("output", "Output")]):
        ax.add_patch(FancyBboxPatch((0.4 + i * 3.6, 0.1), 0.45, 0.35, boxstyle="round,pad=0.02",
                                    facecolor=COLORS[k], edgecolor="#1F3B57"))
        ax.text(1.0 + i * 3.6, 0.27, lab, va="center", fontsize=8.5)
    ax.set_title("Task 10 - Integrated Preprocessing and Visualisation Workflow",
                 fontsize=13, fontweight="bold")
    plt.tight_layout()
    plt.savefig(path, dpi=200)
    plt.close()


if __name__ == "__main__":
    task6_flowchart("charts/task6_flowchart.png")
    task10_flowchart("charts/task10_flowchart.png")
    print("Flowcharts saved in charts/")
