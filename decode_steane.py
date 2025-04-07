from typing import List
from pyzx.pauliweb import PauliWeb
from lib.graph_loader import load_graph
from lib.detection_webs import get_detection_webs
import pyzx as zx

def add_pws(pws: List[PauliWeb])-> List[PauliWeb]:
    """
    Returns (possibly non-continuous) overlap of pauliwebs
    """
    visited_once = set()
    visited_edges = set()
    for pw in pws:
        half_edges = pw.half_edges()
        for key, value in half_edges.items():
            # print(key, value)
            if (key, value) in visited_edges:
                visited_edges.remove((key, value))
            else:
                visited_edges.add((key, value))

        # for node in pw.vertices():
        #     if node in visited_once:
        #         visited_once.remove(node)
        #     else:
        #         visited_once.add(node)
    g = pws[0].g
    # print(visited_edges)
    pauliweb = PauliWeb(g)
    for halfEdge, type in visited_edges:
        pauliweb.add_half_edge(halfEdge, type)
    return pauliweb
    # if pws:
    #     g = pw.g
    #     pauliweb = PauliWeb(g)
    #     for node in visited_once:
    #         if g.ty[node] == 1:
    #             color = 'Z'
    #             for neighbor in g.neighbors(node):
    #                 pauliweb.add_edge((node, neighbor), color)
    #         if g.ty[node] == 2:
    #             color = 'X'
    #             for neighbor in g.neighbors(node):
    #                 pauliweb.add_edge((node, neighbor), color)
    #     return pauliweb
    # else:
    #     raise ValueError("The list of pauliwebs was empty", pws)

def main():
    steane_g = load_graph("zxgs/steane_style_steane_2_rounds.zxg")
    steane_g.set_inputs([21,20,19,48,47,46,45])
    steane_g.set_outputs([170,97,169,125,94,131,132])
    pws = get_detection_webs(steane_g)
    pwsum = add_pws(pws)
    zx.draw(steane_g, labels=True, pauli_web = pwsum)

if __name__ == "__main__":
    main()