import numpy as np

from erode import *
from config import *
from time import time
import matplotlib.pyplot as plt
from map import Map, set_up_landscape
from graphics import plot, plot_gradient, plot3d

scatter = False
size = 128
runs = 1000
debug = Map.of(size)
set_up_landscape(debug, 1, skip_levels)

debug.blur(2)
plot(debug.E, file="debug-before.png")
trs = []

start = time()

for count in range(runs):
    if count % 4 == 0:
        print("%5.2f%%" % (count / runs * 100))
    trs += erode(debug, 100, 100)

end = time()

print("Took %6.2fs" % (end - start))

plot3d(debug.E, file="debug-carved.png")

plt.clf()
plt.cla()

plot(debug.E, file="debug-after.png")

for tr in trs:
    u, v = [(x[0]) for x in tr], [(y[1]) for y in tr]
    if scatter:
        plt.scatter(u, v, c = range(len(tr)))
    else:
        plt.plot(u, v)

plt.show()
