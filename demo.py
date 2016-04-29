
import matplotlib.pyplot as plt
from map import *
from erode import *
from config import *
from graphics import plot, plot3d

size = 512
skip_levels = 3
runs = 5000

demo = Map.of(size)
set_up_landscape(demo, 1, skip_levels)

def plotboth(file):
    plot(demo.E, file=file)
    plot3d(demo.E, file=file[:-len(".png")] + "_3d.png")

plotboth("basic_randomized.png")

demo.blur(8)

plotboth("basic_gaussed.png")

trs = []
for count in range(runs):
    if count % 10 == 0:
        print("%5.2f%%" % (count / runs * 100))
    trs += erode(demo, 100, 100)

plotboth("basic_carved.png")
