from qutip import *
import numpy as np
from math import gcd
from fractions import Fraction

def quantum_period_finding(a, N):
    """
    Implements the quantum part of Shor's algorithm using QuTiP
    Args:
        a: the base number for period finding
        N: the number to be factored
    Returns:
        The period of f(x) = a^x mod N
    """
    n = 2 * len(bin(N)[2:]) 
    
    input_register = tensor([basis([2], 0) for _ in range(n)])
    output_register = tensor([basis([2], 0) for _ in range(len(bin(N)[2:]))])

    hadamard = snot()
    for i in range(n):
        input_register = hadamard * input_register
    
    def modular_exponentiation(state, a, N):
        measurements = measure(state, create_measurement_gates(n))
        x = int(''.join(str(m) for m in measurements), 2)

        result = pow(a, x, N)

        result_binary = format(result, f'0{len(bin(N)[2:])}b')
        output_state = tensor([basis([2], int(b)) for b in result_binary])
        
        return tensor(state, output_state)
    state = modular_exponentiation(input_register, a, N)
    
    def qft(n):
        """Creates Quantum Fourier Transform operator for n qubits"""
        qft_gate = Qobj([[1]])
        for i in range(n):
            qft_gate = tensor(qft_gate, hadamard)
            for j in range(i+1, n):
                phase = np.pi / (2**(j-i))
                cphase = controlled_phase_gate(phase, n, i, j)
                qft_gate = cphase * qft_gate
        return qft_gate
    qft_gate = qft(n)
    final_state = qft_gate * state
    measurements = measure(final_state, create_measurement_gates(n))
    
    measured_value = int(''.join(str(m) for m in measurements), 2)
    fraction = Fraction(measured_value, 2**n).limit_denominator(N)
    
    return fraction.denominator

def create_measurement_gates(n):
    """Creates measurement operators for n qubits"""
    return [sigmaz() for _ in range(n)]

def controlled_phase_gate(phase, n, control, target):
    """Creates a controlled phase gate"""
    gate = identity([2**n])
    gate[2**(control) + 2**(target), 2**(control) + 2**(target)] = np.exp(1j * phase)
    return Qobj(gate)

def shors_algorithm(N):
    """
    Main implementation of Shor's algorithm
    Args:
        N: The number to factor
    Returns:
        Two non-trivial factors of N, or None if factorization fails
    """
    if N % 2 == 0:
        return 2, N//2
    
    if N < 3:
        return None
    a = np.random.randint(2, N)
    
    g = gcd(a, N)
    if g > 1:
        return g, N//g
    r = quantum_period_finding(a, N)
    if r % 2 != 0:
        return shors_algorithm(N)
    x = pow(a, r//2, N)
    if x == N-1:
        return shors_algorithm(N)
    
    p = gcd(x+1, N)
    q = gcd(x-1, N)
    
    if p == N or q == N:
        return shors_algorithm(N)
    
    return p, q


if __name__ == "__main__":
    N = 15 
    factors = shors_algorithm(N)
    if factors:
        print(f"Factors of {N} are: {factors[0]} and {factors[1]}")
    else:
        print("Factorization failed")