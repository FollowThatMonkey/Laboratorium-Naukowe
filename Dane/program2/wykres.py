import matplotlib.pyplot as plt
from sys import argv, exit

x = []
y = []

if len(argv) != 2:
    exit()

with open(argv[1], 'r') as f:
    for line in f.readlines():
        tempx, tempy = line.split()
        x.append(int(tempx))
        y.append(int(tempy))

plt.scatter(x, y)
plt.show()
