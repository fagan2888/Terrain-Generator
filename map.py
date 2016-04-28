from config import *
import numpy as np
from random import random
from math import floor

from oceans import Oceans

from mathtools import is_min, neighbors

from scipy.ndimage.filters import gaussian_filter

class Map:
    def __init__(self, E, x0, y0, w, h):
        self.__E = E
        self._x0 = x0
        self._y0 = y0
        self._w = w
        self._h = h
        self.__range = 0
        self.__oceans = Oceans()
    def of(size):
        E = np.zeros((size,size))
        m = Map(E, 0, 0, size, size)
        return m

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
        self.flood()

    def flood(self):
        M = np.max(self.E)
        m = np.min(self.E)
        self.__range = M - m
        thresh = m + self.__range * k_ocean
        for x in self.xvals:
            for y in self.yvals:
                if self.E[x,y] < thresh:
                    self.__oceans.add((x,y))

    @property
    def neighbors(self):
        offs = neighbors((0,0))
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
        return self.__oceans.in_ocean(r)

    def at_min(self, r):
        return is_min(self.E, r[0], r[1])

    def add_droplet(self, r):
        u = self.ocean_at(r)
        if u.is_empty:
            u = self.__oceans.new_ocean(r)
        h_add = q_droplet * self.__range
        h_new = h_add + u.depth
        dropspots = []
        for x, y in u:
            for r2 in self.__neighbors_of((x,y)):
                if r2 not in u:
                    if self[r2] < self[x,y]:
                        dropspots.append(r2)
                        h_new -= q_droplet * self.__range
                        continue
                    h_adj = h_new * u.size / (u.size + 1)
                    if self[r2] < h_adj:
                        self.__oceans.new_ocean(r2)
                        u.add(r2)
                        h_new = h_adj
                        continue
        u.set_depth(h_new)
        return dropspots


def set_up_landscape(mapp, amount, levels):
    def setup(mapp, amount, levels):
        if mapp.smaller_than_pixel:
            return
        if levels <= 0:
            mapp.offset_z(random() * amount)
        for sub in [mapp.ul, mapp.ur, mapp.ll, mapp.lr]:
            setup(sub, amount / mountain_factor, levels-1)
    setup(mapp, amount, levels)
    mapp.flood()
