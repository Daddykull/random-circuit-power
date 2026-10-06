"""
plot_results.py

Generate validation plots for the
Random-Circuit Power Estimator.
"""

import csv
from pathlib import Path

import matplotlib.pyplot as plt


RESULTS_DIR = Path("results")
PLOTS_DIR = RESULTS_DIR / "plots"

PLOTS_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


def read_csv(filename):
    """Read a CSV file and return rows as dictionaries."""

    path = RESULTS_DIR / filename

    with open(
        path,
        "r",
        encoding="utf-8",
    ) as file:

        return list(
            csv.DictReader(file)
        )


# ============================================================
# VDD PLOT
# ============================================================

def plot_vdd():

    rows = read_csv(
        "validation_vdd.csv"
    )

    vdd = [
        float(row["vdd_V"])
        for row in rows
    ]

    dynamic = [
        float(row["dynamic_uW"])
        for row in rows
    ]

    static = [
        float(row["static_uW"])
        for row in rows
    ]

    total = [
        float(row["total_uW"])
        for row in rows
    ]

    plt.figure(figsize=(8, 5))

    plt.plot(
        vdd,
        dynamic,
        marker="o",
        label="Dynamic Power",
    )

    plt.plot(
        vdd,
        static,
        marker="s",
        label="Static Power",
    )

    plt.plot(
        vdd,
        total,
        marker="^",
        label="Total Power",
    )

    plt.xlabel("Supply Voltage VDD (V)")
    plt.ylabel("Power (uW)")
    plt.title("Power vs Supply Voltage")

    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    path = PLOTS_DIR / "vdd_vs_power.png"

    plt.savefig(
        path,
        dpi=300,
    )

    plt.close()

    print(f"Saved: {path}")


# ============================================================
# FREQUENCY PLOT
# ============================================================

def plot_frequency():

    rows = read_csv(
        "validation_frequency.csv"
    )

    frequency = [
        float(row["frequency_GHz"])
        for row in rows
    ]

    dynamic = [
        float(row["dynamic_uW"])
        for row in rows
    ]

    static = [
        float(row["static_uW"])
        for row in rows
    ]

    total = [
        float(row["total_uW"])
        for row in rows
    ]

    plt.figure(figsize=(8, 5))

    plt.plot(
        frequency,
        dynamic,
        marker="o",
        label="Dynamic Power",
    )

    plt.plot(
        frequency,
        static,
        marker="s",
        label="Static Power",
    )

    plt.plot(
        frequency,
        total,
        marker="^",
        label="Total Power",
    )

    plt.xlabel("Frequency (GHz)")
    plt.ylabel("Power (uW)")
    plt.title("Power vs Operating Frequency")

    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    path = (
        PLOTS_DIR
        / "frequency_vs_power.png"
    )

    plt.savefig(
        path,
        dpi=300,
    )

    plt.close()

    print(f"Saved: {path}")


# ============================================================
# GATE COUNT PLOT
# ============================================================

def plot_gates():

    rows = read_csv(
        "validation_gates.csv"
    )

    gates = [
        int(row["gates"])
        for row in rows
    ]

    dynamic = [
        float(row["dynamic_uW"])
        for row in rows
    ]

    static = [
        float(row["static_uW"])
        for row in rows
    ]

    total = [
        float(row["total_uW"])
        for row in rows
    ]

    plt.figure(figsize=(8, 5))

    plt.plot(
        gates,
        dynamic,
        marker="o",
        label="Dynamic Power",
    )

    plt.plot(
        gates,
        static,
        marker="s",
        label="Static Power",
    )

    plt.plot(
        gates,
        total,
        marker="^",
        label="Total Power",
    )

    plt.xlabel("Number of Logic Gates")
    plt.ylabel("Power (uW)")
    plt.title("Power vs Circuit Size")

    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    path = (
        PLOTS_DIR
        / "gates_vs_power.png"
    )

    plt.savefig(
        path,
        dpi=300,
    )

    plt.close()

    print(f"Saved: {path}")


# ============================================================
# MAIN
# ============================================================

def main():

    print()
    print("=" * 60)
    print("GENERATING VALIDATION PLOTS")
    print("=" * 60)

    plot_vdd()
    plot_frequency()
    plot_gates()

    print()
    print("All plots generated successfully.")


if __name__ == "__main__":
    main()