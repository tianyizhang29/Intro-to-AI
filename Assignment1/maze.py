import random
import time
import numpy as np

# generate 2-d array, 1 means occupied , 0 means empty
def generate_maze(dim, p):
    maze = [[] for p in range(dim)]
    random.seed(time.time())
    for i in range(dim):
        for j in range(dim):
            num = random.random()
            if num <= p:
                maze[i].append(1)
            else:
                maze[i].append(0)
    maze[0][0] = 0
    maze[dim - 1][dim - 1] = 0
    np.save('./maze/%sx%s_%s.npy' % (dim, dim, p), maze)
    return maze

if __name__ == "__main__":
    maze = generate_maze(4, 0.5)
    # maze = np.load('4x4_0.5.npy')
    print(maze)
