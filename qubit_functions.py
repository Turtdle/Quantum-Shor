import numpy as np
from qubit import Qubit
import scipy as sp
import scipy.linalg

class Qubit_Functions:
    def __init__(self):
        self.cnot_matrix = np.array([[1, 0, 0, 0],
                                     [0, 1, 0, 0],
                                     [0, 0, 0, 1],
                                     [0, 0, 1, 0]])
        self.cz = np.array([[1, 0, 0, 0],
                            [0, 1, 0, 0],
                            [0, 0, 1, 0],
                            [0, 0, 0, -1]])
        self.swap = np.array([[1, 0, 0, 0],
                              [0, 0, 1, 0],
                              [0, 1, 0, 0],
                              [0, 0, 0, 1]])
        self.toffoli_matrix = np.array([[1, 0, 0, 0, 0, 0, 0, 0],
                                        [0, 1, 0, 0, 0, 0, 0, 0],
                                        [0, 0, 1, 0, 0, 0, 0, 0],
                                        [0, 0, 0, 1, 0, 0, 0, 0],
                                        [0, 0, 0, 0, 1, 0, 0, 0],
                                        [0, 0, 0, 0, 0, 1, 0, 0],
                                        [0, 0, 0, 0, 0, 0, 0, 1],
                                        [0, 0, 0, 0, 0, 0, 1, 0]])

    def normalize(self, state):
        return state / sp.linalg.norm(state)

    def cnot(self, control_qubit, target_qubit):
        state = np.kron(control_qubit.state, target_qubit.state)
        
        
        state = np.dot(self.cnot_matrix, state)
        

        control_qubit.state = np.array([state[0], state[1]])
        target_qubit.state = np.array([state[2], state[3]])

    def crot(self, control_qubit, target_qubit, angle):
        if control_qubit.measure() == 1:
            target_qubit.state = np.dot(np.array([[np.cos(angle), -np.sin(angle)], 
                                                [np.sin(angle),  np.cos(angle)]]), 
                                        target_qubit.state)
    def toffoli(self, control1, control2, target):
        state = np.kron(np.kron(control1.state, control2.state), target.state)
        state = np.dot(self.toffoli_matrix, state)
        control1.state = np.array([state[0], state[1]])
        control2.state = np.array([state[2], state[3]])
        target.state = np.array([state[4], state[7]])