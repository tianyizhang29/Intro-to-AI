from algorithms import aStarED as ased
import matplotlib.pyplot as plt
import maze
import numpy as np
import time

times = 10000
dim = 8
step_length = 0.01
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

np.save('./result/q2/q3/p_' + time.strftime('%Y-%m-%d %H-%M-%S',time.localtime(time.time())) + '.npy', p)
np.save('./result/q2/q3/passRate_' + time.strftime('%Y-%m-%d %H-%M-%S',time.localtime(time.time())) + '.npy', passRate)

plt.xlabel('density')
plt.ylabel('solvability')
plt.title('density VS solvability')
plt.plot(p, passRate)
plt.show()

