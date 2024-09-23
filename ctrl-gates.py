import numpy as np
from qubit import Qubit

class ControlledGate:

    def cnot(self, control_qubit, target_qubit):
        cnot_matrix = np.array([[1, 0, 0, 0],
                                [0, 1, 0, 0],
                                [0, 0, 0, 1],
                                [0, 0, 1, 0]])
        control_qubit.state = np.matmul(cnot_matrix, control_qubit.state)
        return control_qubit

def main():
    q1 = Qubit(np.array([[0, 1], [1, 0]]))
    q2 = Qubit(np.array([[0, 1], [0, 1]]))
    gate = ControlledGate()

    gate.cnot(q1, q2)
    print(f'q1: {q1}')
    print(f'q2: {q2}')

if __name__ == "__main__":
    main()