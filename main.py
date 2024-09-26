from qubit_register import Qubit_Register
from qubit_functions import Qubit_Functions
from math import pi

def main():
    q1 = Qubit_Register(4)
    q2 = Qubit_Register(4)
    carry = Qubit_Register(4)
    qf = Qubit_Functions()
    
    # Set q1 to represent 5 (0101 in binary)
    q1[1].x_gate()
    q1[3].x_gate()
    
    # Set q2 to represent 7 (0111 in binary)  
    q2[1].x_gate()
    q2[2].x_gate()
    q2[3].x_gate()
    print(q1.measure())
    print(q2.measure())    
    for i in range(3):
        qf.cnot(q1[i], carry[i+1])
        qf.cnot(q2[i], carry[i+1])

        qf.toffoli(carry[i], q1[i], q2[i])
    
    qf.cnot(carry[3], q2[3])
    result = int(''.join(str(x) for x in q2.measure()[::-1]), 2)
    print("5 + 7 =", result)

if __name__ == "__main__":
    main()

    """
    output: 
    ['[1 0]', '[1 0]', '[1 0]']
  ['[0.70710678 0.70710678]', '[0.70710678 0.70710678]', '[0.70710678 0.70710678]']
  ['[1. 0.]', '[1. 0.]', '[1. 0.]']
  [0, 0, 0]
  5 + 7 = 15 ???
  """