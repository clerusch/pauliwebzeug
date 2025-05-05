import numpy
import pyzx
from pyzx import Graph
from typing import List

def graph2floq(g:Graph, ancillanodes:List[int])->Graph:
    """
    Distance preservingly rewrites a zx graph
    """
    # Ok so first we create four nodes to replace the one
    # This is actually hard lol
    for node in ancillanodes:
        qubit = g.qubit(node)
        row = g.row(node)
        neighbors = list(g.neighbors(node))
        g.remove_vertex(node)
        print(neighbors)
        if len(neighbors == 4):
            new_nodes = {}
            for i in range(2):
                new_nodes[i] = g.add_vertex(ty=2, qubit=qubit, row=row+i)
                g.add_edge((new_nodes[i],neighbors[i]))
            for i in range(2):
                new_nodes[i+2] = g.add_vertex(ty=2, qubit=qubit+1, row=row+i)
                g.add_edge((new_nodes[i+2],neighbors[i+2]))
            g.add_edge((new_nodes[0], new_nodes[1]))
            g.add_edge((new_nodes[1], new_nodes[3]))
            g.add_edge((new_nodes[0], new_nodes[2]))
            g.add_edge((new_nodes[2], new_nodes[3]))
        elif len(neighbors) <=2:
            pass
        elif len(neighbors) == 3:
            pass
    return g

def betterGraph2Floq(g:Graph, ancillaqb:int):
    for vertex in list(g.vertices()):
        if g.qubit(vertex) == ancillaqb:
            qubit = g.qubit(vertex)
            row = g.row(vertex)
            neighbors = list(g.neighbors(vertex))
            
            blockNeighbors = list(g.neighbors(vertex))
            # print(blockNeighbors+"hi")
            if len(blockNeighbors) == 4:
                new_nodes = {}
            for i in range(2):
                new_nodes[i] = g.add_vertex(ty=2, qubit=qubit, row=row+i)
                g.add_edge((new_nodes[i],neighbors[i]))
            for i in range(2):
                new_nodes[i+2] = g.add_vertex(ty=2, qubit=qubit+1, row=row+i)
                g.add_edge((new_nodes[i+2],neighbors[i+2]))
            g.add_edge((new_nodes[0], new_nodes[1]))
            g.add_edge((new_nodes[1], new_nodes[3]))
            g.add_edge((new_nodes[0], new_nodes[2]))
            g.add_edge((new_nodes[2], new_nodes[3]))
            g.remove_vertex(vertex)
    print("End")
    pass
