import numpy as np
from config import *
from random import randint
from mathtools import gradAt

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
            a = -k_steep * gradAt(E, round(R[i][0]), round(R[i][1]))
            v = a
            r = (v + V[i]) / 2 + R[i]
            if round(r[0]) < 0 or round(r[0]) >= size or round(r[1]) < 0 or round(r[1]) >= size or mapp.in_ocean(r):
                finished.append(trails[i])
                continue
            trail = trails[i]
            trail.append(r)
            s = S[i] + k_tough * (k_cap * np.linalg.norm(V[i]) - S[i])
            mapp[R[i]] -= s - S[i]
            R2.append(r)
            V2.append(v)
            S2.append(s)
            trails2.append(trail)
        V = V2
        R = R2
        S = S2
        trails = trails2
    return trails + finished
