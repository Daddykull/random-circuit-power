"""
cell_library.py

Small illustrative standard-cell library for the
Random-Circuit Power Estimator.

Each cell contains:
    - input_count : number of logic inputs
    - c_out       : intrinsic output capacitance in fF
    - i_leak      : leakage current in nA
    - logic_fn    : Boolean logic function
"""

CELL_LIBRARY = {

    "INV": {
        "input_count": 1,
        "c_out": 2.0,
        "i_leak": 15.0,
        "logic_fn": lambda ins: int(not ins[0]),
    },

    "BUF": {
        "input_count": 1,
        "c_out": 3.0,
        "i_leak": 18.0,
        "logic_fn": lambda ins: int(bool(ins[0])),
    },

    "AND2": {
        "input_count": 2,
        "c_out": 3.5,
        "i_leak": 22.0,
        "logic_fn": lambda ins: int(ins[0] and ins[1]),
    },

    "OR2": {
        "input_count": 2,
        "c_out": 3.5,
        "i_leak": 22.0,
        "logic_fn": lambda ins: int(ins[0] or ins[1]),
    },

    "NAND2": {
        "input_count": 2,
        "c_out": 3.0,
        "i_leak": 20.0,
        "logic_fn": lambda ins: int(not (ins[0] and ins[1])),
    },

    "NOR2": {
        "input_count": 2,
        "c_out": 3.0,
        "i_leak": 20.0,
        "logic_fn": lambda ins: int(not (ins[0] or ins[1])),
    },

    "XOR2": {
        "input_count": 2,
        "c_out": 5.0,
        "i_leak": 28.0,
        "logic_fn": lambda ins: int(ins[0] != ins[1]),
    },

    "XNOR2": {
        "input_count": 2,
        "c_out": 5.0,
        "i_leak": 28.0,
        "logic_fn": lambda ins: int(ins[0] == ins[1]),
    },
}


# Technology / operating point
VDD_VOLTS = 1.0
FREQ_HZ = 1.0e9

# Additional wiring capacitance for every fanout branch
WIRE_CAP_PER_FANOUT_FF = 0.8