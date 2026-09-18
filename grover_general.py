from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit.primitives import StatevectorSampler
import numpy as np

def grover_oracle(qc, target_bits):
    n = len(target_bits)
    zero_positions = [i for i, bit in enumerate(target_bits) if bit == 0]
    for q in zero_positions:
        qc.x(q)
    if n == 1:
        qc.z(0)
    elif n == 2:
        qc.cz(0, 1)
    else:
        qc.h(n-1)
        qc.mcx(list(range(n-1)), n-1)
        qc.h(n-1)
    for q in zero_positions:
        qc.x(q)

def diffusion(qc, n):
    for q in range(n):
        qc.h(q)
        qc.x(q)
    if n == 1:
        qc.z(0)
    elif n == 2:
        qc.cz(0, 1)
    else:
        qc.h(n-1)
        qc.mcx(list(range(n-1)), n-1)
        qc.h(n-1)
    for q in range(n):
        qc.x(q)
        qc.h(q)

def grover_search(target_bits):
    n = len(target_bits)
    N = 2 ** n
    iterations = round((np.pi / 4) * np.sqrt(N))
    qc = QuantumCircuit(n)
    for q in range(n):
        qc.h(q)
    for _ in range(iterations):
        grover_oracle(qc, target_bits)
        diffusion(qc, n)
    return qc, iterations

def grover_search_fixed_iters(target_bits, iterations):
    n = len(target_bits)
    qc = QuantumCircuit(n)
    for q in range(n):
        qc.h(q)
    for _ in range(iterations):
        grover_oracle(qc, target_bits)
        diffusion(qc, n)
    return qc



print("Case 1:")
qc_test = grover_search_fixed_iters([1, 1], iterations=1)
state_test = Statevector(qc_test)
print(state_test.probabilities())

print("Case 2:")
qc2, iters2 = grover_search([1, 0, 1])
print(f"Iterations: {iters2}")

state2 = Statevector(qc2)
probs2 = state2.probabilities()
for i in range(8):
    print(f"{probs2[i]}")

print("Circuit diagram for 3 qubit case:")
print(qc2.draw())