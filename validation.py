"""
validation.py

Validation experiments for the Random-Circuit Power Estimator.

Experiments:

    1. VDD sweep
    2. Frequency sweep
    3. Gate-count sweep
    4. Reproducibility test

Results are saved to:

    results/validation_vdd.csv
    results/validation_frequency.csv
    results/validation_gates.csv
"""

import csv
from pathlib import Path

from power_calculator import analyze_random_circuit


RESULTS_DIR = Path("results")
RESULTS_DIR.mkdir(exist_ok=True)


# ============================================================
# Helper
# ============================================================

def save_csv(path, rows):
    """Save a list of dictionaries to CSV."""

    if not rows:
        return

    with open(
        path,
        "w",
        newline="",
        encoding="utf-8",
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=rows[0].keys(),
        )

        writer.writeheader()
        writer.writerows(rows)

    print(f"Saved: {path}")


# ============================================================
# 1. VDD SWEEP
# ============================================================

def run_vdd_sweep():

    print()
    print("=" * 70)
    print("VDD SWEEP")
    print("=" * 70)

    vdd_values = [
        0.6,
        0.7,
        0.8,
        0.9,
        1.0,
        1.1,
        1.2,
    ]

    rows = []

    for vdd in vdd_values:

        _, totals, _ = analyze_random_circuit(
            n_primary_inputs=6,
            n_gates=20,
            n_vectors=2000,
            vdd=vdd,
            freq=1.0e9,
            seed=42,
        )

        row = {
            "vdd_V": vdd,
            "dynamic_uW":
                totals["total_dynamic_uW"],
            "static_uW":
                totals["total_static_uW"],
            "total_uW":
                totals["total_power_uW"],
        }

        rows.append(row)

        print(
            f"VDD = {vdd:.1f} V | "
            f"Dynamic = {row['dynamic_uW']:.5f} uW | "
            f"Static = {row['static_uW']:.5f} uW | "
            f"Total = {row['total_uW']:.5f} uW"
        )

    save_csv(
        RESULTS_DIR / "validation_vdd.csv",
        rows,
    )


# ============================================================
# 2. FREQUENCY SWEEP
# ============================================================

def run_frequency_sweep():

    print()
    print("=" * 70)
    print("FREQUENCY SWEEP")
    print("=" * 70)

    frequencies = [
        0.25e9,
        0.5e9,
        0.75e9,
        1.0e9,
        1.25e9,
        1.5e9,
        2.0e9,
    ]

    rows = []

    for freq in frequencies:

        _, totals, _ = analyze_random_circuit(
            n_primary_inputs=6,
            n_gates=20,
            n_vectors=2000,
            vdd=1.0,
            freq=freq,
            seed=42,
        )

        row = {
            "frequency_GHz": freq / 1e9,
            "dynamic_uW":
                totals["total_dynamic_uW"],
            "static_uW":
                totals["total_static_uW"],
            "total_uW":
                totals["total_power_uW"],
        }

        rows.append(row)

        print(
            f"Frequency = {freq / 1e9:.2f} GHz | "
            f"Dynamic = {row['dynamic_uW']:.5f} uW | "
            f"Static = {row['static_uW']:.5f} uW | "
            f"Total = {row['total_uW']:.5f} uW"
        )

    save_csv(
        RESULTS_DIR / "validation_frequency.csv",
        rows,
    )


# ============================================================
# 3. GATE COUNT SWEEP
# ============================================================

def run_gate_sweep():

    print()
    print("=" * 70)
    print("GATE COUNT SWEEP")
    print("=" * 70)

    gate_counts = [
        5,
        10,
        20,
        30,
        40,
        50,
        60,
    ]

    rows = []

    for n_gates in gate_counts:

        _, totals, _ = analyze_random_circuit(
            n_primary_inputs=6,
            n_gates=n_gates,
            n_vectors=2000,
            vdd=1.0,
            freq=1.0e9,
            seed=42,
        )

        row = {
            "gates": n_gates,
            "dynamic_uW":
                totals["total_dynamic_uW"],
            "static_uW":
                totals["total_static_uW"],
            "total_uW":
                totals["total_power_uW"],
        }

        rows.append(row)

        print(
            f"Gates = {n_gates:>3} | "
            f"Dynamic = {row['dynamic_uW']:.5f} uW | "
            f"Static = {row['static_uW']:.5f} uW | "
            f"Total = {row['total_uW']:.5f} uW"
        )

    save_csv(
        RESULTS_DIR / "validation_gates.csv",
        rows,
    )


# ============================================================
# 4. REPRODUCIBILITY TEST
# ============================================================

def run_reproducibility_test():

    print()
    print("=" * 70)
    print("REPRODUCIBILITY TEST")
    print("=" * 70)

    _, totals_1, _ = analyze_random_circuit(
        n_primary_inputs=6,
        n_gates=20,
        n_vectors=2000,
        vdd=1.0,
        freq=1.0e9,
        seed=42,
    )

    _, totals_2, _ = analyze_random_circuit(
        n_primary_inputs=6,
        n_gates=20,
        n_vectors=2000,
        vdd=1.0,
        freq=1.0e9,
        seed=42,
    )

    same_dynamic = (
        totals_1["total_dynamic_uW"]
        == totals_2["total_dynamic_uW"]
    )

    same_static = (
        totals_1["total_static_uW"]
        == totals_2["total_static_uW"]
    )

    same_total = (
        totals_1["total_power_uW"]
        == totals_2["total_power_uW"]
    )

    print(
        f"Dynamic power identical : {same_dynamic}"
    )

    print(
        f"Static power identical  : {same_static}"
    )

    print(
        f"Total power identical   : {same_total}"
    )

    if same_dynamic and same_static and same_total:
        print()
        print("PASS: Results are reproducible.")
    else:
        print()
        print("FAIL: Results are not reproducible.")


# ============================================================
# MAIN
# ============================================================

def main():

    print()
    print("=" * 70)
    print("RANDOM-CIRCUIT POWER ESTIMATOR")
    print("VALIDATION EXPERIMENTS")
    print("=" * 70)

    run_vdd_sweep()
    run_frequency_sweep()
    run_gate_sweep()
    run_reproducibility_test()

    print()
    print("=" * 70)
    print("ALL VALIDATION EXPERIMENTS COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()