import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d.axes3d import Axes3D

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

def plot3d(data, file=None):
    def squish_plot(amount):
        low, high = ax.get_zlim()
        diff = high - low
        low -= diff * amount
        high += diff * amount
        ax.set_zlim(low, high)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_axis_off()
    x = np.array(range(data.shape[0]))
    x, y = np.meshgrid(x,x)

    ax.plot_surface(x,y,data, cmap='terrain', rstride=1, cstride=1,linewidth=0)

    squish_plot(2)
    if file is not None:
        plt.savefig(file, bbox_inches='tight', pad_inches=0, dpi=400)
    else:
        plt.show(block=False)
    plt.cla()
    plt.clf()


def plot(data, file=None):
    fig = plt.imshow(data.T, interpolation='none')
    fig.set_cmap('terrain')
    plt.axis('off')
    if file is not None:
        plt.savefig(file, bbox_inches='tight', pad_inches=0, dpi=400)
    else:
        plt.show(block=False)
    plt.cla()
    plt.clf()
