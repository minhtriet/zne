import copy
from typing import List, Optional

import pennylane as qml
import pennylane.numpy as np


def depolarization_kraus_matrices(p=0.75):
    # the Kraus matrices for depolarization noise
    _K0 = np.sqrt(1 - p) * np.eye(2, dtype=complex)
    _K1 = np.sqrt(p / 3) * np.array([[0., 1.], [1., 0.]], dtype=complex)
    _K2 = np.sqrt(p / 3) * np.array([[0, -1j], [1j, 0]], dtype=complex)
    _K3 = np.sqrt(p / 3) * np.array([[1, 0], [0, -1]], dtype=complex)
    return [_K0, _K1, _K2, _K3]


def circuit_hamiltonian():
    qml.CNOT([0,1])
    qml.RZ(np.pi/3,1)
    qml.CNOT([0,1])
    return qml.expval(qml.PauliZ(1))


def circuit_hamiltonian_noisy(p):
    qml.CNOT([0,1])
    qml.RZ(np.pi/3,1)
    qml.CNOT([0,1])
    qml.QubitChannel(depolarization_kraus_matrices(p), wires=0)
    qml.QubitChannel(depolarization_kraus_matrices(p), wires=1)
    return qml.expval(qml.PauliZ(1))

def circuit_bell_state():
    """
    circuit preparing a Bell state
    """
    qml.Hadamard(wires=0)
    qml.CNOT(wires=[0, 1])
    return qml.expval(qml.PauliZ(0) @ qml.PauliZ(1))


def circuit_bell_state_noisy(p):
    qml.Hadamard(wires=0)
    qml.CNOT(wires=[0, 1])
    qml.QubitChannel(depolarization_kraus_matrices(p), wires=0)
    qml.QubitChannel(depolarization_kraus_matrices(p), wires=1)
    return qml.expval(qml.PauliZ(0) @ qml.PauliZ(1))


def unitary_fold(circuit, scale_factor: int, noise_factor: Optional[float] = None):
    """
    Fold a quantum circuit by applying its unitary evolution multiple times to simulate a larger unitary evolution.

    Args:
        circuit (qml.QNode): The quantum circuit to be folded.
        scale_factor (int): The number of times to fold the circuit. The resulting circuit simulates the unitary evolution (U^H U)^scale_factor,
            where U is the unitary evolution represented by the circuit.
        noise_factor (float): The strength of the noise

    Returns:
        tuple: A tuple containing two elements:
            - list: A list of operations representing the folded circuit.
            - list: A list of measurements in the original circuit.
    """
    # original ops
    if noise_factor is not None:
        circuit(noise_factor)
    else:
        circuit()
    original_ops = circuit.tape.operations
    ops = circuit.tape.copy(copy_operations=True).operations
    n, s = divmod(scale_factor - 1, 2)
    # take all the gate, append and complex conjugate
    # For the 1st part  (U^H U)**n
    for i in range(n):
        for op in original_ops[::-1]:
            if type(op) != qml.ops.channel.QubitChannel:   # adjoint every operator except QubitChannel
                ops.append(qml.adjoint(copy.copy(op)))
            else:
                ops.append(op)

        for op in original_ops:
            ops.append(op)

    # For the 2nd part (L_d^H .. L_s^H) (L_s .. L_d)
    if s > 0:
        last_layers = original_ops[-s:]
        for op in last_layers[::-1]:
            if type(op) != qml.ops.channel.QubitChannel:   # adjoint every operator except QubitChannel
                ops.append(qml.adjoint(copy.copy(op)))
            else:
                ops.append(op)
        for op in last_layers:
            ops.append(op)

    # Return list of op to create the circuit
    return ops, circuit.tape.measurements


def circuit_from_ops(dev, operations: List, measurements: List):
    """
     Create a quantum circuit from a list of operations and measurements.

    Args:
        dev (qml.Device): The PennyLane device to be used for circuit execution.
        operations (list): A list of PennyLane operations representing the quantum gates and measurements to be applied in the circuit.
        measurements (list): A list of PennyLane measurements to be applied in the circuit.

    Returns:
        qml.QNode: A PennyLane QNode representing the quantum circuit created from the provided operations and measurements.
    """

    @qml.qnode(dev)
    def create_circuit():
        for op in operations:
            qml.apply(op)
        return qml.apply(measurements[0])
    return create_circuit()


def create_record(extrapolation_type, noise_level, scale_factor, value):
    """
    Create a record dictionary containing information about a simulation result.

    Args:
        extrapolation_type (str): The type of extrapolation used in the simulation.
        noise_level (float): The strength of noise added to the simulation.
        scale_factor (int): The scale factor used in the simulation.
        value (float): The resulting value obtained from the simulation.

    Returns:
        dict: A dictionary containing the simulation record with the following keys:
            - 'extrapolation_type' (str): The type of extrapolation used.
            - 'noise_strength' (float): The strength of noise added.
            - 'scale_factor' (int): The scale factor used.
            - 'value' (float): The resulting value obtained from the simulation.
    """
    return {'scale_factor': scale_factor, 'noise_strength': noise_level,
            'extrapolation_type': extrapolation_type,
            'value': value}


def linear_extrapolation(x, y):
    """
        Perform linear extrapolation on a set of data points.

        Args:
            x (array_like): The x-coordinates of the data points.
            y (array_like): The y-coordinates of the data points.

        Returns:
            float: The extrapolated value obtained by linearly extrapolating the data points
    """
    opt_params = np.polyfit(x, y, 1)
    return opt_params[-1]


def polynomial_extrapolation(x, y, order):
    """
    Perform polynomial extrapolation on a set of data points.

    This function calculates the coefficients of the polynomial function that best fits the given data points (x, y)
    with the specified order, and returns the extrapolated value at x = infinity, which corresponds to the y-intercept
    of the polynomial fit.

    Args:
        x (array_like): The x-coordinates of the data points.
        y (array_like): The y-coordinates of the data points.
        order (int): The degree of the polynomial

    Returns:
        float: The extrapolated value obtained by extrapolating the polynomial fit to x = infinity.
    """
    opt_params = np.polyfit(x, y, order)
    return opt_params[-1]


def exponential_extrapolation(x, y):
    """
    Perform exponential extrapolation on a set of data points.

    Args:
        x (array_like): The x-coordinates of the data points.
        y (array_like): The y-coordinates of the data points.

    Returns:
        float: The extrapolated value obtained
    """
    opt_params = np.polyfit(-np.array(x), np.log(y), 1)
    return np.exp(opt_params[-1])


def get_reference_extrapolation(device_circuit, max_scale_factor, fold_method, extrapolate_method):
    error_mitigated_device_circuit = qml.transforms.mitigate_with_zne(
        device_circuit,
        range(1, max_scale_factor),
        folding=fold_method,
        extrapolate=extrapolate_method,
    )
    return error_mitigated_device_circuit