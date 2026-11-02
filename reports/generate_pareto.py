"""Create a Pareto chart from real entries in docs/DEFECT_CHECKSHEET.csv.

Run after real testing: py reports/generate_pareto.py
The script deliberately refuses to create a chart if no completed defect data exists.
"""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHECKSHEET = ROOT / "docs" / "DEFECT_CHECKSHEET.csv"
OUTPUT = ROOT / "docs" / "PARETO_CHART.png"


def main() -> None:
    import pandas as pd
    import matplotlib.pyplot as plt

    data = pd.read_csv(CHECKSHEET)
    defects = data[(data["pass_fail"].str.upper() == "FAIL") & data["defect_category"].notna()]
    if defects.empty:
        raise SystemExit("No real failed test entries exist. Add evidence before generating a Pareto chart.")
    counts = defects["defect_category"].value_counts()
    cumulative = counts.cumsum() / counts.sum() * 100
    figure, left_axis = plt.subplots(figsize=(9, 5))
    counts.plot(kind="bar", color="#1B874B", ax=left_axis)
    left_axis.set_ylabel("Defect count")
    left_axis.set_xlabel("Defect category")
    right_axis = left_axis.twinx()
    right_axis.plot(range(len(counts)), cumulative, color="#B5780B", marker="o")
    right_axis.set_ylabel("Cumulative percentage")
    right_axis.set_ylim(0, 110)
    right_axis.axhline(80, color="#5E6655", linestyle="--", linewidth=1)
    figure.tight_layout()
    figure.savefig(OUTPUT, dpi=160)
    print(f"Pareto chart saved to {OUTPUT}")


if __name__ == "__main__":
    main()
