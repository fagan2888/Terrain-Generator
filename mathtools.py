import numpy as np

def grad(V):
    size = V.shape[0]
    A = np.zeros((size, size, 2))
    for x in range(size):
        for y in range(size):
            A[x][y] = gradAt(V, x, y)
    return A

def gradAt(V, i, j):
    size = V.shape[0]
    val = V[i][j]
    if i == size-1:
        dx = val - V[i-1][j]
    else:
        dx = V[i+1][j] - val
    if j == size-1:
        dy = val - V[i][j-1]
    else:
        dy = V[i][j+1] - val
    return np.array([dx, dy])

def generate(size, f):
    A = np.zeros((size, size))
    for x in range(size):
        for y in range(size):
            A[x][y] = f(x, y)
    return A
