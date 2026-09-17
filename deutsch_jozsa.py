from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

qc = QuantumCircuit(4)

qc.x(3)
qc.h(0)
qc.h(1)
qc.h(2)
qc.h(3)
qc.cx(0,3)
qc.cx(1,3)
qc.h(0)
qc.h(1)

state = Statevector(qc)
print(state.probabilities())
print(state)