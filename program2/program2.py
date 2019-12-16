from random import random, randint #losowa liczba z zakresu <0,1), losowa liczba z zakresu <a,b>
from sys import argv #stare dobre argv
import numpy as np
import math
#from scipy.special import comb #symbol newtona
#import matplotlib.pyplot as plt

N = 100
p = 0.9
if len(argv) == 3:
    N, p = int(argv[1]), float(argv[2])

def random_vertex():
    row, col = randint(0, N-1), randint(0, N-1)
    while row == col:
        col = randint(0, N-1)
    return (row, col)

matrix = np.zeros((N, N), dtype = int) #macierz pełna zer
theta = math.log((1-p) / p)
edges = 0 #liczba krawędzi
how_many_iterations = N**3

for iteracja in range(how_many_iterations):
    row, col = random_vertex()
    
    H_current = -theta * edges
    H_new = 0

    if matrix[row][col] == 0:
        H_new = -theta * (edges+1)
    else:
        H_new = -theta * (edges-1)
    dH = H_new - H_current
    if dH < 0:
        if matrix[row][col] == 0:
            matrix[row][col], matrix[col][row] = 1, 1
            edges += 1
        else:
            matrix[row][col], matrix[col][row] = 0, 0
            edges -= 1
    else:
        rand = random()
        if rand < math.exp(dH):
            if matrix[row][col] == 0:
                matrix[row][col], matrix[col][row] = 1, 1
                edges += 1
            else:
                matrix[row][col], matrix[col][row] = 0, 0
                edges -= 1

print(edges)
np.savetxt("macierz_" + str(N) + "x" + str(N) + "_" + str(p), matrix, fmt = '%.1d')
