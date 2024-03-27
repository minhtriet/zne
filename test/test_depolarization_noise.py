import unittest
import pennylane as qml
import numpy as np
import util


class TestCircuitCustom(unittest.TestCase):
    def setUp(self):
        # Set up a PennyLane device for testing
        self.dev = qml.device("default.mixed", wires=2)

    def test_circuit_custom(self):
        ps = [0., 0.001, 0.01, 0.1, 0.2]
        for p in ps:
            dev_noise = qml.transforms.insert(self.dev, qml.DepolarizingChannel, p)
            result = qml.QNode(util.circuit_bell_state_noisy, self.dev)(p)
            expect = qml.QNode(util.circuit_bell_state, dev_noise)()
            assert np.isclose(result, expect), f"Expected {expect}, received {result}"
