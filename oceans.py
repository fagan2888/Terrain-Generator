
from mathtools import neighbors

class Ocean:
    def __init__(self, depth):
        self.__depth = depth
        self.__points = set()
    def add(self, r):
        self.__points.add(tuple(r))
    def set_depth(self, depth):
        self.__depth = depth

    def contains_a_neighbor(r):
        for r2 in neighbors(r):
            if self.contains(r2):
                return True
        return False

    @property
    def size(self):
        return len(self.__points)

class Oceans:
    def __init__(self):
        self.__oceans = []

    def create_ocean(self, r, wdepth):
        ocean = Ocean(wdepth)
        ocean.add(r)
        self.__oceans.append(ocean)
        return ocean

    def add(self, r):
        other_oceans, relevant_oceans = [], []
        for ocean in self.__oceans:
            if ocean.contains_a_neighbor(r):
                relevant_oceans.add(ocean)
            else:
                other_oceans.add(ocean)
        joined = Ocean()
        overall_volume = 0
        for ocean in relevant_oceans:
            relevant_oceans.add(r)
            joined.add_all(ocean)
            overall_volume += joined.volume


        
