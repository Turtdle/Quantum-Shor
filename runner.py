from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit_aer import AerSimulator
from math import gcd, log2, ceil
from fractions import Fraction
import numpy as np
from sympy import isprime
from time import perf_counter_ns

def analyze_quantum_cycles(n_count: int, n_power: int) -> dict:
    """Calculate quantum clock cycles for the circuit."""
    cycles = {
        'initialization': 1,  
        'hadamard': n_count, 
        'controlled_phase': min(n_count, 8) * 3, 
        'qft': (n_count//2) + (n_count * (n_count-1))//2 + n_count,  
        'measurement': n_count
    }
    return {
        'breakdown': cycles,
        'total': sum(cycles.values())
    }

def create_qpe_circuit(a: int, N: int, n_count: int, n_power: int) -> tuple:
    max_qubits = 20
    if n_count + n_power > max_qubits:
        n_count = max_qubits - n_power
    
    qr_count = QuantumRegister(n_count, 'count')
    qr_power = QuantumRegister(n_power, 'power')
    cr = ClassicalRegister(n_count, 'c')
    qc = QuantumCircuit(qr_count, qr_power, cr)
    
    cycles = analyze_quantum_cycles(n_count, n_power)
    
    qc.x(qr_power[0])
    for i in range(n_count):
        qc.h(qr_count[i])
    
    for i in range(min(n_count, 8)):
        angle = 2 * np.pi * pow(a, 2**i, N) / N
        qc.cp(angle, qr_count[i], qr_power[0])
    
    for i in range(n_count//2):
        qc.swap(qr_count[i], qr_count[n_count-i-1])
    
    for j in range(n_count):
        for m in range(j):
            qc.cp(-np.pi/float(2**(j-m)), qr_count[m], qr_count[j])
        qc.h(qr_count[j])
    
    qc.measure(qr_count, cr)
    return qc, cycles

def find_period(a: int, N: int) -> tuple:
    n_power = ceil(log2(N))
    n_count = min(2 * n_power, 12)
    total_cycles = 0
    
    try:
        qc, cycles = create_qpe_circuit(a, N, n_count, n_power)
        total_cycles = cycles['total']
        
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
                return r, total_cycles * shots
    except Exception as e:
       
        return None, total_cycles
        
    return None, total_cycles * shots

def classical_period_finding(a: int, N: int, max_tries: int = 100) -> tuple:
    value = a
    for r in range(1, max_tries):
        if value == 1:
            return r, 0
        value = (value * a) % N
    return None, 0

def shors_algorithm(N: int, max_attempts: int = 5) -> tuple:
    if N % 2 == 0:
        return 2, N//2, 0
    if is_prime(N):
        n_power = ceil(log2(N))
        n_count = min(2 * n_power, 12)
        base_cycles = analyze_quantum_cycles(n_count, n_power)['total']
        return N, 1, base_cycles 
        
    total_quantum_cycles = 0
    for attempt in range(max_attempts):
        a = np.random.randint(2, N)
        if gcd(a, N) != 1:
            return gcd(a, N), N//gcd(a, N), total_quantum_cycles
            
        r, cycles = find_period(a, N)
        total_quantum_cycles += cycles
        
        if r is None:
            r, _ = classical_period_finding(a, N)
            
        if r is None or r % 2 != 0:
            continue
            
        try:
            factor1 = gcd(pow(a, r//2) + 1, N)
            factor2 = gcd(pow(a, r//2) - 1, N)
            if factor1 * factor2 == N and min(factor1, factor2) != 1:
                return factor1, factor2, total_quantum_cycles
        except Exception as e:
            continue
            
    return None, None, total_quantum_cycles

def is_prime(n: int) -> bool:
    return isprime(n)

def factor(n):
    if isprime(n):
        n_power = ceil(log2(n))
        n_count = min(2 * n_power, 12)
        base_cycles = analyze_quantum_cycles(n_count, n_power)['total']
        return n, base_cycles
    
    factors = shors_algorithm(n)
    while factors[0] == None or factors[1] == None:
        new_factors = shors_algorithm(n)
        factors = (new_factors[0], new_factors[1], factors[2] + new_factors[2])
    
    factor1, cycles1 = factor(factors[0])
    factor2, cycles2 = factor(factors[1])
    total_cycles = factors[2] + cycles1 + cycles2
    
    return (factor1, factor2), total_cycles

def run_data(num):
    starting_time = perf_counter_ns()
    #print(f"Starting at nanosecond timestamp: {starting_time}")
    
    N = num
    factors, total_quantum_cycles = factor(N)
    
    output = {
        'factors' : factors,
        'total_quantum_cycles' : total_quantum_cycles,
        'computation_time' : perf_counter_ns() - starting_time
        }
    return output
    