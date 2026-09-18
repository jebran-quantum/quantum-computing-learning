from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler

def deutsch_jozsa(n, relevant_bits):
    qc = QuantumCircuit(n + 1, n)
    helper = n
    qc.x(helper)
    for q in range(n + 1):
        qc.h(q)
    for bit in relevant_bits:
        qc.cx(bit, helper)
    for q in range(n):
        qc.h(q)
    qc.measure(range(n), range(n))
    return qc

sampler = StatevectorSampler()

cases = [
    (2, [], "constant"),
    (2, [0], "balanced"),
    (3, [0, 1], "balanced"),
    (4, [2], "balanced"), 
]

for n, bits, label in cases:
    qc = deutsch_jozsa(n, bits)
    counts = sampler.run([qc], shots=10).result()[0].data.c.get_counts()
    print(f"n={n}, bits={bits} ({label})")
    print(f"  Counts: {counts}\n")