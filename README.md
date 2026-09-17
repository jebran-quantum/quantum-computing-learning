# Quantum Algorithms: Deutsch-Jozsa & Grover's Search

This repo is about my learning in some Quantum Computing Algorithms

## Deutsch-Jozsa Algorithm

### Problem
Consider a function f(x) which takes an n-bit input and returns a single bit, either 0 or 1. One of two things is possible:

Constant: the output is the same for every input.

Balanced: the output is 0 for exactly half the inputs and 1 for the other half.

A classical computer has to check inputs one by one to be sure worst case up to 2^(n-1)+1 queries. A quantum computer needs only 1 query, no matter how big n is.


### Approach
We use n qubits for input and 1 extra qubit for output. First we flip the output qubit to |1> and put all qubits into superposition with Hadamard gates. Then we apply the black box (oracle). Finally we apply Hadamard gates again and measure the input qubits. If we measure all zeros, the function is constant. If we measure anything else, it's balanced.
for getting balanced we use cnot gate
```python
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler

# Balanced oracle: f(x0, x1) = x0
qc = QuantumCircuit(3, 2)
qc.x(2)
qc.h(0); qc.h(1); qc.h(2)
qc.cx(0, 2)
qc.h(0); qc.h(1)
qc.measure([0, 1], [0, 1])

sampler = StatevectorSampler()
job = sampler.run([qc], shots=10)
counts = job.result()[0].data.c.get_counts()
print(counts)
```

```
     ┌───┐          ┌───┐┌─┐
q_0: ┤ H ├───────■──┤ H ├┤M├
     ├───┤┌───┐  │  └┬─┬┘└╥┘
q_1: ┤ H ├┤ H ├──┼───┤M├──╫─
     ├───┤├───┤┌─┴─┐ └╥┘  ║
q_2: ┤ X ├┤ H ├┤ X ├──╫───╫─
     └───┘└───┘└───┘  ║   ║
c: 2/═════════════════╩═══╩═
                      1   0
```               
for constant function remove cnot
```python
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler

qc = QuantumCircuit(3, 2)

qc.x(2)
qc.h(0)
qc.h(1)
qc.h(2)


qc.h(0)
qc.h(1)

qc.measure([0, 1], [0, 1])

sampler = StatevectorSampler()
job = sampler.run([qc], shots=10)
result = job.result()

counts = result[0].data.c.get_counts()
print(counts)
print(qc)
```

```
     ┌───┐┌───┐┌─┐   
q_0: ┤ H ├┤ H ├┤M├───
     ├───┤├───┤└╥┘┌─┐
q_1: ┤ H ├┤ H ├─╫─┤M├
     ├───┤├───┤ ║ └╥┘
q_2: ┤ X ├┤ H ├─╫──╫─
     └───┘└───┘ ║  ║ 
c: 2/═══════════╩══╩═
                0  1 
                
```
### Results
**Simulator:**
Ran on StateVectorSampler with 10 shots.

Constant oracle → measured 00 10/10 times.

Balanced oracle → measured 01 10/10 times.

**Real hardware (ibm_kingston):**
Balanced oracle → measured 01 about 970/1000 times.

Constant oracle on hardware: not yet tested.

### What Didn't Work / Surprises

- Forgot to add `qc.measure()` on my first multi-qubit QRNG attempt — the classical bits defaulted to 0 and every shot printed `0000`, which looked like a bug in the quantum logic but was actually just missing measurement instructions.
- Mixed up Qiskit's bit ordering more than once — measurement outcomes are printed with qubit 0 as the *rightmost* character in the bitstring, not the leftmost. Cost me a few wrong conclusions until I started converting index → binary carefully every time.
- When building custom Grover oracles for different targets (e.g. `|01⟩`, `|00⟩`), I initially put the X-gates on the wrong qubit before working out the actual rule: sandwich an X gate around the oracle's CZ for every qubit where the target bit is 0, leave qubits with target bit 1 untouched.
- The most interesting result: running a plain Hadamard gate on real hardware gave a noticeably biased split (~70/30 instead of 50/50) even with 1000 shots — a real, systematic bias from the hardware, not just statistical noise (confirmed since the ratio didn't improve with more shots). But Deutsch-Jozsa, run on the same hardware, stayed ~99% accurate despite having *more* gates and *more* qubits. Turns out algorithms that funnel probability toward one dominant outcome (large gap between the right answer and everything else) are much more robust to noise than a 50/50 superposition, where there's no margin to absorb any bias.

## Grover's Algorithm

### Problem
We have a list of N items and only one is the one we want (marked by an oracle). A classical computer needs about N/2 checks on average. Grover's algorithm finds it in about √N steps. For 2 qubits (4 items) that's basically one shot.


### Approach
We start by putting all qubits into an equal superposition, so every item has the same chance. Then we repeat a "Grover step" apply the oracle which flips the sign of the marked item and then apply the diffusion operator which flips all amplitudes around their average. Each step makes the marked item's amplitude bigger.

### Results
Simulator:

Checked with Statevector (exact probabilities, no shots): probability of measuring 11 = 1.0.

Shot-based run and real-hardware run: not yet tested.

## Setup
Install the package:
pip install qiskit qiskit-ibm-runtime qiskit-aer
run it:
python3 deutsch_jozsa.py
python3 grover.py
