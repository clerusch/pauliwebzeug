import pyzx as zx
from lib.graph_loader import load_graph
import networkx as nx
from f2linalg.f2linalg import Mat2
import numpy as np
from pyzx.pauliweb import PauliWeb
from lib.detection_webs import get_detection_webs
from stim import target_rec, Circuit
import matplotlib.pyplot as plt
from typing import List
import stim

def to_circ(g:zx.Graph)->Circuit:
    # circ = Circuit()
    # How do we go about formalizing this?
    # We have the advantage of a layout thats already circuit-like
    
    pass

def main():
    test_graph = load_graph("zxgs/steane_style_steane_2_rounds.zxg")
    test_graph.set_inputs([21,20,19,48,47,46,45])
    test_graph.set_outputs([170,97,169,125,94,131,132])
    pws = get_detection_webs(test_graph)
    circ = to_circ(test_graph)
    print(circ)
    # for pw in pws:
    #     circ.add_detector(pw)

if __name__ == '__main__':
    main()