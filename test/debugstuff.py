import pyzx as zx
from pyzx.pauliweb import compute_pauli_webs

# Define a simple quantum circuit
c = zx.qasm("""
qreg q[2];
cx q[0], q[1];
""")
g = c.to_graph()
order, zwebs, xwebs = compute_pauli_webs(g)
print(type(xwebs[2]))