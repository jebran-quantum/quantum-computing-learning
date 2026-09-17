from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

qc = QuantumCircuit(2)

qc.h(0); qc.h(1)
qc.x(0); qc.x(1)
qc.cz(0,1)
qc.x(0); qc.x(1)
        
qc.h(0); qc.h(1)
qc.x(0); qc.x(1)
qc.cz(0, 1)
qc.x(0); qc.x(1)
qc.h(0); qc.h(1)

state = Statevector(qc)
print(state.probabilities())
print(state)
print(qc.draw())