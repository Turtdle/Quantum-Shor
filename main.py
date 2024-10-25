from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit_aer import AerSimulator
from math import gcd
from fractions import Fraction
import numpy as np

def create_qpe_circuit(a: int, N: int, n_count: int, n_power: int) -> QuantumCircuit:
    """
    Creates Quantum Phase Estimation circuit
    
    Args:
        a: Base of the modular exponentiation
        N: Modulus
        n_count: Number of counting qubits
        n_power: Number of qubits for modular exponentiation
    """
    qr_count = QuantumRegister(n_count, 'count')
    qr_power = QuantumRegister(n_power, 'power')
    cr = ClassicalRegister(n_count, 'c')
    qc = QuantumCircuit(qr_count, qr_power, cr)

    # Initialize power register to |1>
    qc.x(qr_power[0])

    # Initialize count register in superposition
    for i in range(n_count):
        qc.h(qr_count[i])

    # Apply controlled rotations
    for i in range(n_count):
        angle = 2 * np.pi * pow(a, 2**i, N) / N
        qc.cp(angle, qr_count[i], qr_power[0])

    # Apply inverse QFT
    for i in range(n_count//2):
        qc.swap(qr_count[i], qr_count[n_count-i-1])
    for j in range(n_count):
        for m in range(j):
            qc.cp(-np.pi/float(2**(j-m)), qr_count[m], qr_count[j])
        qc.h(qr_count[j])

    # Measure counting register
    qc.measure(qr_count, cr)
    
    return qc

def find_period(a: int, N: int) -> int:
    """
    Quantum period finding routine
    
    Args:
        a: Base of the modular exponentiation
        N: Modulus
    
    Returns:
        The period r such that a^r mod N = 1
    """
    n_count = 2 * len(bin(N)[2:])  # Number of counting qubits
    n_power = len(bin(N)[2:])      # Number of qubits for modular exponentiation

    qc = create_qpe_circuit(a, N, n_count, n_power)
    
    # Run on simulator
    backend = AerSimulator()
    shots = 1000
    transpiled_qc = transpile(qc, backend)
    result = backend.run(transpiled_qc, shots=shots).result()
    counts = result.get_counts()
    
    # Process results
    measured_phases = []
    for output in counts:
        phase = int(output, 2) / (2**n_count)
        measured_phases.extend([phase] * counts[output])
    
    # Find the period from the phases
    for phase in measured_phases:
        frac = Fraction(phase).limit_denominator(N)
        r = frac.denominator
        if r % 2 == 0 and pow(a, r, N) == 1:
            return r
    
    return None

def shors_algorithm(N: int, max_attempts: int = 10) -> tuple:
    """
    Main implementation of Shor's algorithm
    
    Args:
        N: Number to factor
        max_attempts: Maximum number of attempts to find factors
    
    Returns:
        Tuple of two factors of N
    """
    if N % 2 == 0:
        return 2, N//2
    
    if is_prime(N):
        return N, 1
    
    for _ in range(max_attempts):
        # Choose random number a < N
        a = np.random.randint(2, N)
        
        # Check if a and N are coprime
        if gcd(a, N) != 1:
            return gcd(a, N), N//gcd(a, N)
        
        # Find period using quantum subroutine
        r = find_period(a, N)
        
        if r is None or r % 2 != 0:
            continue
            
        # Calculate potential factors
        factor1 = gcd(pow(a, r//2) + 1, N)
        factor2 = gcd(pow(a, r//2) - 1, N)
        
        if factor1 * factor2 == N and min(factor1, factor2) != 1:
            return factor1, factor2
    
    return None, None

def is_prime(n: int) -> bool:
    """Simple primality test"""
    if n < 2:
        return False
    for i in range(2, int(np.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

if __name__ == "__main__":
    # Example: Try to factor 15 (3 * 5)
    N = 177221
    print(f"Attempting to factor {N}...")
    factors = shors_algorithm(N)
    if factors[0] is not None:
        print(f"Factors found: {factors}")
    else:
        print("Failed to find factors")