import numpy as np
from config import *
from random import randint
from mathtools import gradAt

class Raindrop:
    def __init__(self, x, y, s, trail):
        self.__x = x
        self.__y = y
        self.__s = s
        self.__trail = trail

    def step(self):
        pass

    def update(self, r, s):
        return Raindrop(r[0], r[1], s, self.__trail)

    def gen_raindrop(board_size):
        return Raindrop(randint(0, board_size-1), randint(0, board_size-1), 0, [])

    def gen_raindrops(quantity_rain, board_size):
        return [Raindrop.gen_raindrop(board_size) for _ in range(quantity_rain)]

    @property
    def x(self):
        return self.__x
    @property
    def y(self):
        return self.__y
    @property
    def r(self):
        return np.array([self.x, self.y])
    @property
    def s(self):
        return self.__s

    def track(self, loc):
        self.__trail.append(loc)
    def finish(self, finished):
        finished.append(self.__trail)

    def alltrails(rains):
        return [rain.__trail for rain in rains]

def erode(mapp, rain, steps):
    size = mapp.width
    rains = Raindrop.gen_raindrops(rain, size)
    finished = []
    for count in range(steps):
        rains2 = []
        for i in range(len(rains)):
            v = -k_steep * gradAt(mapp.E, round(rains[i].x), round(rains[i].y))
            r = v + rains[i].r
            end = round(r[0]) < 0 or round(r[0]) >= size or round(r[1]) < 0 or round(r[1]) >= size
            if not end:
                end = mapp.in_ocean(r)
            if end:
                rains[i].finish(finished)
                continue
            ds = k_tough * (k_cap * np.linalg.norm(v) - rains[i].s)
            s = rains[i].s + ds
            mapp[rains[i].r] -= ds
            rains[i].track(r)
            rains2.append(rains[i].update(r, s))
        rains = rains2
    return Raindrop.alltrails(rains) + finished
