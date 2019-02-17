import numpy as np
from algorithms import pathfinding as pf
import maze
import time
import matplotlib.pyplot as plt
"""
ps = np.arange(0, 0.8, 0.01)
dim = 8
iter_times = 10000

path_average_bfs = []
path_average_dfs = []
for p in ps:
    counter = iter_times
    shortest_path_length_dfs = 0
    shortest_path_length_bfs = 0
    count_time = 0
    while counter > 0:
        matrix = maze.generate_maze(dim, p)
        path_bfs = pf.bfs(matrix)
        path_dfs = pf.dfs(matrix)
        if len(path_bfs) != 0:
            shortest_path_length_bfs += len(path_bfs)
            shortest_path_length_dfs += len(path_dfs)
            count_time += 1
        counter -= 1
    if count_time == 0:
        path_average_bfs.append(0)
        path_average_dfs.append(0)
    else:
        path_average_bfs.append(shortest_path_length_bfs / count_time)
        path_average_dfs.append(shortest_path_length_dfs / count_time)
    print(count_time)

path_average_bfs = np.array(path_average_bfs)
path_average_dfs = np.array(path_average_dfs)

np.save('./result/q2/q6/p_' + str(p) + '_' + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + '.npy', ps)
np.save('./result/q2/q6/path_average_bfs' + str(p) + '_' + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + '.npy', path_average_bfs)
np.save('./result/q2/q6/path_average_dfs' + str(p) + '_' + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + '.npy', path_average_dfs)

"""
path_average_bfs = np.load('./result/q2/q6/path_average_bfs0.79_2019-02-16 01:41:16.npy')
path_average_dfs = np.load('./result/q2/q6/path_average_dfs0.79_2019-02-16 01:41:16.npy')
ps = np.load('./result/q2/q6/p_0.79_2019-02-16 01:41:16.npy')


plt.xlabel('Density')
plt.ylabel('Shortest path length of DFS and BFS')
plt.title('Density VS Shortest path length of DFS and BFS')
plt.plot(ps, path_average_bfs, label='BFS')
plt.plot(ps, path_average_dfs, label='DFS')
plt.legend(loc='upper right')
plt.show()