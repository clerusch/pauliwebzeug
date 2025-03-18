from f2linalg.f2linalg import Mat2
import numpy as np
import networkx as nx
import pyzx as zx
from pyzx.pauliweb import PauliWeb
def make_test_graph_zz()->zx.Graph:
    new_order = [4,5,6,7,8,9,10,11,12,13,14,15]
    g = nx.Graph([(15,14),(15,12),\
                (13,9),(13,10),(12,8),(12,9),(14,10),(14,11),\
                    (8,4),(9,5),(10,6),(11,7)])
    g_reordered = nx.to_numpy_array(g, nodelist=new_order, dtype=np.uint8)
    return g, g_reordered
def make_md(g_reordered):
    # The 4 here is number of output spiders
    outs = 4
    N = g_reordered
    I_n = np.eye(outs, dtype=np.uint8)
    zeroblock = np.zeros((N.shape[1]-outs, outs), dtype=np.uint8)
    mdl = np.vstack((I_n, zeroblock))
    md = Mat2(np.hstack((mdl, N)))
    return md
def get_nullspace(md):
    mds = md.nullspace()
    nsm = [np.array(vec.data) for vec in mds]
    # internal = np.array([0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1])
    # nsm.append(internal)
    nsm = np.hstack(nsm)
    return nsm
def get_pws(d, v, g: zx.Graph):
    green_edges = set()
    red_edges = set()
    for i, val in enumerate(v.data):
        if val == 1:
            for edge in g.edges():
                if d[i] in edge:
                    # 1 if Z, 2 if X
                    vertex_color = g.ty[d[i]]
                    if vertex_color == 2:
                        if edge in green_edges:
                            green_edges.remove(edge)
                        else:
                            green_edges.add(edge)
                    elif vertex_color == 2:
                        if edge in red_edges:
                            red_edges.remove(edge)
                        else:
                            red_edges.add(edge)
    greenpw = PauliWeb(g)
    redpw = PauliWeb(g)
    for e in green_edges:
        greenpw.add_edge(e, 'Z')
    for e in red_edges:
        redpw.add_edge(e, 'X')
    print(red_edges)
    return greenpw, redpw

                    


def main():
    g, gr, new_order = make_test_graph_zz()
    md = make_md(gr)
    print(md)
    ns = get_nullspace(md)
    # my_vec = np.array([[0,1,3,5]])
    # my_vev_2 = np.array([[6,7,8,9]])
    # mat = np.hstack((my_vec.T, my_vev_2.T))
    print(ns)
    mdns = np.hstack([np.array(vec.data)for vec in md.nullspace()])
    v = mdns[:,0]
    d = new_order
    pws = get_pws(d, v, lg)
    print(pws)
    # zx.draw(lg, labels=True)
    # pw = PauliWeb(lg)
    # pw.add_edge((11,7), 'X')
    zx.draw(lg, labels=True, pauli_web=pws[1])
    # for e in es:
    #     g.set_edge_type(e,zx.EdgeType.HADAMARD)
    # internal = np.array([[0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1]])
    # print(np.linalg.matrix_rank(ns))
    # print(ns[0].shape)
    # print(internal.T.shape)
    # ns2 = np.hstack((ns, internal.T))
    # print(ns2)
    # print(np.linalg.matrix_rank(ns2))
    # pass











if __name__ == "__main__":
    main()