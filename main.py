from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit_aer import AerSimulator
from math import gcd, log2, ceil
from fractions import Fraction
import numpy as np
from sympy import isprime
from time import perf_counter_ns

def create_qpe_circuit(a: int, N: int, n_count: int, n_power: int) -> QuantumCircuit:
    max_qubits = 20  
    if n_count + n_power > max_qubits:
        n_count = max_qubits - n_power
        
    
    qr_count = QuantumRegister(n_count, 'count')
    qr_power = QuantumRegister(n_power, 'power')
    cr = ClassicalRegister(n_count, 'c')
    qc = QuantumCircuit(qr_count, qr_power, cr)
    qc.x(qr_power[0])

    for i in range(n_count):
        qc.h(qr_count[i])
    for i in range(min(n_count, 8)): 
        angle = 2 * np.pi * pow(a, 2**i, N) / N
        qc.cp(angle, qr_count[i], qr_power[0])

    # Apply inverse QFT
    for i in range(n_count//2):
        qc.swap(qr_count[i], qr_count[n_count-i-1])
    for j in range(n_count):
        for m in range(j):
            qc.cp(-np.pi/float(2**(j-m)), qr_count[m], qr_count[j])
        qc.h(qr_count[j])

    qc.measure(qr_count, cr)
    
    return qc

def find_period(a: int, N: int) -> int:

    n_power = ceil(log2(N))
    n_count = min(2 * n_power, 12)
    
    try:
        qc = create_qpe_circuit(a, N, n_count, n_power)

        backend = AerSimulator(
            method='statevector',
            max_parallel_experiments=1,
            max_parallel_shots=1
        )

        shots = 100
        transpiled_qc = transpile(qc, backend, optimization_level=1)
        result = backend.run(transpiled_qc, shots=shots).result()
        counts = result.get_counts()

        measured_phases = []
        for output in counts:
            phase = int(output, 2) / (2**n_count)
            measured_phases.extend([phase] * counts[output])

        for phase in measured_phases:
            frac = Fraction(phase).limit_denominator(N)
            r = frac.denominator
            if r % 2 == 0 and pow(a, r, N) == 1:
                return r
                
    except Exception as e:

        return None
    
    return None

def classical_period_finding(a: int, N: int, max_tries: int = 100) -> int:

    value = a
    for r in range(1, max_tries):
        if value == 1:
            return r
        value = (value * a) % N
    return None

def shors_algorithm(N: int, max_attempts: int = 5) -> tuple:

    if N % 2 == 0:
        return 2, N//2
    
    if is_prime(N):
        return N, 1
    
    
    for attempt in range(max_attempts):
        
        a = np.random.randint(2, N)
        if gcd(a, N) != 1:
            return gcd(a, N), N//gcd(a, N)
        r = find_period(a, N)
        if r is None:
            r = classical_period_finding(a, N)
        
        if r is None or r % 2 != 0:
            continue
        try:
            factor1 = gcd(pow(a, r//2) + 1, N)
            factor2 = gcd(pow(a, r//2) - 1, N)
            
            if factor1 * factor2 == N and min(factor1, factor2) != 1:
                return factor1, factor2
        except Exception as e:
            continue
    
    return None, None

def is_prime(n: int) -> bool:
    return isprime(n)

def factor(n):
    if isprime(n):
        #print(f'Factor {n} is prime.')
        return n
    else:
        #print(f'Factor {n} is not prime. Attempting to factorize...')
        pass
    factors = shors_algorithm(n)
    while factors[0] == None or factors[1] == None:
        factors = shors_algorithm(n)
    
    return factor(factors[0]), factor(factors[1])
if __name__ == "__main__":
    starting_time = perf_counter_ns()
    print(f"Starting at nanosecond timestamp: {starting_time}")
    N = 797991779
    print(f"Factors: of {N}: {factor(N)}")
    print(f"Time taken: {perf_counter_ns() - starting_time} ns")
    print(f'Time in seconds: {(perf_counter_ns() - starting_time) / 1e9} s')
    
    