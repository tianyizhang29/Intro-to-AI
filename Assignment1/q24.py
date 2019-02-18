import numpy as np
from algorithms import pathfinding as pf
import maze
import time
import matplotlib.pyplot as plt

ps = np.arange(0, 0.51, 0.01)
dim = 8
iter_times = 10000

path_average = []
for p in ps:
    counter = iter_times
    shortest_path_length = 0
    count_time = 0
    while counter > 0:
        matrix = maze.generate_maze(dim, p)
        path = pf.bfs(matrix)
        if len(path) != 0:
            shortest_path_length += len(path)
            count_time += 1
        counter -= 1
    path_average.append(shortest_path_length / count_time)
    print(count_time)

path_average = np.array(path_average)


np.save('./result/q2/q4/p_' + str(dim) + '_' + str(p) + '_' + time.strftime('%Y-%m-%d %H-%M-%S',time.localtime(time.time())) + '.npy', ps)
np.save('./result/q2/q4/path_average_' + str(dim) + '_' + str(p) + '_' + time.strftime('%Y-%m-%d %H-%M-%S',time.localtime(time.time())) + '.npy', path_average)

"""
path_average = np.load('./result/q2/q4/path_average_8_0.49_2019-02-15 23-44-35.npy')
ps = np.load('./result/q2/q4/p_8_0.49_2019-02-15 23-44-35.npy')
"""
plt.xlabel('Density')
plt.ylabel('Expected shortest path length')
plt.title('Density VS Expected shortest path length')
plt.plot(ps, path_average)
plt.show()