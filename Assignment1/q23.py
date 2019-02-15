from algorithms import aStarED as ased
import matplotlib.pyplot as plt
import maze
import numpy as np

times = 100
dim = 8
step_length = 0.02
p = np.arange(0.1, 0.9, step_length)
passRate = []
for j in p:
    repeate_times = times
    passCount = 0
    print('p: ' + str(j))
    while repeate_times > 0:
        matrix = maze.generate_maze(dim, j)
        astar = ased.aStar(matrix)
        hasPath = astar.find_path()
        if not hasPath:
            repeate_times -= 1
            continue
        passCount += 1
        repeate_times -= 1
    passRate.append(passCount / times)
passRate = np.array(passRate)
# passRate = np.load("./result/1bfs.npy")
plt.plot(p, passRate)
plt.show()

