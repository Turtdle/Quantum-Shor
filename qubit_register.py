from qubit import Qubit
class Qubit_Register:
    def __init__(self, numBits):
        self.numBits = numBits
        self.numStates = 1 << numBits
        self.entagled = []
        self.bits = [Qubit() for i in range(numBits)]\
        