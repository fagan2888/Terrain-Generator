import matplotlib.pyplot as plt

from mathtools import grad, generate

def plot_gradient(V, loc):
    g = grad(V)
    gx = generate(g.shape[0], lambda i, j: g[i][j][0])
    gy = generate(g.shape[0], lambda i, j: g[i][j][1])
    fig = plt.imshow(V, interpolation='none')
    plt.savefig(loc + "-original.png")
    fig = plt.imshow(gx, interpolation='none')
    plt.savefig(loc + "-ddx.png")
    fig = plt.imshow(gy, interpolation='none')
    plt.savefig(loc + "-ddy.png")

def plot(data, file=None):
    fig = plt.imshow(data.T, interpolation='none')
    fig.set_cmap('terrain')
    plt.axis('off')
    if file is not None:
        plt.savefig(file, bbox_inches='tight', pad_inches=0)
    else:
        plt.show(block=False)
