# Shor's Algorithm Implementation

A quantum computing implementation of Shor's algorithm using QuTiP (Quantum Toolbox in Python) for integer factorization.

## Requirements

- See requirements.txt

## Installation

```bash
pip install numpy qutip
```

## Usage

```python
from shors_algorithm import shors_algorithm

N = 15  # Number to factor
factors = shors_algorithm(N)
if factors:
    print(f"Factors of {N} are: {factors[0]} and {factors[1]}")
```

## Limitations

- Educational implementation suitable for small numbers
- Requires significant computational resources
- May need multiple runs for successful factorization

## Contributing

Contributions are welcome. Please submit a Pull Request.

## Credits

1. minutephysics (youtube) https://www.youtube.com/watch?v=lvTqbM5Dq4Q
2. wikipedia for everything else
