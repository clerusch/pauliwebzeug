import matplotlib.pyplot as plt
import pyzx
import warnings

def draw_g(g:pyzx.Graph, location:str)->None:
    # Draw and save manually
    with warnings.catch_warnings():
        # This is for the plt.show() warning
        warnings.simplefilter("ignore", category=UserWarning)
        fig = pyzx.draw_matplotlib(g, labels=True)
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
    fig.savefig("img/"+location+".png", dpi=400, bbox_inches="tight")