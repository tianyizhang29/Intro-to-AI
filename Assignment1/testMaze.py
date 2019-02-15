import pathfinding as pf
import aStarED as ased
import maze
import time
import matplotlib.pyplot as plt

repeate_times = 50
dim = 3
p = 0.2

# Beacause of the top left and bottom right position are the start point and end point. So the size of 
# maze should larger than 2. The smallest size should be 3. In this experiment, we would like to try 20
# times, setting the repeat time with 20. Test the execution time of DFS algorithm.

# while repeate_times > 0:
#     matrix = maze.generate_maze(dim, p)
#     start = datetime.datetime.now()
#     path = pf.dfs(matrix)
#     print(len(path))
#     end = datetime.datetime.now()
#     t = end - start
#     while len(path) < dim * 2 - 1 or path[len(path) - 1][0] != dim - 1 or path[len(path) - 1][1] != dim - 1:
#         matrix = maze.generate_maze(dim, p)
#         start = datetime.datetime.now()
#         path = pf.dfs(matrix)
#         end = datetime.datetime.now()
#         t = end - start
#     print(str(dim) + ': ' + str(t))
#     repeate_times -= 1
#     dim += 1
dims = []
times = []
while repeate_times > 0:
    matrix = maze.generate_maze(dim, p)
    astar = ased.aStar(matrix)
    start = time.time()
    path = astar.find_path()
    end = time.time()
    t = end - start
    print(str(dim) + '---->' + str(t))
    repeate_times -= 1
    dim += 1
    dims.append(dim)
    times.append(t)
plt.plot(dims, times)
plt.xlabel('dim')
plt.ylabel('time')
plt.show()
# if len(path) < dim * 2 - 1 or path[len(path) - 1][0] != dim - 1 or path[len(path) - 1][1] != dim - 1:
#     print('No valid path')
# else:
#     print(str(dim) + ': ' + str(t))