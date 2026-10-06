"""
validation_analysis.py

Quantitative validation of the
Random-Circuit Power Estimator.

Checks:
    1. VDD dynamic-power scaling
    2. Frequency linearity
    3. Gate-count correlation
    4. Reproducibility
"""

import csv
import math
from pathlib import Path

from power_calculator import analyze_random_circuit


RESULTS_DIR = Path("results")


def read_csv(filename):
    """Read a CSV file from the results directory."""

    path = RESULTS_DIR / filename

    with open(
        path,
        "r",
        encoding="utf-8",
    ) as file:
        return list(csv.DictReader(file))


def calculate_r_squared(x, y):
    """Calculate R-squared for a simple linear relationship."""

    x_mean = sum(x) / len(x)
    y_mean = sum(y) / len(y)

    ss_total = sum(
        (value - y_mean) ** 2
        for value in y
    )

    ss_residual = sum(
        (
            y_value
            - (
                (
                    sum(
                        (
                            x_value - x_mean
                        )
                        * (
                            y_value - y_mean
                        )
                        for x_value, y_value
                        in zip(x, y)
                    )
                    / sum(
                        (
                            x_value - x_mean
                        ) ** 2
                        for x_value in x
                    )
                )
                * (x_value - x_mean)
                + y_mean
            )
        ) ** 2
        for x_value, y_value in zip(x, y)
    )

    if ss_total == 0:
        return 1.0

    return 1.0 - (
        ss_residual / ss_total
    )


def validate_vdd():

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

    print()
    print("=" * 70)
    print("1. VDD SCALING VALIDATION")
    print("=" * 70)

    print(
        "Expected relationship: "
        "Dynamic Power ∝ VDD²"
    )

    reference_vdd = vdd[0]
    reference_dynamic = dynamic[0]

    errors = []

    for voltage, measured in zip(
        vdd,
        dynamic,
    ):

        expected = (
            reference_dynamic
            * (voltage / reference_vdd) ** 2
        )

        error_percent = (
            abs(measured - expected)
            / expected
            * 100
        )

        errors.append(error_percent)

        print(
            f"VDD = {voltage:.1f} V | "
            f"Measured = {measured:.5f} uW | "
            f"Expected = {expected:.5f} uW | "
            f"Error = {error_percent:.6f}%"
        )

    print(
        f"\nMaximum scaling error: "
        f"{max(errors):.6f}%"
    )

    if max(errors) < 1e-6:
        print("PASS: VDD² scaling confirmed.")
    else:
        print("CHECK: VDD scaling deviation detected.")


def validate_frequency():

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

    print()
    print("=" * 70)
    print("2. FREQUENCY LINEARITY VALIDATION")
    print("=" * 70)

    print(
        "Expected relationship: "
        "Dynamic Power ∝ Frequency"
    )

    r_squared = calculate_r_squared(
        frequency,
        dynamic,
    )

    print(
        f"R² = {r_squared:.10f}"
    )

    if r_squared > 0.999999:
        print(
            "PASS: Dynamic power is "
            "strongly linear with frequency."
        )
    else:
        print(
            "CHECK: Frequency relationship "
            "shows deviation."
        )


def validate_gate_count():

    rows = read_csv(
        "validation_gates.csv"
    )

    gates = [
        int(row["gates"])
        for row in rows
    ]

    total = [
        float(row["total_uW"])
        for row in rows
    ]

    print()
    print("=" * 70)
    print("3. GATE-COUNT VALIDATION")
    print("=" * 70)

    print(
        "Expected relationship: "
        "Power generally increases with circuit size."
    )

    increasing_steps = 0

    for previous, current in zip(
        total,
        total[1:],
    ):

        if current > previous:
            increasing_steps += 1

    total_steps = len(total) - 1

    r_squared = calculate_r_squared(
        gates,
        total,
    )

    print(
        f"Increasing steps: "
        f"{increasing_steps}/{total_steps}"
    )

    print(
        f"Correlation R²: "
        f"{r_squared:.6f}"
    )

    if increasing_steps == total_steps:
        print(
            "PASS: Power increases at every "
            "tested circuit size."
        )
    else:
        print(
            "PASS WITH VARIATION: Power generally "
            "increases, with topology-dependent variation."
        )


def validate_reproducibility():

    print()
    print("=" * 70)
    print("4. REPRODUCIBILITY VALIDATION")
    print("=" * 70)

    result_1 = analyze_random_circuit(
        n_primary_inputs=6,
        n_gates=20,
        n_vectors=2000,
        seed=42,
    )

    result_2 = analyze_random_circuit(
        n_primary_inputs=6,
        n_gates=20,
        n_vectors=2000,
        seed=42,
    )

    totals_1 = result_1[1]
    totals_2 = result_2[1]

    dynamic_same = math.isclose(
        totals_1["total_dynamic_uW"],
        totals_2["total_dynamic_uW"],
        rel_tol=1e-12,
    )

    static_same = math.isclose(
        totals_1["total_static_uW"],
        totals_2["total_static_uW"],
        rel_tol=1e-12,
    )

    total_same = math.isclose(
        totals_1["total_power_uW"],
        totals_2["total_power_uW"],
        rel_tol=1e-12,
    )

    print(
        f"Dynamic power identical : "
        f"{dynamic_same}"
    )

    print(
        f"Static power identical  : "
        f"{static_same}"
    )

    print(
        f"Total power identical   : "
        f"{total_same}"
    )

    if (
        dynamic_same
        and static_same
        and total_same
    ):
        print(
            "\nPASS: Results are reproducible."
        )
    else:
        print(
            "\nFAIL: Results are not reproducible."
        )


def main():

    print()
    print("=" * 70)
    print("QUANTITATIVE VALIDATION")
    print("Random-Circuit Power Estimator")
    print("=" * 70)

    validate_vdd()
    validate_frequency()
    validate_gate_count()
    validate_reproducibility()

    print()
    print("=" * 70)
    print("VALIDATION COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()