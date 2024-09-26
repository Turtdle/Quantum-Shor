from qubit import Qubit
class Qubit_Register:
    def __init__(self, numBits):
        self.numBits = numBits
        self.numStates = 1 << numBits
        self.entagled = []
        self.bits = [Qubit() for i in range(numBits)]

    def __str__(self):
        return str([str(bit) for bit in self.bits])
    
    def __getitem__(self, key):
        return self.bits[key]
    
    def __setitem__(self, key, value):
        self.bits[key] = value
    
    def __add__(self, other):
        if self.numBits != other.numBits:
            raise ValueError("Cannot add registers of different sizes")
        new_register = Qubit_Register(self.numBits)
        new_register.bits = [self.bits[i] + other.bits[i] for i in range(self.numBits)]
        return new_register
    
    def __sub__(self, other):
        if self.numBits != other.numBits:
            raise ValueError("Cannot subtract registers of different sizes")
        new_register = Qubit_Register(self.numBits)
        new_register.bits = [self.bits[i] - other.bits[i] for i in range(self.numBits)]
        return new_register
    
    def __mul__(self, other):
        if self.numBits != other.numBits:
            raise ValueError("Cannot multiply registers of different sizes")
        new_register = Qubit_Register(self.numBits)
        new_register.bits = [self.bits[i] * other.bits[i] for i in range(self.numBits)]
        return new_register
    
    def __truediv__(self, other):
        if self.numBits != other.numBits:
            raise ValueError("Cannot divide registers of different sizes")
        new_register = Qubit_Register(self.numBits)
        new_register.bits = [self.bits[i] / other.bits[i] for i in range(self.numBits)]
        return new_register

    def apply(self, gate):
        for i in range(self.numBits):
            self.bits[i] = gate(self.bits[i])
        return self

    def measure(self):
        return [bit.measure() for bit in self.bits]
    
    