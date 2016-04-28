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
        ds = k_tough * (k_cap * np.linalg.norm(v) - self.__s)
        s = self.__s + ds
        mapp[self.r] -= ds
        self.__track(r)
        self.__update(r, s)
        end = self.__is_at_end(mapp)
        return end

    def __is_at_end(self, mapp):
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

    def __update(self, r, s):
        self.__x = r[0]
        self.__y = r[1]
        self.__s = s

    def __gen_raindrop(board_size):
        return Raindrop(randint(0, board_size-1), randint(0, board_size-1), 0, [])

    def gen_raindrops(quantity_rain, board_size):
        return [Raindrop.__gen_raindrop(board_size) for _ in range(quantity_rain)]

    @property
    def r(self):
        return np.array([self.__x, self.__y])

    def __track(self, loc):
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
        for rain in rains:
            ended = rain.step(mapp)
            if ended:
                rain.finish(finished)
            else:
                rains2.append(rain)

        rains = rains2
    return Raindrop.alltrails(rains) + finished
