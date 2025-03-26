import pyzx as zx 
from lib.graph_loader import load_graph
import networkx as nx
from f2linalg.f2linalg import Mat2
import numpy as np
from pyzx.pauliweb import PauliWeb
from lib.detection_webs import get_detection_webs
from stim import target_rec, Circuit
import matplotlib.pyplot as plt
def measure_Z_stab(circ):
    circ.append("H",[7,9,10])
    circ.append("CNOT", [7,0])
    circ.append("CNOT", [10,5])
    circ.append("CNOT", [10,11])
    circ.append("CNOT", [9,6])
    circ.append("CNOT", [9,10])
    circ.append("CNOT", [10,8])
    circ.append("CNOT", [7,9])
    circ.append("CNOT", [10,7])
    circ.append("CNOT", [9,8])
    circ.append("CNOT", [7,11])
    circ.append("CNOT", [9,11])
    circ.append("CNOT", [7,1])
    circ.append("CNOT", [8,2])
    circ.append("CNOT", [9,3])
    circ.append("CNOT", [10,4])
    circ.append("H", [7,8,9,10])
    circ.append("MR", [7,8,9,10,11])
    circ.append("TICK")

def measure_X_stab(circ):
    circ.append("H",[8,11])
    circ.append("CNOT", [0,7])
    circ.append("CNOT", [5,10])
    circ.append("CNOT", [11,10])
    circ.append("CNOT", [6,9])
    circ.append("CNOT", [10,9])
    circ.append("CNOT", [8,10])
    circ.append("CNOT", [9,7])
    circ.append("CNOT", [7,10])
    circ.append("CNOT", [8,9])
    circ.append("CNOT", [11,7])
    circ.append("CNOT", [11,9])
    circ.append("CNOT", [1,7])
    circ.append("CNOT", [2,8])
    circ.append("CNOT", [3,9])
    circ.append("CNOT", [4,10])
    circ.append("H", [11])
    circ.append("MR", [7,8,9,10,11])
    circ.append("TICK")

def measure_Z(circ):
    circ.append("CNOT",[0,12])
    circ.append("CNOT",[1,12])
    circ.append("CNOT",[2,12])
    circ.append("CNOT",[3,12])
    circ.append("CNOT",[4,12])
    circ.append("CNOT",[5,12])
    circ.append("CNOT",[6,12])
    circ.append("MR", [12])
    circ.append("TICK")

def add_detectors(circ):
    # x is highest number of rec, for some reason need this stupid way
    x = 32
    # Recs:
    # Green ancilla first
    circ.append("DETECTOR", [target_rec(15-x)])
    # Red ancilla middle
    circ.append("DETECTOR", [target_rec(20-x)])
    # Red joint
    circ.append("DETECTOR", [target_rec(11-x), target_rec(20-x), target_rec(21-x)])
    # Red ancilla fourth
    circ.append("DETECTOR", [target_rec(30-x)])
    # Green ancilla third
    circ.append("DETECTOR", [target_rec(25-x)])
    # Red joint
    circ.append("DETECTOR", [target_rec(11-x), target_rec(12-x), target_rec(13-x), target_rec(20-x),target_rec(21-x), target_rec(22-x), target_rec(23-x)])
    # Green joint
    circ.append("DETECTOR", [target_rec(17-x), target_rec(18-x), target_rec(27-x), target_rec(28-x)])
    # Green joint
    circ.append("DETECTOR", [target_rec(16-x), target_rec(17-x), target_rec(19-x), target_rec(26-x),target_rec(27-x), target_rec(29-x)])
    # Red joint
    circ.append("DETECTOR", [target_rec(12-x), target_rec(14-x), target_rec(20-x), target_rec(22-x), target_rec(24-x)])
    # Finally, the logical detector: (True means a bitflip happened here)
    circ.append("DETECTOR", [target_rec(10-x), target_rec(31-x)])


def main():
    # Since logical Z is transversal, we just project onto
    # any stabilised state by stabiliser measurements and then
    # doing a logical Z measurement.
    circ = Circuit()
    # prepare logical |0>
    measure_Z_stab(circ)
    measure_X_stab(circ)
    measure_Z(circ)
    # Measure stabilizers for detection regions
    measure_Z_stab(circ)
    measure_X_stab(circ)
    # Add errors
    p = 1
    circ.append_operation("X_error", [11], p)
    # Complete detection regions
    measure_Z_stab(circ)
    measure_X_stab(circ)
    # now we want to see if we get the same measuremetn result as previously
    measure_Z(circ)
    
    add_detectors(circ)
    # # x is highest number of rec, for some reason need this stupid way
    # x = 32
    # # Recs:
    # # Green ancilla first
    # circ.append("DETECTOR", [target_rec(15-x)])
    # # Red ancilla middle
    # circ.append("DETECTOR", [target_rec(20-x)])
    # # Red joint
    # circ.append("DETECTOR", [target_rec(11-x), target_rec(20-x), target_rec(21-x)])
    # # Red ancilla fourth
    # circ.append("DETECTOR", [target_rec(30-x)])
    # # Green ancilla third
    # circ.append("DETECTOR", [target_rec(25-x)])
    # # Red joint
    # circ.append("DETECTOR", [target_rec(11-x), target_rec(12-x), target_rec(13-x), target_rec(20-x),target_rec(21-x), target_rec(22-x), target_rec(23-x)])
    # # Green joint
    # circ.append("DETECTOR", [target_rec(17-x), target_rec(18-x), target_rec(27-x), target_rec(28-x)])
    # # Green joint
    # circ.append("DETECTOR", [target_rec(16-x), target_rec(17-x), target_rec(19-x), target_rec(26-x),target_rec(27-x), target_rec(29-x)])
    # # Red joint
    # circ.append("DETECTOR", [target_rec(12-x), target_rec(14-x), target_rec(20-x), target_rec(22-x), target_rec(24-x)])
    # # Finally, the logical detector: (True means a bitflip happened here)
    # circ.append("DETECTOR", [target_rec(10-x), target_rec(31-x)])

    

    # print(circ.diagram('timeline-text'))
    sampler = circ.compile_detector_sampler()
    result = sampler.sample(shots=1000)
    for num, row in enumerate(result):
        for entry in row[:-1]:
            if entry:
                print(f"error happened in {row}")

if __name__ == "__main__":
    main()