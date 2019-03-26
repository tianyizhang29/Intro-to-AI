import numpy as np

class Grid:
    def __init__(self, width, length):
        self.width = width
        self.length = length
        self.grid = self.generate()
    
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
        return grid
