import numpy as np
from random import random
from scipy.special import comb
import matplotlib.pyplot as plt
import sys, math

N = 100 #liczba wierzchołków
p = 0.1 #prawdopodobieństwo krawędzi
if len(sys.argv) == 3: #jeśli w argumencie wywołania są dane
    N, p = int(sys.argv[1]), float(sys.argv[2]) #to program zostanie wywołany z nimi, 1 argument to N, 2 argument to p

#########################################

## pomocniczne funkcje ##

def random_graph(N, p): # tworzenie losowego grafu klasyczną metodą
    matrix = np.zeros((N, N), dtype = int) # tworzenie macierzy pełnej zer o rozmiarze NxN

    # tworzenie macierzy sąsiedztwa
    for row in range(N):
        for col in range(row + 1, N):
            if random() < p:
                matrix[col][row], matrix[row][col] = 1, 1
    
    np.savetxt("macierz_" + str(N) + "x" + str(N) + "_" + str(p), matrix, fmt = '%.1d') # zapis macierzy do pliku

    K = np.zeros(N, dtype = int) #tablica stopni wierzchołków, z niej dalej będzie tworzony histogram P(k)
    for row in range(N):
        for col in range(N):
            K[row] += matrix[row][col]

    P = np.array([], dtype = float) #tworzenie pustej tablicy
    for i in range(min(K), max(K)+1): #pętla w zakresie od minimalnego do maksymalnego stopnia wierzhołka K
        P = np.append(P, float(np.count_nonzero(K == i))) #zliczenie liczby stopni danego weirzchołka K
   
    zakres = np.arange(min(K), max(K)+1) # zakres dla krtórego będzie tworzony histogram!

    return zakres, P/N

def binominal_dist(N, p): # P(k) ze wzoru
    P = np.zeros(N)

    for ki in range(N):
        P[ki] = comb(N-1, ki) * p**ki * (1-p)**(N-1-ki)

    return P

#########################################

## wywołanie powyższych funkcji ##

praktyka = random_graph(N, p)
teoria = binominal_dist(N, p)

#########################################

## Wykresik ##

plt.bar(praktyka[0], praktyka[1], align="center", width=0.9, label = "Graf losowy")
plt.bar(np.arange(len(teoria)), teoria, align = "center", width = 0.6, alpha = 0.5, label="Rozkład dwumianowy") # utworzenie wykresu słupkowego P(k) dla wzorku teoretycznego
plt.title("Histogram P(k) dla wygenerowanego grafu losowego o N = " + str(N) + " oraz p = " + str(p) + " oraz danych teoretycznych", wrap=True)
plt.xlabel("k")
plt.ylabel("Prawdopodobieństwo")
plt.xlim(np.amin(praktyka[0]) - int(math.sqrt(N/10)), np.amax(praktyka[0]) + int(math.sqrt(N/10)))
plt.legend()
plt.grid(True)

plt.savefig("histogram_" + str(N) + "x" + str(N) + "_" + str(p) + ".png", dpi = 240) # zapisanie wykresu do pliku
plt.show()

#########################################
