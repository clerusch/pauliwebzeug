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

def measure_Z(circ:Circuit)->None:
    circ.append("CNOT",[0,7])
    circ.append("CNOT",[1,7])
    circ.append("CNOT",[2,7])
    circ.append("CNOT",[3,7])
    circ.append("CNOT",[4,7])
    circ.append("CNOT",[5,7])
    circ.append("CNOT",[6,7])
    circ.append("MR", [7])
def measure_Z_stab(circ:Circuit) -> None:
    circ.append("CNOT", [0,7])
    circ.append("CNOT", [1,7])
    circ.append("CNOT", [2,7])
    circ.append("CNOT", [3,7])
    circ.append("MR", [7])
    circ.append("CNOT", [0,7])
    circ.append("CNOT", [1,7])
    circ.append("CNOT", [4,7])
    circ.append("CNOT", [5,7])
    circ.append("MR", [7])
    circ.append("CNOT", [0,7])
    circ.append("CNOT", [2,7])
    circ.append("CNOT", [4,7])
    circ.append("CNOT", [6,7])
    circ.append("MR", [7])
    circ.append("TICK")
def measure_X_stab(circ:Circuit) -> None:
    circ.append("H", [7])
    circ.append("CNOT", [7,0])
    circ.append("CNOT", [7,1])
    circ.append("CNOT", [7,2])
    circ.append("CNOT", [7,3])
    circ.append("H", [7])
    circ.append("MR", [7])
    circ.append("H", [7])
    circ.append("CNOT", [7,0])
    circ.append("CNOT", [7,1])
    circ.append("CNOT", [7,4])
    circ.append("CNOT", [7,5])
    circ.append("H", [7])
    circ.append("MR", [7])
    circ.append("H", [7])
    circ.append("CNOT", [7,0])
    circ.append("CNOT", [7,2])
    circ.append("CNOT", [7,4])
    circ.append("CNOT", [7,6])
    circ.append("H", [7])
    circ.append("MR", [7])
    circ.append("TICK")

def add_detectors_2(circ:Circuit) -> None:
    # x is highest number of rec, for some reason need this stupid way
    x = circ.num_measurements #- 1
    # Recs:
    # First green stabilizer
    circ.append("DETECTOR", [target_rec(0-x),target_rec(6-x)])
    # Second green stabilizer
    circ.append("DETECTOR", [target_rec(1-x),target_rec(7-x)])
    # Third green stabilizer
    circ.append("DETECTOR", [target_rec(2-x),target_rec(8-x)])
    # first red stabilizer
    circ.append("DETECTOR", [target_rec(3-x),target_rec(9-x)])
    # Second red stabilizer
    circ.append("DETECTOR", [target_rec(4-x),target_rec(10-x)])
    # Third red stabilizer
    circ.append("DETECTOR", [target_rec(5-x),target_rec(11-x)])

def make_a_circ_and_get_res(shots:int, type:str, qubit: int)->List[bool]:
    p = 1.0
    circ = Circuit()
    # measure_Z(circ)
    measure_Z_stab(circ)
    measure_X_stab(circ)
    circ.append(type,[qubit],p)
    measure_Z_stab(circ)
    measure_X_stab(circ)
    add_detectors_2(circ)
    # here we want the shots to be bigger? why is there some guy sleeping in my office in  the middle of the day??
    # shots = 10
    sampler = circ.compile_detector_sampler()
    result = sampler.sample(shots=shots)
    return result

def main():
    for qb in range(7):
        print(f"qubit {qb}")
        for type in ["X_error", "Z_error"]:
            print(f"Errortype {type}")
            print(make_a_circ_and_get_res(type, qb))

    # print(circ.diagram())

if __name__=="__main__":
    main()