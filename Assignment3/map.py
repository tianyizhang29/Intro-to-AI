import numpy as np
import random

terrian_type = {1:"flat", 2:"hilly", 3:"forested", 4:"caves"}
change = [[-1, 0], [1, 0], [0, -1], [0, 1]]

class Map:
    def __init__(self, width, length):
        self.width = width
        self.length = length
        self.grid, self.belief = self.generate()
        self.target_location = [random.randint(0, self.width - 1), random.randint(0, self.length - 1)]
    
    def generate(self):
        total = self.width * self.length
        grid = np.zeros(total,dtype='int64')
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

    def move_target(self):
        pre_type = self.grid[self.target_location[0]][self.target_location[1]]
        
        dice = random.randint(0,3)
        self.target_location[0] += change[dice][0]
        self.target_location[1] += change[dice][1]

        while self.target_location[0] < 0 or self.target_location[0] > self.width - 1 or \
            self.target_location[1] < 0 or self.target_location[1] > self.length - 1:
            dice = random.randint(0,3)
            self.target_location[0] += change[dice][0]
            self.target_location[1] += change[dice][1]

        next_type = self.grid[self.target_location[0]][self.target_location[1]]
        hint = [pre_type, next_type]
        random.shuffle(hint)
        return hint

    def get_terrian_type(self, x, y):
        return terrian_type[(self.grid[x][y])]
