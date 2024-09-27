import numpy as np

class Qubit:
    def __init__(self, state=None):
        if state is None:
            self.state = np.array([1, 0], dtype=complex)
        else:
            self.state = np.array(state, dtype=complex)
        self.normalize()

    def normalize(self):
        norm = np.linalg.norm(self.state)
        if norm != 0:
            self.state = self.state / norm

    def measure(self):
        prob_0 = np.abs(self.state[0])**2
        return 0 if np.random.random() < prob_0 else 1

    def __str__(self):
        return f"|ψ⟩ = {self.state[0]:.2f}|0⟩ + {self.state[1]:.2f}|1⟩"