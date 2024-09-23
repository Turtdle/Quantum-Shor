import numpy as np

class Qubit:
    def __init__(self, state=np.array([[1, 0], [0, 1]])):
        self.state = state

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