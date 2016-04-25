import numpy as np
from config import *
from random import randint
from mathtools import gradAt
from time import time

time_matrix = {
        'a' : 0,
        'r' : 0,
        'erode' : 0,
        'in ocean' : 0,
        's' : 0,
        'calc_end' : 0,
        'list' : 0
    }

def erode(mapp, rain, steps):
    size = mapp.width
    R = [np.array([
                    randint(0, size-1), randint(0, size-1)
                ])
             for _ in range(rain)]
    V = [np.zeros(2) for _ in range(rain)]
    S = [0 for _ in range(rain)]
    trails = [[] for _ in range(rain)]
    finished = []
    E = mapp.data
    for count in range(steps):
        R2 = []
        V2 = []
        S2 = []
        trails2 = []
        for i in range(len(R)):
            t = time()
            a = -k_steep * gradAt(E, round(R[i][0]), round(R[i][1]))
            time_matrix['a'] += time() - t
            v = a
            t = time()
            r = (v + V[i]) / 2 + R[i]
            time_matrix['r'] += time() - t
            t = time()
            end = round(r[0]) < 0 or round(r[0]) >= size or round(r[1]) < 0 or round(r[1]) >= size
            time_matrix['calc_end'] += time() - t
            if not end:
                t = time()
                end = mapp.in_ocean(r)
                time_matrix['in ocean'] += time() - t
            if end:
                finished.append(trails[i])
                continue
            t = time()
            ds = k_tough * (k_cap * np.linalg.norm(V[i]) - S[i])
            s = S[i] + ds
            time_matrix['s'] += time() - t
            t = time()
            mapp[R[i]] -= ds
            time_matrix['erode'] += time() - t
            t = time()
            trail = trails[i]
            trail.append(r)
            R2.append(r)
            V2.append(v)
            S2.append(s)
            trails2.append(trail)
            time_matrix['list'] += time() - t
        V = V2
        R = R2
        S = S2
        trails = trails2
    return trails + finished
