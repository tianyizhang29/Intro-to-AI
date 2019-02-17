import maze
import copy
import random
import pathfinding as pf
import aStarED
import aStarMD

init_dim = 4
init_p = 0.3
init_maze = maze.generate_maze(init_dim, init_p)
dx = [-1,0,1]
dy = [-1,0,1]

def hill_climbing(maze, method):
    # choose a random point for starting running hill_climbing algorithm
    x = random.randint(0, init_dim)
    y = random.randint(0, init_dim)
    # evaluate 8 neighbour point for hill_climbing
    complex = evaluate(maze, method)
    while True:
        prev_x = copy.deepcopy(x)
        prev_y = copy.deepcopy(y)

        for i in range(3):
            for j in range(3):
                if (dx[i] != 0 and dy[j] != 0):
                    new_x = x + dx[i]
                    new_y = y + dy[j]
                else:
                    continue
                cur_maze = copy.deepcopy(maze)
                if new_x < 0 or new_x >= init_dim or new_y < 0 or new_y >= init_dim:
                    continue
                else:
                    if cur_maze[new_x][new_y] == 0:
                        cur_maze[new_x][new_y] = 1
                    else:
                        cur_maze[new_x][new_y] = 0
                    cur_complex = evaluate(cur_maze, method)
                    if cur_complex > complex:
                        x = new_x
                        y = new_y
                        maze = cur_maze
                        complex = cur_complex
                        print('updated x:' + str(x) + '   y:' + str(y))
        if prev_x == x and prev_y == y:
            print('Found most complex maze!')
            break
    return maze


def evaluate(maze, method):
    complex = 0
    ed = aStarED.aStar(maze= maze)
    md = aStarMD.aStar(maze= maze)

    if (method == 'dfs'):
        complex = pf.bfs(maze)
    elif (method == 'dfs'):
        complex = pf.dfs(maze)
    elif (method == 'aStarED'):
        complex = ed.find_path()
    elif (method == 'aStarMD'):
        complex = md.find_path()
    complex = sum(complex)
    return complex

if __name__ == '__main__':
    maze = [[0,1,1,1],
            [0,0,1,0],
            [0,0,0,1],
            [1,1,0,0]]

    print(hill_climbing(maze, 'aStarED'))
