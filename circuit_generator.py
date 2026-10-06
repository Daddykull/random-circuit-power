"""
circuit_generator.py

Generates a random combinational gate-level circuit.

The circuit is represented as a Directed Acyclic Graph (DAG).

Primary inputs are created first.
Every newly created gate can only connect to nodes
that already exist.

Therefore:

    node index(input) < node index(gate)

which guarantees that the circuit can be evaluated
in a simple forward pass.
"""

import random

from cell_library import CELL_LIBRARY


class Node:

    def __init__(self, idx, kind, gate_type=None, inputs=None):

        self.idx = idx

        # "PI" or "GATE"
        self.kind = kind

        # Gate type such as AND2, XOR2, INV, etc.
        self.gate_type = gate_type

        # Indices of nodes feeding this gate
        self.inputs = inputs or []

        # Number of gates driven by this node
        self.fanout = 0

        # Current logic value
        self.value = 0

        # Number of observed transitions
        self.toggle_count = 0


def generate_random_circuit(
    n_primary_inputs=6,
    n_gates=20,
    seed=None
):
    """
    Generate a random combinational circuit.

    Returns:

        nodes
        primary_input_indices
    """

    rng = random.Random(seed)

    nodes = []

    # ---------------------------------------------------------
    # Create primary inputs
    # ---------------------------------------------------------

    for i in range(n_primary_inputs):

        nodes.append(
            Node(
                idx=i,
                kind="PI"
            )
        )

    # ---------------------------------------------------------
    # Create logic gates
    # ---------------------------------------------------------

    gate_types = list(CELL_LIBRARY.keys())

    for i in range(
        n_primary_inputs,
        n_primary_inputs + n_gates
    ):

        gate_type = rng.choice(gate_types)

        input_count = CELL_LIBRARY[gate_type]["input_count"]

        # Only earlier nodes can be selected.
        candidate_pool = list(range(i))

        inputs = [
            rng.choice(candidate_pool)
            for _ in range(input_count)
        ]

        nodes.append(
            Node(
                idx=i,
                kind="GATE",
                gate_type=gate_type,
                inputs=inputs
            )
        )

    # ---------------------------------------------------------
    # Calculate fanout
    # ---------------------------------------------------------

    for node in nodes:

        for source_idx in node.inputs:

            nodes[source_idx].fanout += 1

    primary_input_indices = list(
        range(n_primary_inputs)
    )

    return nodes, primary_input_indices


def evaluate_circuit(
    nodes,
    primary_input_indices,
    input_vector
):
    """
    Evaluate the complete circuit for one
    primary-input vector.

    Example:

        input_vector = [0, 1, 1, 0, 1, 0]

    Every node's value is updated.

    Toggle counts are also updated.
    """

    # ---------------------------------------------------------
    # Apply primary inputs
    # ---------------------------------------------------------

    for pi_idx, bit in zip(
        primary_input_indices,
        input_vector
    ):

        new_value = bit

        if new_value != nodes[pi_idx].value:

            nodes[pi_idx].toggle_count += 1

        nodes[pi_idx].value = new_value

    # ---------------------------------------------------------
    # Evaluate gates
    # ---------------------------------------------------------

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

        new_value = logic_function(
            input_values
        )

        if new_value != node.value:

            node.toggle_count += 1

        node.value = new_value

    return nodes