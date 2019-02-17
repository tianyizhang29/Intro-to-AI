import maze
from algorithms import pathfinding as pf
from algorithms import aStarED as aS
import numpy as np

if __name__ == "__main__":

    matrix = np.load('./result/q2/q2/p_8x8_0.2.npy')
    for i in matrix:
        print(i)
    pathDFS = pf.dfs(matrix)
    pathBFS = pf.bfs(matrix)
    aStarObj = aS.aStar(matrix)
    print("************************")
    print("DFS:")
    print(pathDFS)
    print("************************")
    print("BFS:")
    print(pathBFS)
    print("************************")
    print("AStar:")
    pathAS = aStarObj.find_path()
    print("************************")

    """ Generate a solvable maze
    flag = False
    while not flag:
        matrix = maze.generate_maze(8, 0.2)
        path = pf.bfs(matrix)
        if len(path) != 0:
            flag = True
    
    np.save('./result/q2/q2/p_8x8_0.2.npy', matrix)
    print(matrix)
    """
