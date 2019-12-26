import numpy as np
from random import randint, random
from sys import argv
import math

N = 100
p = 0.1
if len(argv) == 3:
    N, p = argv[1], argv[2]

matrix = np.zeros((N, N), dtype = int) #utworzenie macierzy NxN pełnej zer
theta = math.log(p / (1-p)) #theta ze wzorku z hamiltonianu
E_current = 0 # aktualna liczba krawędzi grafu
how_many_iterations = N**3 # liczba iteracji (losowań grafu i jego zmiany)

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

def remove_vertex(row, col): #usuwa krawędź we skazanym miejscu
    global E_current
    matrix[row][col], matrix[col][row] = 0, 0
    E_current -= 1

#########################################

## główna część programu ##
for iteration in range (how_many_iterations):
    row, col = random_vertex() #losowanie węzła spoza przekątnej

    H_current = theta * E_current #obecny hamiltonian Hi=theta*E_i

    if matrix[row][col] == 0: #przypadek gdy wylosowaliśmy brak krawędzi (rozpatrujemy jej dodanie)
        H_new = theta * (E_current + 1) #nowy hamiltonian Hj=theta*E_j

        dH = H_new - H_current #delta hamiltonianów
        
        if random() < math.exp(dH): #z prawdopodobieństwem dodajemy krawędź
            add_vertex(row, col)

    else: #przypadek gdy wylosowaliśmy krawędź (rozpatrujemy jej usunięcie)
        H_new = theta * (E_current - 1) #nowy hamiltonian Hj=theta*E_j

        dH = H_new - H_current

        if random() < math.exp(dH): #z prawdopodobieństwem dodajemy krawędź
            remove_vertex(row, col)

    print("Edges", E_current)

np.savetxt("macierz_" + str(N) + "x" + str(N) + "_" + str(p), matrix, fmt = '%.1d')
