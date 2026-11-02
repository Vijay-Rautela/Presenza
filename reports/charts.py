"""Matplotlib report charts generated from real reporting data."""

from pathlib import Path

from config import PROJECT_ROOT, COLORS


def subject_attendance_chart(rows: list[dict]) -> Path:
    """Save a real subject-percentage bar chart and return its file path."""
    if not rows:
        raise ValueError("No subject data is available for a chart.")
    import matplotlib.pyplot as plt

    output_dir = PROJECT_ROOT / "reports" / "generated"
    output_dir.mkdir(parents=True, exist_ok=True)
    output = output_dir / "subject_attendance.png"
    labels = [row.get("code", row.get("subject", "Subject")) for row in rows]
    values = [row["percentage"] for row in rows]
    figure, axis = plt.subplots(figsize=(8, 4.5))
    figure.patch.set_facecolor(COLORS["background"]); axis.set_facecolor(COLORS["surface"])
    axis.bar(labels, values, color=COLORS["primary"])
    axis.axhline(75, color=COLORS["accent"], linewidth=1.5, label="75% reference")
    axis.set_ylim(0, 100); axis.set_ylabel("Attendance percentage"); axis.set_title("Attendance by subject")
    axis.legend(); figure.tight_layout(); figure.savefig(output, dpi=160); plt.close(figure)
    return output
