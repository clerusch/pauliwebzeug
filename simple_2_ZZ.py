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

def meas_ZZ(circ:Circuit) -> None:
    circ.append("CNOT", [0,2])
    circ.append("CNOT", [1,2])
    circ.append("MR", [2])

def main():
    shots = 1
    c = Circuit()
    meas_ZZ(c)
    c.append("X_error",[1],1.0)
    meas_ZZ(c)
    c.append("DETECTOR", [target_rec(-1),target_rec(-2)])

    sampler = c.compile_detector_sampler()
    res = sampler.sample(shots=shots)
    print(res)

if __name__ == "__main__":
    main()
