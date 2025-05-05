import numpy
import pyzx
from pyzx import Graph
from typing import List
# idea is to have an input string of stabilizers and get a zxg graph

def stab2graph(eingabe:List[str])->Graph:
    """
    Converts a list of pauli stabilizers into a ZX Graph
    """
    num_qb = len(eingabe[0])
    g = Graph()
    current_qubits = {}
    # Left boundaries
    for qubit in range(num_qb):
        current_qubits[qubit]=g.add_vertex(ty=0, qubit=qubit, row=0)
    # Add a measurement ancilla
    # g.add_vertex(ty=1, qubit=num_qb+1, row=1)
    for i, stab in enumerate(eingabe, start=1):
        curr_anc = g.add_vertex(ty = 2, qubit=num_qb+1, row=2*i-1)
        for qb, letter in enumerate(stab):
            if letter=="I":
                pass
            elif letter=="X":
                last_qubit = current_qubits[qb]
                hadamard1 = g.add_vertex(ty=3,qubit=qb, row=2*i-0.5)
                g.add_edge((last_qubit, hadamard1))
                current_qubits[qb]=g.add_vertex(ty=1, qubit=qb, row=2*i)
                g.add_edge((hadamard1,current_qubits[qb]))
                g.add_edge((current_qubits[qb], curr_anc))
                hadamard2 = g.add_vertex(ty=3,qubit=qb, row=2*i+0.5)
                g.add_edge((current_qubits[qb], hadamard2))
                current_qubits[qb]=hadamard2

            elif letter=="Z":
                last_qubit = current_qubits[qb]
                current_qubits[qb]=g.add_vertex(ty=1, qubit=qb, row=2*i)
                g.add_edge((last_qubit,current_qubits[qb]))
                g.add_edge((current_qubits[qb], curr_anc))

                # g.add_edge((i,2*i))
    # Right boundaries
    for qubit in range(num_qb):
        last_qubit = current_qubits[qubit]
        current_qubits[qubit]=g.add_vertex(ty=0, qubit=qubit, row=2*len(eingabe)+1)
        g.add_edge((last_qubit,current_qubits[qubit]))
    return g

def main():
    # here e.g. a stabilizer state
    string = ["ZZI","IZZ","XXX"]


if __name__ == "__main__":
    main()