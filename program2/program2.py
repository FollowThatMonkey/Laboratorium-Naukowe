import numpy as np
from random import randint, random
from sys import argv
import math
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

N = 100
p = 0.1
if len(argv) == 3:
    N, p = int(argv[1]), float(argv[2])

matrix = np.zeros((N, N), dtype = int) #utworzenie macierzy NxN pełnej zer
theta = math.log(p / (1-p)) #theta ze wzorku z hamiltonianu
E_current = 0 # aktualna liczba krawędzi grafu
how_many_iterations = int(1.5e6) # liczba iteracji (losowań grafu i jego zmiany)

## pomocniczne funkcje (używane niżej) ##

def random_vertex():
    row, col = randint(0, N-1), randint(0, N-1)
    while row == col:
        col = randint(0, N-1) #losowanie col != row (żeby nie wylosować przekątnej)
    return (row, col)

def add_vertex(row, col): #dodaje krawędź we wskazanym miejscu
    global E_current
    matrix[row][col], matrix[col][row] = 1, 1
    E_current += 1

def remove_vertex(row, col): #usuwa krawędź we wskazanym miejscu
    global E_current
    matrix[row][col], matrix[col][row] = 0, 0
    E_current -= 1

#########################################

## główna część programu ##
for iteration in range (how_many_iterations):
    row, col = random_vertex() #losowanie węzła spoza przekątnej

    H_current = theta * E_current #obecny hamiltonian Hi=theta*E_i

    if matrix[row][col] == 0: #przypadek gdy wylosowaliśmy brak krawędzi (rozpatrujemy jej dodanie)
        if theta >= 0:
            add_vertex(row, col)
        elif random() <= math.exp(theta):
            add_vertex(row, col)

    else: #przypadek gdy wylosowaliśmy krawędź (rozpatrujemy jej usunięcie)
        if -theta >= 0:
            remove_vertex(row, col)
        elif random() <= math.exp(-theta):
            remove_vertex(row, col)

#########################################

print("Number of edges:", E_current)
np.savetxt("macierz_" + str(N) + "x" + str(N) + "_" + str(p), matrix, fmt = '%.1d')

K = np.zeros(N, dtype = int) #tablica stopni wierzchołków
for row in range(N):
    for col in range(N):
        K[row] += matrix[row][col]

P = np.array([], dtype = float)
for i in range(min(K), max(K)+1):
    P = np.append(P, float(np.count_nonzero(K == i)))
P = P/N
zakres = np.arange(min(K), max(K)+1)

## wykres ##

plt.bar(zakres, P, width=0.9, label="Metoda MC")
plt.title("Histogram P(k) dla symulowanego grafu o N = " + str(N) + " oraz p = " + str(p))
plt.xlabel("k"); plt.ylabel("Prawdopodobieństwo")
plt.grid(True)
rozmiar = plt.gcf().get_size_inches()
plt.gcf().set_size_inches(rozmiar[0] * 2, rozmiar[1] * 2)
plt.gcf().gca().xaxis.set_major_locator(MaxNLocator(integer=True))
plt.legend()

plt.savefig("histogram_" + str(N) + "x" + str(N) + "_" + str(p) + ".png", dpi = 240)
plt.show()

#########################################

