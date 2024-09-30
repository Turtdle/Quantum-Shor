import numpy as np
from qubit import Qubit
def cnot_gate(control, target):
    if control.measure() == 1:
        target.state = np.array([target.state[1], target.state[0]])

def toffoli_gate(control1, control2, target):
    if control1.measure() == 1 and control2.measure() == 1:
        target.state = np.array([target.state[1], target.state[0]])

def quantum_full_adder(a, b, cin):
    q_a = Qubit([1, 0] if a == 0 else [0, 1])
    q_b = Qubit([1, 0] if b == 0 else [0, 1])
    q_cin = Qubit([1, 0] if cin == 0 else [0, 1])
    q_cout = Qubit()

    cnot_gate(q_a, q_b)
    cnot_gate(q_cin, q_b)
    toffoli_gate(q_a, q_cin, q_cout)
    toffoli_gate(q_a, q_b, q_cout)

    sum_bit = q_b.measure()
    carry_out = q_cout.measure()

    return sum_bit, carry_out

def quantum_4bit_adder(a, b):
    if not (0 <= a < 16 and 0 <= b < 16):
        raise ValueError("Inputs must be 4-bit numbers (0-15)")


    a_bits = [int(x) for x in f"{a:04b}"]
    b_bits = [int(x) for x in f"{b:04b}"]

    result_bits = []
    carry = 0

    for i in range(3, -1, -1):
        sum_bit, carry = quantum_full_adder(a_bits[i], b_bits[i], carry)
        result_bits.insert(0, sum_bit)

    if carry == 1:
        print("Warning: Overflow occurred")

    return int(''.join(map(str, result_bits)), 2)
