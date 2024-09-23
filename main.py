from qubit import Qubit
from qubit_functions import Qubit_Functions
import numpy as np
def NKron(*args):
  """Calculate a Kronecker product over a variable number of inputs"""
  result = np.array([[1.0]])
  for op in args:
    result = np.kron(result, op)
  return result
def main():
    Zero = Qubit(np.array([1,0]))
    One = Qubit(np.array([0,1]))
    ZeroZero = Zero * Zero
    OneOne = One * One
    Plus = Qubit((Zero.state + One.state) / np.sqrt(2))
    PlusPlus = Plus * Plus
    CatState = Qubit((ZeroZero.state + OneOne.state) / np.sqrt(2))
    print(CatState)
    CatStateT = np.dot(CatState.state, CatState.state.T)
    print(CatStateT)
    P0 = np.array([Zero, Zero.state.T])
    P1 = np.array([One, One.state.T])
    X = np.array([[0,1],
              [1,0]])
    Prob0 = np.trace(np.dot(NKron(P0, Id), RhoCatState))
    print(Prob0)

    


if __name__ == "__main__":
    main()