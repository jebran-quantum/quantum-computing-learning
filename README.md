## Generalized Implementations

`deutsch_jozsa_general.py` — works for any number of input qubits `n` and 
any oracle, specified as a list of "relevant bits" the function depends on 
(empty list = constant function). Verified across n=2, n=3, and n=4 with 
different relevant-bit combinations, all producing correct constant/balanced 
classifications.

`grover_general.py` — works for any target bitstring, with the oracle and 
diffusion operator built programmatically (X-gate placement based on target 
bits, multi-controlled-X/Z for 3+ qubits).

**Finding:** the standard iteration-count formula `round((π/4)·√N)` can 
overshoot for small N. For N=4, the formula gives 2 iterations, but the 
true optimum is 1 — running 2 iterations cycles the amplitude back down to 
uniform superposition (25% each outcome) instead of staying near certainty. 
Confirmed by forcing `iterations=1` manually, which recovered the expected 
~100% success rate. For N=8, the formula's suggested 2 iterations worked 
well (94.5% success), so the overshoot issue seems specific to very small 
search spaces.