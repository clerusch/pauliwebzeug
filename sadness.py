import pyzx as zx
import stim
from lib.graph_loader import load_graph  # your custom loader

def zxg_to_stim(filename, num_ancillas=5, num_data=7):
    g = load_graph(filename)

    input_vertices = g.inputs()
    output_vertices = g.outputs()
    total_qubits = num_ancillas + num_data

    # Build wire map from input to output vertex
    qubit_wires = []

    for idx in range(total_qubits):
        input_v = input_vertices[idx]
        wire = [input_v]
        current = input_v

        while True:
            neighbors = [n for n in g.neighbors(current) if g.type(n) != 'BOUNDARY']
            if not neighbors:
                break
            next_v = neighbors[0]
            wire.append(next_v)
            g.remove_edge(current, next_v)
            current = next_v

        qubit_wires.append(wire)

    # Start building stim circuit
    circuit = stim.Circuit()

    for q, wire in enumerate(qubit_wires):
        for v in wire[1:]:  # skip input node
            vtype = g.type(v)
            phase = g.phase(v)

            if vtype == 'Z':
                if isinstance(phase, str):
                    # symbolic measurement
                    circuit.append("# symbolic phase: Z({}) on qubit {}".format(phase, q))
                    circuit.append("M", [q])
                elif phase == 1:
                    circuit.append("Z", [q])
            elif vtype == 'X':
                circuit.append("H", [q])
            # TODO: check for Hadamard edge connections → CX / CZ

        # optional: end of ancilla wire
        if q < num_ancillas and "M" not in str(circuit[-1]):
            circuit.append("M", [q])

    return circuit

if __name__ == "__main__":
    filename = "zxgs/steane_style_steane_2_rounds.zxg"
    circ = zxg_to_stim(filename)
    print("Generated Stim Circuit:\n")
    print(circ)
    with open("converted.stim", "w") as f:
        f.write(str(circ))