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
def measure_Z_stab(circ:Circuit) -> None:
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

def measure_X_stab(circ:Circuit) -> None:
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

def measure_Z(circ:Circuit) -> None:
    circ.append("CNOT",[0,12])
    circ.append("CNOT",[1,12])
    circ.append("CNOT",[2,12])
    circ.append("CNOT",[3,12])
    circ.append("CNOT",[4,12])
    circ.append("CNOT",[5,12])
    circ.append("CNOT",[6,12])
    circ.append("MR", [12])
    circ.append("TICK")

def add_detectors_2(circ:Circuit) -> None:
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

def add_detectors_4(circ:Circuit) -> None:
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

def create_steane_error_circ(num_rounds: int, errortype: str, qubits: List[int], p: float)->Circuit:
    """
    This function creates a dist-preserving steane error circuit, with errors introduced
    on qubits at the exact middle of stabilizer rounds.

    Inputs:
        num_rounds: Number of stabilizer measurement rounds
        errortype:  String describing X/Y/Z error for stim
        qubits:     List of qubits to apply error on
        p:          Probability of error occurrence
    Output:
        A stim Circuit with errors applied at the middle, according to inputs.
    """
    # Handling user error
    # OOh this is fancy :D
    dispatch = {
        2: add_detectors_2,
        4: add_detectors_4,
        #... add more here
    }
    supported_types ={"X_error", "Y_error", "Z_error"}
    if num_rounds not in dispatch:
        raise ValueError("Unsupported number of rounds")
    if errortype not in supported_types:
        raise ValueError("Unsupported error type")
    
    circ = Circuit()
    # prepare logical |0>
    measure_Z_stab(circ)
    measure_X_stab(circ)
    measure_Z(circ)
    # Measure stabilizers for detection regions
    for _ in range(num_rounds//2):
        measure_Z_stab(circ)
        measure_X_stab(circ)
    # Add errors
    # time location is in-between stab rounds
    # idk if this is correct but divide by 12 because i do it many times?
    circ.append(errortype, qubits, p)# [0,1,2,3,4,5,6,7,8,9,10,11], p)
    # Complete detection regions
    for _ in range(num_rounds//2):
        measure_Z_stab(circ)
        measure_X_stab(circ)
    # now we want to see if we get the same measuremetn result as previously
    measure_Z(circ)
    
    # Fuck the detectors are different too on multiple rounds -.-
    dispatch[num_rounds](circ)
    
    return circ

def main():
    num_qubits = 11
    pers = np.linspace(0,0.2,1000)
    shots = 10_000
    lers = []
    for per in pers:
        circ = create_steane_error_circ(per)
        # run stim circuit
        sampler = circ.compile_detector_sampler()
        result = sampler.sample(shots=shots)
        l_errors = 0
        for num, row in enumerate(result):
            # We have an ordering of detectors, and we even additionally have the exact location
            # so we could just add the corresponding gates and measure? does our circuit still
            # exist here??
            is_row_correcting = False
            for elem in row[:-1]:
                if elem:
                    is_row_correcting = True
            if row[-1]:# and not is_row_correcting:
                l_errors += 1
        lers.append(l_errors/shots)
    plt.plot(pers, lers, label="data")
    plt.plot(pers, pers, label="Pseudo")
    plt.legend(loc="upper left")
    plt.savefig("./img/steane_thresh.png")
if __name__ == "__main__":
    main()
