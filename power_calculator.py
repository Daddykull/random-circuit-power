"""
power_calculator.py

Measures switching activity and estimates:

    1. Dynamic power
    2. Static (leakage) power
    3. Total power

Dynamic power:

    P_dynamic = alpha * 0.5 * C_load * VDD^2 * f

Static power:

    P_static = VDD * I_leak
"""

import random

from cell_library import (
    CELL_LIBRARY,
    VDD_VOLTS,
    FREQ_HZ,
    WIRE_CAP_PER_FANOUT_FF,
)

from circuit_generator import (
    generate_random_circuit,
    evaluate_circuit,
)


def run_random_vector_simulation(
    nodes,
    primary_input_indices,
    n_vectors=2000,
    seed=None,
):
    """
    Run random-vector simulation.

    The first vector establishes the initial circuit state.
    Toggle counting starts from the second vector.

    Therefore, every counted transition corresponds to a
    transition between two actual simulated vectors.
    """

    rng = random.Random(seed)

    for vector_index in range(n_vectors):

        # Generate one random input vector
        input_vector = [
            rng.randint(0, 1)
            for _ in primary_input_indices
        ]

        # -----------------------------------------------------
        # First vector:
        # Establish initial state WITHOUT counting toggles.
        # -----------------------------------------------------

        if vector_index == 0:

            # Set primary-input values
            for pi_idx, bit in zip(
                primary_input_indices,
                input_vector,
            ):
                nodes[pi_idx].value = bit

            # Propagate the first vector through the circuit
            for node in nodes:

                if node.kind != "GATE":
                    continue

                input_values = [
                    nodes[source_idx].value
                    for source_idx in node.inputs
                ]

                logic_function = CELL_LIBRARY[
                    node.gate_type
                ]["logic_fn"]

                node.value = logic_function(
                    input_values
                )

        # -----------------------------------------------------
        # Remaining vectors:
        # Count real transitions.
        # -----------------------------------------------------

        else:

            evaluate_circuit(
                nodes,
                primary_input_indices,
                input_vector,
            )

    return n_vectors


def compute_power(
    nodes,
    n_vectors,
    vdd=VDD_VOLTS,
    freq=FREQ_HZ,
    wire_cap_per_fanout=WIRE_CAP_PER_FANOUT_FF,
):
    """
    Calculate dynamic, static and total power
    for every logic gate.

    Returns:

        per_gate_rows
        totals
    """

    per_gate_rows = []

    total_dynamic_w = 0.0
    total_static_w = 0.0

    # =========================================================
    # Analyze every node
    # =========================================================

    for node in nodes:

        # Primary inputs are not counted as logic-cell power.
        if node.kind != "GATE":
            continue

        # -----------------------------------------------------
        # Get standard-cell parameters
        # -----------------------------------------------------

        cell = CELL_LIBRARY[node.gate_type]

        # -----------------------------------------------------
        # Calculate load capacitance
        #
        # C_load =
        #     intrinsic output capacitance
        #     +
        #     fanout × wiring capacitance
        # -----------------------------------------------------

        c_load_ff = (
            cell["c_out"]
            + node.fanout * wire_cap_per_fanout
        )

        # Convert fF → F
        c_load_f = c_load_ff * 1e-15

        # -----------------------------------------------------
        # Measured switching activity
        #
        # toggle_count = number of observed transitions
        # n_vectors - 1 = number of transitions intervals
        # -----------------------------------------------------

        alpha = (
            node.toggle_count
            / max(1, n_vectors - 1)
        )

        # -----------------------------------------------------
        # Dynamic power
        #
        # P_dyn = alpha × 0.5 × C × V² × f
        # -----------------------------------------------------

        p_dynamic_w = (
            alpha
            * 0.5
            * c_load_f
            * (vdd ** 2)
            * freq
        )

        # -----------------------------------------------------
        # Static / leakage power
        #
        # I_leak is stored in nA.
        # Convert nA → A.
        # -----------------------------------------------------

        leakage_current_a = (
            cell["i_leak"] * 1e-9
        )

        p_static_w = (
            vdd * leakage_current_a
        )

        # -----------------------------------------------------
        # Accumulate circuit totals
        # -----------------------------------------------------

        total_dynamic_w += p_dynamic_w
        total_static_w += p_static_w

        # -----------------------------------------------------
        # Store per-gate result
        # -----------------------------------------------------

        per_gate_rows.append(
            {
                "node_idx": node.idx,
                "gate_type": node.gate_type,
                "fanout": node.fanout,
                "c_load_fF": c_load_ff,
                "alpha": alpha,
                "p_dynamic_uW": p_dynamic_w * 1e6,
                "p_static_uW": p_static_w * 1e6,
                "p_total_uW": (
                    p_dynamic_w + p_static_w
                ) * 1e6,
            }
        )

    # =========================================================
    # Circuit totals
    # =========================================================

    totals = {
        "total_dynamic_uW":
            total_dynamic_w * 1e6,

        "total_static_uW":
            total_static_w * 1e6,

        "total_power_uW":
            (total_dynamic_w + total_static_w) * 1e6,
    }

    return per_gate_rows, totals


def analyze_random_circuit(
    n_primary_inputs=6,
    n_gates=20,
    n_vectors=2000,
    vdd=VDD_VOLTS,
    freq=FREQ_HZ,
    seed=None,
):
    """
    Complete analysis pipeline:

        1. Generate random circuit
        2. Simulate random input vectors
        3. Measure switching activity
        4. Calculate power

    Returns:

        per_gate_rows
        totals
        nodes
    """

    # ---------------------------------------------------------
    # Generate circuit
    # ---------------------------------------------------------

    nodes, primary_input_indices = (
        generate_random_circuit(
            n_primary_inputs,
            n_gates,
            seed=seed,
        )
    )

    # ---------------------------------------------------------
    # Run random-vector simulation
    # ---------------------------------------------------------

    run_random_vector_simulation(
        nodes,
        primary_input_indices,
        n_vectors=n_vectors,
        seed=seed,
    )

    # ---------------------------------------------------------
    # Calculate power
    # ---------------------------------------------------------

    per_gate_rows, totals = compute_power(
        nodes,
        n_vectors,
        vdd=vdd,
        freq=freq,
    )

    return (
        per_gate_rows,
        totals,
        nodes,
    )