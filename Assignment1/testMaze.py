from algorithms import aStarED as ased
import maze
import time
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

times = 10000

dims = np.arange(45, 53, 1)
p = np.arange(0.3, 0.6, 0.1)
passRate = []
for i in dims:
    for j in p:
        repeate_times = times
        passCount = 0
        print('dims: ' + str(i))
        print('p: ' + str(j))
        while repeate_times > 0:
            matrix = maze.generate_maze(i, j)
            astar = ased.aStar(matrix)
            hasPath = astar.find_path()
            if hasPath:
                passCount += 1
            repeate_times -= 1
        passRate.append(passCount / times)

# plot the 3D figure
passRate = np.array(passRate)
passRate = np.reshape(passRate, (len(p), len(dims)))
dims, p = np.meshgrid(dims, p)
fig = plt.figure()
ax = Axes3D(fig)
ax.plot_surface(dims, p, passRate, rstride=1, cstride=1, cmap='rainbow')
plt.show()
# Beacause of the top left and bottom right position are the start point and end point. So the size of 
# maze should larger than 2. The smallest size should be 3. In this experiment, we would like to try 20
# times, setting the repeat time with 20. Test the execution time of DFS algorithm.