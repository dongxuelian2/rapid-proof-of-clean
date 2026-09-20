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
        (0.3, 2.0, "3 clean\nreferences", "#dbeafe"),
        (2.5, 2.0, "96-frame\ntwo-state view", "#e0e7ff"),
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
        (ROOT / "experiments" / "results" / "phase1_results.json").read_text(encoding="utf-8")
    )
    failures = [
        "dirty_reference",
        "uniform_absorber",
        "optically_invisible_residue",
        "negative_blur_cancellation",
    ]

    def value(method: str, failure: str) -> float:
        row = next(
            item
            for item in data["failure_aggregate"]
            if item["method"] == method and item["failure_mode"] == failure
        )
        return 100 * row["false_clean_rate"]

    v0 = [value("v0_single_reference", item) for item in failures]
    v1 = [value("v1_retained", item) for item in failures]
    labels = [
        "Dirty\nreference",
        "Uniform\nabsorber",
        "Optically\ninvisible",
        "Geometry\ncancellation",
    ]
    fig, ax = plt.subplots(figsize=(9, 5))
    x = range(len(failures))
    ax.bar([i - 0.19 for i in x], v0, width=0.38, label="v0", color="#94a3b8")
    ax.bar([i + 0.19 for i in x], v1, width=0.38, label="retained v1", color="#2563eb")
    ax.set_xticks(list(x), labels)
    ax.set_ylim(0, 112)
    ax.set_ylabel("Proxy-PASS pixels in positive construction (%)")
    ax.set_title("Adversarial false-clean constructions — SYNTHETIC ONLY", weight="bold")
    ax.legend(frameon=False)
    ax.grid(axis="y", alpha=0.25)
    ax.text(
        1.5,
        -26,
        "Fixed toy-model scenes; pixels are descriptive, not independent trials.\n"
        "100% remains for an optically invisible construction.",
        ha="center",
        fontsize=9,
    )
    save(fig, "figure2_synthetic_failure_comparison")


def coverage_time() -> None:
    with (ROOT / "experiments" / "results" / "coverage_time_model.csv").open(
        encoding="utf-8"
    ) as handle:
        rows = list(csv.DictReader(handle))
    targets = [
        "work_surface_1m2",
        "high_touch_set_4m2",
        "prep_zone_5m2",
        "small_room_targets_12m2",
        "large_room_targets_25m2",
    ]
    labels = [
        "1 m²\nwork",
        "4 m²\nhigh-touch",
        "5 m²\nprep",
        "12 m²\nsmall room",
        "25 m²\nlarge room",
    ]
    colors = {"optimistic": "#16a34a", "conservative": "#2563eb", "stress": "#dc2626"}
    fig, ax = plt.subplots(figsize=(9, 5.4))
    for profile in colors:
        values = [
            float(
                next(row for row in rows if row["profile"] == profile and row["target"] == target)[
                    "total_minutes"
                ]
            )
            for target in targets
        ]
        ax.plot(labels, values, marker="o", linewidth=2.2, label=profile, color=colors[profile])
    ax.axhline(30, linestyle="--", color="#111827", linewidth=1.5, label="30-minute objective")
    ax.set_ylabel("Modeled total time (minutes)")
    ax.set_title("Coverage/time scenarios — ASSUMPTIONS, NOT MEASUREMENTS", weight="bold")
    ax.set_ylim(0, 190)
    ax.grid(axis="y", alpha=0.25)
    ax.legend(frameon=False, ncol=2)
    ax.text(
        2,
        -38,
        "Visible target-surface area; inaccessible fractions and reposition overhead included.\n"
        "Hardware timing, rescans and operator interruptions are unvalidated.",
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
