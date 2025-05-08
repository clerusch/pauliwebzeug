import numpy
import pyzx
from pyzx import Graph
from typing import List
from lib.graph_loader import load_graph
from stab2graph import stab2graph
from graph2floq import graph2floq, betterGraph2Floq
import matplotlib.pyplot as plt
from lib.draw_graph import draw_g


def weight_mod_2_decomp(g: Graph) -> Graph:
    # Precompute nodes to decompose, and snapshot relevant info
    to_decompose = []
    for node in g.vertices():
        outdeg = len(g.neighbors(node))
        if outdeg % 2 in (0, 1) and outdeg>=4:
            to_decompose.append({
                "node": node,
                "neighbors": list(g.neighbors(node)),
                "outdeg": outdeg,
                "qubit": g.qubit(node),
                "row": g.row(node),
                "type": g.type(node)
            })

    for info in to_decompose:
        node = info["node"]
        neighbors = info["neighbors"]
        n = len(neighbors)
        qubit = info["qubit"]
        row = info["row"]
        typ = info["type"]
        outdeg = info["outdeg"]
        # Alright so here we really want to prepare our neighbors, right?
        # So first i think we need to make all edges directed correctly
        # So half of our tensor edges should go in and half should go out?
        # Omg this is taking soooooo fucking long should i just not do this rn?
        # Maybe just focus on the high weight steane whatever thing
        # Which is actually: what is the correct dictionary from syndrome to error
        g.remove_vertex(node)

        top_nodes = {}
        bottom_nodes = {}

        for i in range(n // 2 + 2):
            if i <= 1:
                top_nodes[i] = g.add_vertex(ty=typ, qubit=qubit +n//2 - i*n//2, row=row - 0.25)
            else:
                bottom_nodes[i - 2] = g.add_vertex(
                    ty=typ,
                    qubit=qubit + n / 2 - i,# * n / 6,
                    row=row + 0.5
                )

        for top_node in top_nodes.values():
            for bottom_node in bottom_nodes.values():
                if (top_node, bottom_node) not in g.edges() and (bottom_node, top_node) not in g.edges():
                    g.add_edge((top_node, bottom_node))

        for i in range(len(bottom_nodes)):
            g.add_edge((bottom_nodes[i], neighbors[2*i]))
            g.add_edge((bottom_nodes[i],neighbors[2*i+1]))

        if outdeg % 2 == 1:
            print(n)
            g.add_edge((top_nodes[0], neighbors[-1]))

    return g

def main():
    pass

if __name__ == "__main__":
    main()