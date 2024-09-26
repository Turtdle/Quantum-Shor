import numpy as np
import scipy as sp
import scipy.linalg

class Qubit:
    def __init__(self, state=np.array([1, 0])):
        if type(state) == list:
            if len(state) == 2:
                state = np.array(state)
            else:
                raise ValueError("Invalid state")
        if type(state) == np.ndarray:
            self.state = state
        self.Hadamard = 1./np.sqrt(2) * np.array([[1, 1],
                                     [1, -1]])
    def __str__(self):
        return str(self.state)

    def _normalize(self, state):
        if isinstance(state, list):
            state = np.array(state, dtype=complex)
        if isinstance(state, np.ndarray):
            if state.shape == (2,):
                return state / np.linalg.norm(state)
            else:
                raise ValueError("Invalid state shape")
        else:
            raise ValueError("Invalid state type")

    def x_gate(self):
        x_matrix = np.array([[0, 1], [1, 0]])
        self.state = np.matmul(x_matrix, self.state)
        return self

    def y_gate(self):
        y_matrix = np.array([[0, -1j], [1j, 0]])
        self.state = np.matmul(y_matrix, self.state)
        return self

    def z_gate(self):
        z_matrix = np.array([[1, 0], [0, -1]])
        self.state = np.matmul(z_matrix, self.state)
        return self

    def h_gate(self):
        self.state = np.matmul(self.Hadamard, self.state)
        return self
    
    def s_gate(self):
        s_matrix = np.array([[1, 0], [0, 1j]])
        self.state = np.matmul(s_matrix, self.state)
        return self
    
    def t_gate(self):
        t_matrix = np.array([[1, 0], [0, np.exp(1j*np.pi/4)]])
        self.state = np.matmul(t_matrix, self.state)
        return self

    def copy(self):
        return Qubit(np.copy(self.state))

    def __add__(self, other):
        return Qubit(self.state + other.state)

    def __mul__(self, other):
        return Qubit(np.kron(self.state, other.state))
    
    def sqrt(self):
        self.state = np.sqrt(self.state)
        return self
    
    def __truediv__(self, other):
        return Qubit(self.state / other.state)

    def first(self):
        return self.state[0]
    
    def second(self):
        return self.state[1]
    
    def transpose(self):
        self.state = np.transpose(self.state)
        return self
    
    def measure(self):
        prob_0 = np.abs(self.state[0])**2
        if np.random.random() < prob_0:
            self.state = np.array([1, 0], dtype=complex)
            return 0
        else:
            self.state = np.array([0, 1], dtype=complex)
            return 1
    def h(self):
        self.state = np.matmul(self.Hadamard, self.state)
        return self