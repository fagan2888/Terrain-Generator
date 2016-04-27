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

    def step(self, mapp):
        v = -k_steep * gradAt(mapp.E, round(self.__x), round(self.__y))
        r = self.r + v
        self.__x = r[0]
        self.__y = r[1]
        end = self.is_at_end(mapp)
        return v, r, end

    def is_at_end(self, mapp):
        size = mapp.width
        if round(self.__x) < 0:
            return True
        if round(self.__x) >= size:
            return True
        if round(self.__y) < 0:
            return True
        if round(self.__y) >= size:
            return True
        if mapp.in_ocean(self.r):
            return True
        if mapp.at_min(self.r):
            return True
        return False

    def update(self, r, s):
        self.__x = r[0]
        self.__y = r[1]
        self.__s = s

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
            v, r, end = rains[i].step(mapp)
            if end:
                rains[i].finish(finished)
                continue
            ds = k_tough * (k_cap * np.linalg.norm(v) - rains[i].s)
            s = rains[i].s + ds
            mapp[rains[i].r] -= ds
            rains[i].track(r)
            rains[i].update(r, s)
            rains2.append(rains[i])
        rains = rains2
    return Raindrop.alltrails(rains) + finished
