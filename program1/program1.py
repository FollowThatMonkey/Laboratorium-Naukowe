#!/usr/bin/python3.7
import numpy as np
from random import random
from scipy.special import comb
import matplotlib.pyplot as plt
import sys

N = 100 #liczba wierzchołków
p = 0.1 #prawdopodobieństwo krawędzi
if len(sys.argv) == 3: #jeśli w argumencie wywołania są dane
    N = int(sys.argv[1]) #to program zostanie wywołany z nimi
    p = float(sys.argv[2]) #1 argument to N, 2 argument to p
plot_range = [0, N-1] #to do wykresu się później przyda (zakres OX)
min_probability = 10**-4 #minimalne prawdopodobieństwo dla którego będzie wyświetlany wykresik

def random_graph(N, p):
    matrix = np.zeros((N, N), dtype = int)

    # tworzenie macierzy sąsiedztwa
    for row in range(N):
        for col in range(row + 1, N):
            rand = random()
            if rand < p:
                matrix[col][row], matrix[row][col] = 1, 1
    
    np.savetxt("macierz_" + str(N) + "x" + str(N) + "_" + str(p), matrix, fmt = '%.1d')

    ki = [] #tablica stopni wierzchołków
    for row in range(N):
        k = 0 #stopień aktualnego wierzchołka
        for col in range(N):
            k += matrix[row][col]
        ki.append(k)

    k_max = max(ki) #najwyższy stopień wierzchołka
    Nk = np.zeros(k_max + 1) # tablica z liczbą wierzchołków o k krawędziach
    for i in range(len(Nk)):
        Nk[i] = ki.count(i)
    P = Nk / N # rozklad prawdopodobienstwa z naszego losowego grafu

    #print("Nk =", Nk)
    #print("P =", P)

    return P

def binominal_dist(N, p):
    P = np.zeros(N - 1)

    for ki in range(N - 1):
        P[ki] = comb(N-1, ki) * p**ki * (1-p)**(N-1-ki)

    for i in range(N - 1):
       if P[i] > min_probability:
           plot_range[0] = i
           break
    for i in range(N-2, -1, -1):
        if P[i] > min_probability:
            plot_range[1] = i
            break
    print(plot_range)
    #print(P)

    return P


praktyka = random_graph(N, p)
teoria = binominal_dist(N, p)

# Wykresik
plt.bar(np.arange(len(praktyka)), praktyka, align = 'edge', width = 0.9)
plt.bar(np.arange(len(teoria)), teoria, align = 'edge', width = 0.4)
plt.title("Histogram P(k) dla wygenerowanego grafu losowego o N = " + str(N) + " oraz p = " + str(p) + " oraz danych teoretycznych", wrap=True)
plt.xlabel("k")
plt.ylabel("Prawdopodobieństwo")
plt.grid(True)
plt.xlim(plot_range[0], plot_range[1])

plt.savefig("histogram_" + str(N) + "x" + str(N) + "_" + str(p) + ".png", dpi = 240)
plt.show()
