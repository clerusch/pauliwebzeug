import pyzx as zx 
from graph_loader import load_graph
import networkx as nx
from f2linalg.f2linalg import Mat2
import numpy as np
from pyzx.pauliweb import PauliWeb
from typing import Dict
def ordered_nodes(g:zx.Graph):
    original = list(g.vertices())
    outputs = [v for v in original if v in g.outputs() or v in g.inputs()]
    vertices = outputs + [v for v in original if g.ty[v]!=0 and v not in outputs]
    index_map = {vertices.index(item): original_index for original_index, item in enumerate(original) if item in vertices}

    # index_map = {original_index: vertices.index(item) for original_index, item in enumerate(original) if item in vertices}
    return vertices, index_map
def get_pw(index_map: Dict, v:np.array,g):
    """
    Create Pauliweb on given graph according to kernel vector v
    """
    # print(np.nonzero(v)[0])
    # w = np.zeros(len(g.vertices()), dtype=np.uint8)
    # for i, val in enumerate(v):
    #     if val == 1:
    #         w[index_map[i]+(len(g.outputs()+g.inputs()))] = 1
    print(index_map)
    outs = len(g.inputs())+len(g.outputs())
    color = g.ty[index_map[np.nonzero(v)[0][0]-outs]]
    
    print(color)
    # print(w)
    
    pw = PauliWeb(g)
    # Cuz pauliweb type will be opposite colored
    if color == 1:
        pwtype = 'X'
    elif color == 2:
        pwtype = 'Z'
    else:
        raise ValueError('Color of the vertex should be 1 or 2')
    print(pwtype)
    red_edges = set()
    green_edges = set()
    for i in np.nonzero(v)[0]:
        node_color =  g.ty[index_map[i-outs]]
        for edge in g.edges():
            if index_map[i-outs] in edge:
                if node_color == 1:
                    if edge in green_edges:
                        green_edges.remove(edge)
                    else:
                        green_edges.add(edge)
                elif node_color == 2:
                    if edge in red_edges:
                        red_edges.remove(edge)
                    else:
                        red_edges.add(edge)
    for e in red_edges:
        pw.add_edge(e,'Z')
    for e in green_edges:
        pw.add_edge(e,'X')
    return pw
def make_rg(oldg):
    g = oldg.copy()
    for node in g.vertices():
        nodecolor = g.ty[node]
        
        for neighbor in g.neighbors(node):
            # print(node, neighbor)
            if g.ty[neighbor] == nodecolor:
                row = (g.row(node)+g.row(neighbor)) /2
                qubit = (g.qubit(node)+g.qubit(neighbor)) /2
                oldg.remove_edge((neighbor, node))
                new_vertex = oldg.add_vertex(ty=(nodecolor%2)+1, qubit=qubit, row=row)
                oldg.add_edge((node, new_vertex))
                oldg.add_edge((new_vertex, neighbor))
                g = oldg.copy()
    return oldg
def get_detection_webs(g:zx.Graph):
    """
    Compute the detection webs for the given graph.
    """
    new_order, index_map = ordered_nodes(g)
    ng = nx.Graph(g.edges())
    outs = len(g.inputs())+len(g.outputs())
    N = nx.to_numpy_array(ng, nodelist=new_order, dtype=np.uint8)
    I_n = np.eye(outs, dtype=np.uint8)
    zeroblock = np.zeros((N.shape[1]-outs, outs), dtype=np.uint8)
    mdl = np.vstack((I_n, zeroblock))
    md = Mat2(np.hstack((mdl, N)))
    # adds a stack of single-entry rows to eliminate outputs of the graphs firing vector
    no_output = np.hstack((np.eye(2*outs, dtype=np.uint8), np.zeros((2*outs, len(md.data[0])-2*outs), dtype=np.uint8)))
    md_no_output = Mat2(np.vstack((md.data, no_output)))
    # print(md_no_output.nullspace())
    mdnons = np.hstack([np.array(vec.data)for vec in md_no_output.nullspace()])
    # print(mdnons)
    pws = []
    for v in mdnons.T:
        print(v)
        pw = get_pw(index_map, v,g)
        pws.append(pw)
    return pws
    # zx.draw(lg, labels=True)
    # pw = PauliWeb(lg)
    # pw.add_edge((11,7), 'X')
    zx.draw(g, labels=True, pauli_web=pw)

def main():
    # g = load_graph("zxgs/xx_stab_choi.zxg")
    # g.set_inputs([4,5])
    # g.set_outputs([6,7])
    # pws = get_detection_webs(g)
    # print(pws)
    test_g4 = load_graph("zxgs/2_rounds_steane_rg.zxg")
    test_g4.set_inputs([19,20,21,17,16,15,14])
    test_g4.set_outputs([65,73,71,62,60,72,67])
    pws = get_detection_webs(test_g4)
if __name__ == '__main__':
    main()