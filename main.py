"""
main.py

Command-line interface for the Random-Circuit Power Estimator.

The program:

    1. Generates a random combinational circuit
    2. Simulates random input vectors
    3. Measures switching activity
    4. Calculates dynamic power
    5. Calculates static power
    6. Reports total power
    7. Optionally saves results to CSV
"""

import argparse
import csv

from cell_library import VDD_VOLTS, FREQ_HZ

from power_calculator import analyze_random_circuit


def print_report(
    per_gate_rows,
    totals,
    vdd,
    freq,
    n_primary_inputs,
    n_gates,
    n_vectors,
):
    """Print a complete power-analysis report."""

    print()
    print("=" * 100)
    print(" RANDOM CIRCUIT POWER ANALYSIS")
    print("=" * 100)

    print(f" Primary inputs      : {n_primary_inputs}")
    print(f" Logic gates         : {n_gates}")
    print(f" Random vectors run  : {n_vectors}")
    print(f" Supply voltage      : {vdd} V")
    print(f" Reference frequency : {freq:.3e} Hz")

    print("-" * 100)

    header = (
        f"{'Idx':>5} "
        f"{'Gate':<8} "
        f"{'Fanout':>8} "
        f"{'C_load(fF)':>12} "
        f"{'Alpha':>9} "
        f"{'P_dyn(uW)':>13} "
        f"{'P_stat(uW)':>13} "
        f"{'P_total(uW)':>14}"
    )

    print(header)
    print("-" * 100)

    for row in per_gate_rows:

        print(
            f"{row['node_idx']:>5} "
            f"{row['gate_type']:<8} "
            f"{row['fanout']:>8} "
            f"{row['c_load_fF']:>12.3f} "
            f"{row['alpha']:>9.4f} "
            f"{row['p_dynamic_uW']:>13.5f} "
            f"{row['p_static_uW']:>13.5f} "
            f"{row['p_total_uW']:>14.5f}"
        )

    print("-" * 100)

    print(
        f" TOTAL DYNAMIC POWER : "
        f"{totals['total_dynamic_uW']:.5f} uW"
    )

    print(
        f" TOTAL STATIC POWER  : "
        f"{totals['total_static_uW']:.5f} uW"
    )

    print(
        f" TOTAL POWER         : "
        f"{totals['total_power_uW']:.5f} uW"
    )

    print("=" * 100)
    print()


def write_csv(
    per_gate_rows,
    totals,
    path,
):
    """Write per-gate and total power results to CSV."""

    fieldnames = [
        "node_idx",
        "gate_type",
        "fanout",
        "c_load_fF",
        "alpha",
        "p_dynamic_uW",
        "p_static_uW",
        "p_total_uW",
    ]

    with open(
        path,
        "w",
        newline="",
        encoding="utf-8",
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames,
        )

        writer.writeheader()

        for row in per_gate_rows:
            writer.writerow(row)

        # Blank line before totals
        writer.writerow({})

        writer.writerow(
            {
                "node_idx": "TOTAL",
                "gate_type": "",
                "fanout": "",
                "c_load_fF": "",
                "alpha": "",
                "p_dynamic_uW":
                    totals["total_dynamic_uW"],
                "p_static_uW":
                    totals["total_static_uW"],
                "p_total_uW":
                    totals["total_power_uW"],
            }
        )

    print(
        f"CSV report written to: {path}"
    )


def main():

    parser = argparse.ArgumentParser(
        description=(
            "Random combinational circuit "
            "static/dynamic power estimator"
        )
    )

    parser.add_argument(
        "--inputs",
        type=int,
        default=6,
        help="number of primary inputs",
    )

    parser.add_argument(
        "--gates",
        type=int,
        default=20,
        help="number of logic gates",
    )

    parser.add_argument(
        "--vectors",
        type=int,
        default=2000,
        help="number of random simulation vectors",
    )

    parser.add_argument(
        "--vdd",
        type=float,
        default=VDD_VOLTS,
        help="supply voltage in volts",
    )

    parser.add_argument(
        "--freq",
        type=float,
        default=FREQ_HZ,
        help="reference frequency in Hz",
    )

    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="random seed",
    )

    parser.add_argument(
        "--csv",
        type=str,
        default=None,
        help="optional CSV output path",
    )

    args = parser.parse_args()

    # ---------------------------------------------------------
    # Run complete analysis
    # ---------------------------------------------------------

    per_gate_rows, totals, nodes = (
        analyze_random_circuit(
            n_primary_inputs=args.inputs,
            n_gates=args.gates,
            n_vectors=args.vectors,
            vdd=args.vdd,
            freq=args.freq,
            seed=args.seed,
        )
    )

    # ---------------------------------------------------------
    # Print report
    # ---------------------------------------------------------

    print_report(
        per_gate_rows,
        totals,
        args.vdd,
        args.freq,
        args.inputs,
        args.gates,
        args.vectors,
    )

    # ---------------------------------------------------------
    # Optional CSV
    # ---------------------------------------------------------

    if args.csv:

        write_csv(
            per_gate_rows,
            totals,
            args.csv,
        )


if __name__ == "__main__":
    main()