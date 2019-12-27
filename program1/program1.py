import numpy as np
from random import random
from scipy.special import comb
import matplotlib.pyplot as plt
import sys, math

N = 100 #liczba wierzchołków
p = 0.1 #prawdopodobieństwo krawędzi
if len(sys.argv) == 3: #jeśli w argumencie wywołania są dane
    N, p = int(sys.argv[1]), float(sys.argv[2]) #to program zostanie wywołany z nimi, 1 argument to N, 2 argument to p

def random_graph(N, p):
    matrix = np.zeros((N, N), dtype = int)

    # tworzenie macierzy sąsiedztwa
    for row in range(N):
        for col in range(row + 1, N):
            rand = random()
            if rand < p:
                matrix[col][row], matrix[row][col] = 1, 1
    
    np.savetxt("macierz_" + str(N) + "x" + str(N) + "_" + str(p), matrix, fmt = '%.1d')

    ki = np.zeros(N, dtype = int) #tablica stopni wierzchołków
    for row in range(N):
        for col in range(N):
            ki[row] += matrix[row][col]

    return ki

def binominal_dist(N, p):
    P = np.zeros(N)

    for ki in range(N):
        P[ki] = comb(N-1, ki) * p**ki * (1-p)**(N-1-ki)

    return P


praktyka = random_graph(N, p)
teoria = binominal_dist(N, p)

# Wykresik
num_bins = (np.amax(praktyka)-np.amin(praktyka)) - 1

plt.hist(praktyka, bins = num_bins, density = True, rwidth = 0.9)
plt.bar(np.arange(len(teoria)), teoria, color = 'y', width = 0.7, alpha = 0.5)
plt.title("Histogram P(k) dla wygenerowanego grafu losowego o N = " + str(N) + " oraz p = " + str(p) + " oraz danych teoretycznych", wrap=True)
plt.xlabel("k")
plt.ylabel("Prawdopodobieństwo")
plt.xlim(np.amin(praktyka) - int(math.sqrt(N/10)), np.amax(praktyka) + int(math.sqrt(N/10)))
plt.grid(True)

plt.savefig("histogram_" + str(N) + "x" + str(N) + "_" + str(p) + ".png", dpi = 240)
plt.show()
