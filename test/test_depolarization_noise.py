import unittest
import pennylane as qml
import numpy as np
import util


class TestCircuitCustom(unittest.TestCase):
    def setUp(self):
        # Set up a PennyLane device for testing
        self.dev = qml.device("default.mixed", wires=2)

    def test_circuit_custom(self):
        # Define the quantum circuit function
        @qml.qnode(self.dev)
        def circuit_custom(p):
            qml.Hadamard(wires=0)
            qml.CNOT(wires=[0, 1])
            qml.QubitChannel(util.depolarization_kraus_matrices(p), wires=0)
            qml.QubitChannel(util.depolarization_kraus_matrices(p), wires=1)
            return qml.expval(qml.PauliZ(0) @ qml.PauliZ(1))

        # Set the parameter value for testing
        ps = [0., 0.001, 0.01, 0.1, 0.2]
        expected = [1., 0.997335, 0.973511, 0.751111, 0.537778]
        # Execute the quantum circuit
        for i, p in enumerate(ps):
            result = circuit_custom(p)
            assert np.isclose(result, expected[i])
