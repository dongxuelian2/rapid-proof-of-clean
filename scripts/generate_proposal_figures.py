"""Generate submission figures from repository evidence."""

from __future__ import annotations

import csv
import json
import shutil
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

ROOT = Path(__file__).resolve().parents[1]
FIGURES = ROOT / "figures"
PROPOSAL_FIGURES = ROOT / "proposal" / "figures"


def save(fig: plt.Figure, stem: str) -> None:
    FIGURES.mkdir(parents=True, exist_ok=True)
    PROPOSAL_FIGURES.mkdir(parents=True, exist_ok=True)
    for suffix in ("png", "svg"):
        path = FIGURES / f"{stem}.{suffix}"
        fig.savefig(path, dpi=220, bbox_inches="tight")
        if suffix == "svg":
            normalized = "\n".join(
                line.rstrip() for line in path.read_text(encoding="utf-8").splitlines()
            )
            path.write_text(normalized + "\n", encoding="utf-8")
        shutil.copyfile(path, PROPOSAL_FIGURES / path.name)
    plt.close(fig)


def workflow() -> None:
    fig, ax = plt.subplots(figsize=(12, 4.8))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 5)
    ax.axis("off")
    boxes = [
        (0.3, 2.0, "3 references +\ndated anchor", "#dbeafe"),
        (2.5, 2.0, "adaptive 2→36\n(60 diagnostic)", "#e0e7ff"),
        (4.8, 2.0, "bounded transfer\ninference", "#ede9fe"),
        (7.2, 2.0, "PASS / FLAG /\nUNKNOWN", "#fef3c7"),
        (9.7, 2.0, "coverage log +\naction", "#dcfce7"),
    ]
    for x, y, label, color in boxes:
        ax.add_patch(
            FancyBboxPatch(
                (x, y),
                1.8,
                1.0,
                boxstyle="round,pad=0.08",
                facecolor=color,
                edgecolor="#334155",
                linewidth=1.4,
            )
        )
        ax.text(x + 0.9, y + 0.5, label, ha="center", va="center", fontsize=10)
    for x in (2.1, 4.4, 6.8, 9.3):
        ax.add_patch(FancyArrowPatch((x, 2.5), (x + 0.35, 2.5), arrowstyle="->", mutation_scale=14))
    ax.text(
        8.1,
        1.2,
        "UNKNOWN → correct setup → reacquire → orthogonal test",
        ha="center",
        fontsize=10,
        color="#7c2d12",
    )
    ax.add_patch(
        FancyArrowPatch(
            (10.6, 1.95), (8.2, 1.45), arrowstyle="->", mutation_scale=14, color="#7c2d12"
        )
    )
    ax.set_title("Reference-guarded active-reflectance workflow", fontsize=16, weight="bold")
    ax.text(
        6,
        0.3,
        "Concept architecture — physical workflow not yet validated",
        ha="center",
        fontsize=10,
        style="italic",
    )
    save(fig, "figure1_workflow")


def failure_comparison() -> None:
    data = json.loads(
        (ROOT / "experiments" / "results" / "final_research_results.json").read_text(
            encoding="utf-8"
        )
    )
    selected = {
        row["policy"]: 100 * row["observable_dirty_false_clean_rate"]
        for row in data["summary"]
    }
    policies = ["fast_20", "fixed_v2_1", "adaptive_standard", "conservative_60"]
    labels = ["Fast 20", "Fixed v2.1\n44 max", "Adaptive v2.2\n36 PASS", "Conservative\n60"]
    fig, ax = plt.subplots(figsize=(9, 5))
    values = [selected[policy] for policy in policies]
    colors = ["#dc2626", "#f59e0b", "#2563eb", "#64748b"]
    bars = ax.bar(labels, values, color=colors)
    ax.bar_label(bars, labels=[f"{value:.2f}%" for value in values], padding=3)
    ax.set_ylim(0, 14)
    ax.set_ylabel("Observable-dirty FOV false-clean (%)")
    ax.set_title("Domain-shift policy comparison — SYNTHETIC ONLY", weight="bold")
    ax.grid(axis="y", alpha=0.25)
    ax.text(
        1.5,
        -3.0,
        "Constructed response/morphology distribution; not field prevalence.\n"
        "Observation-matched residue remains 100% false-clean for every policy.",
        ha="center",
        fontsize=9,
    )
    save(fig, "figure2_synthetic_failure_comparison")


def coverage_time() -> None:
    with (ROOT / "experiments" / "results" / "adaptive_coverage_time_model.csv").open(
        encoding="utf-8"
    ) as handle:
        rows = list(csv.DictReader(handle))
    targets = ["1m2", "5m2", "12m2", "25m2"]
    labels = ["1 m²", "5 m²", "12 m²", "25 m²"]
    budgets = {
        "expected_valid_synthetic_mix": ("synthetic-mix mean", "#16a34a"),
        "clean_pass_certificate": ("clean PASS: 36 frames", "#2563eb"),
        "p95_valid_synthetic_mix": ("p95: 60 frames", "#dc2626"),
    }
    fig, ax = plt.subplots(figsize=(9, 5.4))
    for budget, (label, color) in budgets.items():
        values = [
            float(
                next(
                    row
                    for row in rows
                    if row["profile"] == "conservative"
                    and row["target"] == target
                    and row["budget_label"] == budget
                )["total_minutes"]
            )
            for target in targets
        ]
        ax.plot(labels, values, marker="o", linewidth=2.2, label=label, color=color)
    ax.axhline(30, linestyle="--", color="#111827", linewidth=1.5, label="30-minute objective")
    ax.set_ylabel("Modeled total time (minutes)")
    ax.set_title("Coverage/time scenarios — ASSUMPTIONS, NOT MEASUREMENTS", weight="bold")
    ax.set_ylim(0, 35)
    ax.grid(axis="y", alpha=0.25)
    ax.legend(frameon=False, ncol=2)
    ax.text(
        1.5,
        -7,
        "Conservative input profile; visible target area and inaccessible fraction included.\n"
        "Frame switching, hardware timing and operator performance are unmeasured.",
        ha="center",
        fontsize=9,
    )
    save(fig, "figure3_coverage_time_model")


def main() -> int:
    workflow()
    failure_comparison()
    coverage_time()
    print("Generated three proposal figures in PNG and SVG")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
