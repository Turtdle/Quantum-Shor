from qubit import Qubit
import numpy as np
def main():
    ZeroZero = Qubit(np.array([[1, 0], [0, 0]]))
    OneOne = Qubit(np.array([[0, 0], [0, 1]]))
    PlusPlus = Qubit(np.array([[0.5, 0.5], [0.5, 0.5]]))
    CatState = ZeroZero+OneOne
    print(ZeroZero+OneOne)
    CatState.normalize()
    print(CatState)
    print(CatState.first()[0])
    print(CatState.first()[1])
    print(CatState.second()[0])
    print(CatState.second()[1])


if __name__ == "__main__":
    main()