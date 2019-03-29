import numpy as np
import random

terrian_type = {1:"flat", 2:"hilly", 3:"forested", 4:"caves"}

class Map:
    def __init__(self, width, length):
        self.width = width
        self.length = length
        self.grid, self.belief = self.generate()
        self.target_location = (random.randint(0, self.width - 1), random.randint(0, self.length - 1))
    
    def generate(self):
        total = self.width * self.length
        grid = np.zeros(total)
        for i in range(total):
            if i < total * 0.2:
                grid[i] = 1
            elif i < total * 0.5:
                grid[i] = 2
            elif i < total * 0.8:
                grid[i] = 3
            else:
                grid[i] = 4
        np.random.shuffle(grid)
        grid = np.reshape(grid, (self.width, self.length))
        return grid, np.full((self.width, self.length), 1 / total)

    def get_terrian_type(self, x, y):
        return terrian_type[(self.grid[x][y])]
