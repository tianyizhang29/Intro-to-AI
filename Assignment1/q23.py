from algorithms import aStarED as ased
import matplotlib.pyplot as plt
import maze
import numpy as np

times = 50
dim = 8
step_length = 0.05
p = np.arange(0.2, 0.8, step_length)
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
            continue
        passCount += 1
        repeate_times -= 1
    passRate.append(passCount / times)
passRate = np.array(passRate)
plt.plot(p, passRate)
plt.show()

