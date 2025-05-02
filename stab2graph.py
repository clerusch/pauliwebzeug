import numpy
import pyzx
from pyzx import Graph
from typing import List
# idea is to have an input string of stabilizers and get a zxg graph

def stab2graph(eingabe:List[str])->Graph:
    num_qb = len(eingabe[0])
    g = Graph()
    for qubit in num_qb:
        g.add_vertex(ty=0, qubit=qubit, row=0)
    return g

def main():
    # here e.g. a stabilizer state
    string = ["ZZI","IZZ","XXX"]


if __name__ == "__main__":
    main()