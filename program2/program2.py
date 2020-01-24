import numpy as np
from random import randint, random
from sys import argv
import math
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from statistics import mean

N = 100
p = 0.1
if len(argv) == 3:
    N, p = int(argv[1]), float(argv[2])

matrix = np.zeros((N, N), dtype = int) #utworzenie macierzy NxN pełnej zer
theta = math.log(p / (1-p)) #theta ze wzorku z hamiltonianu
E_current = 0 # aktualna liczba krawędzi grafu
how_many_iter = 800 # liczba iteracji co ile będzie sprawdzane czy <E>=const.
E_mean_list = [0] * how_many_iter #tablica lizcby krawędzi grafu z ostatnich iteracji
E_mean_current = 0 #obecna średnia liczba krawędzi
how_many_previous = 10 #liczba mówiąca ile ostatnich średnich będzie porównywana
E_mean_previous = [math.nan]*how_many_previous #tablica zawierająca określoną liczbę ostatnio liczonych średnich
comparison_accuracy = 15 #dokładność z którą porównywane będą średnie

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
iteration = 0
mean_iteration = 0 #iterator potrzebny do dodawania poprzednich średnich na odpowiednie miejsce w tablicy E_mean_previous
while True:
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
    
    E_mean_list[iteration % how_many_iter] = E_current

    if iteration % how_many_iter == 0:
        E_mean_current = int(mean(E_mean_list))

        print("Iteracja =", iteration, ", E_mean_current =", E_mean_current,", E_mean_previous =", E_mean_previous)

        if all(abs(E_mean_current - prev_mean) <= comparison_accuracy for prev_mean in E_mean_previous): # jeśli wszystkie średnie z tablicy są równe aktualnej średniej z dokładnością do comparison_accuracy, to break
            break
        else: #jeśli średnie z dokładnoscią do pewnej liczby się różnią, to:
            E_mean_previous[mean_iteration%how_many_previous] = E_mean_current #dodanie aktualnej średniej do tablicy poprzednich średnich
            mean_iteration += 1 #zwiększenie iteratora mówiącego którą średnią z poprzednich (z tablicy) teraz będziemy rozpatrywać
   
    iteration += 1

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

