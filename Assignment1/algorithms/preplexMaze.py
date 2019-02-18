import maze
import copy
import random
import pathfinding as pf
import aStarED
import aStarMD

init_dim = 8
init_p = 0.5
init_maze = maze.generate_maze(init_dim, init_p)
dx = [-1,0,1]
dy = [-1,0,1]

def hill_climbing(maze, method, param):
    #repeate n times
    for i in range(10):
        # choose a random point for starting running hill_climbing algorithm
        x = random.randint(0, init_dim - 1)
        y = random.randint(0, init_dim - 1)
        maze[x][y] = 1 if maze[x][y] == 0 else 0
        complex = evaluate(maze, method, param)
        while True:
            prev_x = copy.deepcopy(x)
            prev_y = copy.deepcopy(y)

            # evaluate 8 neighbour point for hill_climbing
            for i in range(3):
                for j in range(3):
                    if (dx[i] != 0 and dy[j] != 0):
                        new_x = x + dx[i]
                        new_y = y + dy[j]
                    else:
                        continue
                    cur_maze = copy.deepcopy(maze)
                    # over bound; continue
                    if new_x < 0 or new_x >= init_dim or new_y < 0 or new_y >= init_dim:
                        continue
                    else:
                        # update current cell to be empty or occupied
                        if cur_maze[new_x][new_y] == 0:
                            cur_maze[new_x][new_y] = 1
                        else:
                            cur_maze[new_x][new_y] = 0
                        cur_complex = evaluate(cur_maze, method, param)
                        # record the 'hardest' maze in 8 neighbours
                        if cur_complex > complex:
                            x = new_x
                            y = new_y
                            maze = cur_maze
                            complex = cur_complex
                            print('updated x:' + str(x) + '   y:' + str(y))
            if prev_x == x and prev_y == y:
                break
    print('Found most complex maze!')
    return maze


def evaluate(maze, method, param):
    complex = 0
    ed = aStarED.aStar(maze= maze)
    md = aStarMD.aStar(maze= maze)

    if (method == 'bfs'):
        complex = sum(pf.bfs(maze))
    elif (method == 'dfs'):
        if (param == 'MSP'):
            complex = pf.dfs(maze)[0]
        elif (param == 'MFS'):
            complex = pf.dfs(maze)[1]
    elif (method == 'aStarED'):
        complex = sum(ed.find_path())
    elif (method == 'aStarMD'):
        if (param == 'MNE'):
            complex = md.find_path()[1]
        elif (param == 'MFS'):
            complex = md.find_path()[2]
    return complex

if __name__ == '__main__':
    maze = [[0,1,1,1],
            [0,0,1,0],
            [0,0,0,1],
            [1,1,0,0]]

    print(hill_climbing(init_maze, 'aStarMD', 'MFS'))
