import pennylane as qml
import pennylane.numpy as np
import copy
from typing import List

def unitary_fold(circuit, scale_factor: int):
    # original ops
    circuit()
    original_ops = circuit.tape.operations
    ops = circuit.tape.copy(copy_operations=True).operations
    n, s = divmod(scale_factor - 1, 2)
    # take all the gate, append and complex conjugate
    # For the 1st part  (U^H U)**n
    for i in range(n):
        for op in original_ops[::-1]:
            ops.append(qml.adjoint(copy.copy(op)))

        for op in original_ops:
            ops.append(op)

    # For the 2nd part (L_d^H .. L_s^H) (L_s .. L_d)
    if s > 0:
        last_layers = original_ops[-s:]
        for op in last_layers[::-1]:
            ops.append(qml.adjoint(copy.copy(op)))
        for i in last_layers:
            ops.append(op)

            # Return list of op to create the circuit
    return ops, circuit.tape.measurements


def linear_extrapolation(x, y):
    opt_params = np.polyfit(x, y, 1)
    return opt_params[-1]

def polinomial_extraplation(x, y, order):
    opt_params = np.polyfit(x, y, order)
    return opt_params[-1]

def exponential_extraplation(x, y):
    opt_params = np.polyfit(x, np.log(y), 1)
    return np.exp(opt_params[-1])