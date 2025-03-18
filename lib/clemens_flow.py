import pyzx as zx
from typing import Dict, Set, Tuple, Optional
from pyzx.graph.base import BaseGraph, VT, ET
import numpy as np
from pyzx.linalg import Mat2

def gflow_aux(g: BaseGraph[VT, ET], inp: Set[VT], out: Set[VT], k: int,\
              corr: Dict[VT,Set[VT]], l: Dict[VT, int], processed: Set[VT]) \
              -> Optional[Tuple[Dict[VT, int], Dict[VT, Set[VT]]]]:
    """
    k-th iteration step of auxilary gflow function.
    """
    out_s = out.difference(inp)
    C = set()
    non_outs = set(g.vertices()).difference(out)
    g_mat = Mat2([[1 if g.connected(v,w) else 0 for v in non_outs] for w in out_s])  #np.zeros((n,n), dtype=np.uint8)

    zerovec = Mat2.zeros(len(non_outs), 1)
    for index, u in enumerate(non_outs):
        I_u = zerovec.copy() 
        I_u.data[index][0] = 1
        X0 = g_mat.solve(I_u)
        if X0 != zerovec:
            C.add(u)
            corr[u] = {tuple(map(tuple, X0.data))}
            l[u] = k 
    if not C:
        # base case
        if out == set(g.vertices()):
            return (l, corr)
        else:
            print(out, g.vertices())
            return None
    else:
        print(k)
        return gflow_aux(g, inp, out.union(C), k+1, corr, l, processed)


def gflow(g: BaseGraph[VT, ET],inp: Set[VT],out: Set[VT])\
    -> Optional[Tuple[Dict[VT, int], Dict[VT, Set[VT]]]]:
    """
    Input:
        g: A grap-like zx diagram.
        inp: Set of input vertices.
        out: Set of output vertices.
    Output:
        If there is no gflow, None. else:
        Tuple(Order, Correction) with:
        Order: A dictionary mapping vertices to their order in the gflow.
        Correction: A dictionary mapping vertices to their correction sets.
    Based on Algorithm in https://arxiv.org/pdf/0709.2670
    """
    
    l = {}
    corr = {}
    processed = set()
    for v in out:
        l[v] = 0
    return gflow_aux(g, inp, out.difference(inp), 1, corr, l, processed)

def main():
    from graph_loader import load_graph
    # import networkx as nx
    import matplotlib.pyplot as plt
    import warnings
    warnings.simplefilter("ignore")
    # Disable interactive mode to prevent automatic pop-ups
    plt.ioff()
    plt.switch_backend("Agg")
    # mat = gflow(lg, lg.inputs(), lg.outputs())
    # G = zx.from_adjacency_matrix(mat)
    # plt.figure(figsize=np.shape(mat))
    
    # zx.draw_matplotlib(G, labels=True)
    # plt.savefig("img/zz_rg_mat_graph.png")
    # lg = load_graph("zxgs/cnot_graphlike.zxg")
    c = zx.qasm("""
    qreg q[2];
    cx q[0], q[1];
    """)
    g = c.to_graph()
    fig = zx.draw(g, labels=True)
    # Save the figure instead of displaying it
    fig.savefig("img/cnot.png", format="png", dpi=300)
    plt.close(fig)  # Close the figure to prevent it from popping up# mat = gflow(lg, lg.inputs(), lg.outputs())
    # lg.set_inputs([0,1])
    # lg.set_outputs([2,3])
    from pyzx.gflow import gflow as flo
    f = flo(g)
    print(f)
    gf = gflow(g, set([0,1]), set([4,5]))
    print(gf)
    

if __name__ == "__main__":
    main()