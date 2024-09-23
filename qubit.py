import numpy as np
import scipy as sp
import scipy.linalg

class Qubit:
    def __init__(self, state=np.array([[1, 0], [0, 1]])):
        if type(state) == list:
            if len(state) == 2 and len(state[0]) == 2 and len(state[1]) == 2:
                state = np.array(state)
            else:
                raise ValueError("Invalid state")
        if type(state) == np.ndarray:
            if state.shape == (2, 2):
                self.state = state
            else:
                raise ValueError("Invalid state")
        self.NormalizeState = lambda state: state / sp.linalg.norm(state)
        self.Hadamard = 1./np.sqrt(2) * np.array([[1, 1],
                                     [1, -1]])
    def __str__(self):
        return str(self.state)

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

    def normalize(self):
        self.state = self.state / sp.linalg.norm(self.state)
        return self

    def copy(self):
        return Qubit(np.copy(self.state))

    def __add__(self, other):
        return Qubit(self.state + other.state)
    
    def first(self):
        return self.state[0]
    
    def second(self):
        return self.state[1]
    
    def amplitude00(self):
        return self.state[0][0]

    def amplitude01(self):
        return self.state[0][1]

    def amplitude10(self):
        return self.state[1][0]

    def amplitude11(self):
        return self.state[1][1]

def main():
    q = Qubit()
    q2 = Qubit(np.array([[0, 1], [1, 0]]))
    print(f'x-gate: {q.x_gate()}')
    print(f'y-gate: {q.y_gate()}')
    print(f'z-gate: {q.z_gate()}')
    print(f'x-gate: {q2.x_gate()}')
    print(f'y-gate: {q2.y_gate()}')
    print(f'z-gate: {q2.z_gate()}')

if __name__ == "__main__":
    main()