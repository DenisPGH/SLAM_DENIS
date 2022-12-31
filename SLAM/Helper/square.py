from random import randrange

from matplotlib import pyplot as plt
from matplotlib.colors import ListedColormap
import numpy as np


class Square:
    def __init__(self, state, pos):
        self.state = state
        self.pos = pos
        self.adj_sqs = []
        self.optimal_sq = []

    def __repr__(self):
        return str(self.state)

dim = 20
#grid = np.array([[Square(randrange(2), [x, y]) for y in range(dim)] for x in range(dim)])
grid = np.array([[Square(1, [x, y]) for y in range(dim)] for x in range(dim)])
grid_np = np.array([[grid[x, y].state for y in range(dim)] for x in range(dim)])







plt.pcolor(np.arange(-0.5, dim), np.arange(-0.5, dim), grid_np, cmap=ListedColormap(['green', 'white']))
plt.gca().set_aspect('equal')  # show square as square
plt.xticks(range(dim))
plt.yticks(range(dim))
plt.show()



