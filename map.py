from config import *
import numpy as np
from random import random
from math import floor

from scipy.ndimage.filters import gaussian_filter

class Map:
    def __init__(self, zvals, x0, y0, w, h):
        self.__E = zvals
        self._x0 = x0
        self._y0 = y0
        self._w = w
        self._h = h
        self.recalculate_bounds()
    def of(size):
        zvals = np.zeros((size,size))
        m = Map(zvals, 0, 0, size, size)
        return m

    def recalculate_bounds(self):
        M = np.max(self.E)
        m = np.min(self.E)
        self.__thresh = m + (M - m) * k_ocean

    @property
    def E(self):
        return self.__E

    def __quadrant(self, xoff, yoff):
        return Map(self.__E, self._x0 + xoff, self._y0 + yoff, self._w / 2, self._h / 2)

    def __offset(self, xoff, yoff):
        return Map(self.__E, self._x0 + xoff, self._y0 + yoff, self._w, self._h)

    def offset_z(self, zoff):
        self.__E[self._x0 : self._x0+self._w, self._y0 : self._y0+self._h] += zoff

    def blur(self, sigma):
        self.__E = gaussian_filter(self.__E,sigma)
        self.recalculate_bounds()

    @property
    def neighbors(self):
        offs = [(0,1), (0,-1), (1,0), (-1,0)]
        neigh = []
        for x, y in offs:
            dx = x * self._w
            dy = y * self._h
            nx = self._x0 + dx
            ny = self._y0 + dy
            if 0 <= nx and nx + self._w <= self.__E.shape[0]:
                if 0 <= ny and ny + self._h <= self.__E.shape[1]:
                    neigh.append(self.__offset(dx, dy))
        return neigh

    @property
    def xvals(self):
        return range(floor(self._w))

    @property
    def yvals(self):
        return np.arange(floor(self._h))

    @property
    def ul(self):
        return self.__quadrant(0, 0)
    @property
    def ur(self):
        return self.__quadrant(self._w / 2, 0)
    @property
    def ll(self):
        return self.__quadrant(0, self._w / 2)
    @property
    def lr(self):
        return self.__quadrant(self._w / 2, self._h / 2)

    @property
    def center(self):
        return self[self._w / 2, self._h / 2]

    @property
    def smaller_than_pixel(self):
        return self._w < 1 and self._h < 1

    def __str__(self):
        return "Map %s\t%s\t%s\t%s" % (self._x0, self._y0, self._w, self._h)

    def __check_bounds(self, item):
        if len(item) != 2:
            raise AssertionError(str(item) + "does not have 2 elements!")
        item = round(item[0]), round(item[1])
        if not (0 <= item[0] < self._w) and not (0 <= item[1] < self._h):
            raise AssertionError(str(item) + " is out of bounds")
        return item

    @property
    def width(self):
        return self._w

    @property
    def height(self):
        return self._h

    def __getitem__(self, item):
        item = self.__check_bounds(item)
        return self.__E[item[0] + self._x0][item[1] + self._y0]
    def __setitem__(self, item, val):
        item = self.__check_bounds(item)
        self.__E[item[0] + self._x0][item[1] + self._y0] = val

    def in_ocean(self, r):
        val = self[r]
        return val < self.__thresh

def set_up_landscape(mapp, amount, levels):
    if mapp.smaller_than_pixel:
        return
    if levels <= 0:
        mapp.offset_z(random() * amount)
    for sub in [mapp.ul, mapp.ur, mapp.ll, mapp.lr]:
        set_up_landscape(sub, amount / mountain_factor, levels-1)
    mapp.recalculate_bounds()
