import numpy
import pyzx
from pyzx import Graph
from typing import List
from lib.graph_loader import load_graph
from stab2graph import stab2graph
from graph2floq import graph2floq, betterGraph2Floq
import matplotlib.pyplot as plt
from lib.draw_graph import draw_g

def weight_4_decomp(g: Graph) -> Graph:
    """
    Distance preservingly rewrites graph with exactly weight 4 pauli measurements
    """
    for node in list(g.vertices()):
        if len(g.neighbors(node)) != 4:
            continue

        # Record existing info
        neighbors = list(g.neighbors(node))
        qubit = g.qubit(node)
        row = g.row(node)
        typ = g.type(node)
        g.remove_vertex(node)

        # Create new vertices around the original one
        new_nodes = {}
        for i, neighbor in enumerate(neighbors):
            qb_offset = -0.5 + i % 2
            row_offset = -0.5 + i // 2
            new_node = g.add_vertex(ty=typ, qubit=qubit + qb_offset, row=row + row_offset)
            new_nodes[i] = new_node
            g.add_edge((neighbor, new_node))

        # Add internal edges based on alignment
        values = list(new_nodes.values())
        for i, node_a in enumerate(values):
            for node_b in values[i + 1:]:
                aligned = (
                    g.row(node_a) == g.row(node_b) or
                    g.qubit(node_a) == g.qubit(node_b)
                )
                not_connected = (node_a, node_b) not in g.edges() and (node_b, node_a) not in g.edges()
                if aligned and not_connected:
                    g.add_edge((node_a, node_b))
    return g


# def weight_mod_2_decomp(g:Graph)->Graph:
#     for node in list(g.vertices()):
#         outdeg = len(g.neighbors(node))
#         if outdeg%4 !=0 and outdeg%4!=1:
#             continue
#         # remember stuff
#         neighbors = list(g.neighbors(node))
#         n = len(neighbors)
#         qubit = g.qubit(node)
#         row = g.row(node)
#         typ = g.type(node)
#         g.remove_vertex(node)
#         top_nodes = {}
#         bottom_nodes = {}
#         for i in range(n//2+2):
#             if i <= 1:
#                 top_nodes[i] = g.add_vertex(ty=typ, qubit = qubit+i, row=row-0.25)
#                 continue
#             bottom_nodes[i-2] = g.add_vertex(ty=typ, qubit = qubit-n/2+i*n/6, row = row + 0.5)
#         for top_node in top_nodes.values():
#             for bottom_node in bottom_nodes.values():
#                 not_connected = (top_node, bottom_node) not in g.edges() \
#                     and (bottom_node, top_node) not in g.edges()
#                 if not_connected:
#                     g.add_edge((top_node, bottom_node))
#         for i, bottom_node in enumerate(bottom_nodes.values()):
#             g.add_edge((bottom_node, neighbors[i]))
#         if outdeg%4 == 0:
#             print(n)
#             g.add_edge((top_nodes[0],neighbors[-1]))
#     return g            

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
    # Fix connections to neighbors
    # So this kinda
    stabs = ["XXXXXXXX"]#XXXXXXXX"]#,"ZZZZII"]
    g = stab2graph(stabs)
    draw_g(g,"original")
    g2 = weight_mod_2_decomp(g)
    draw_g(g2,"edited")

if __name__ == "__main__":
    main()