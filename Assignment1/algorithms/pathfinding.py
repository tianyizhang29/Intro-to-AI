import numpy as np
import sys
sys.path.append("..")
import maze
dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]

maxRecursiveDepth = 0

"""The recursive function of DFS"""
def recur(maze, isVisited, i, j, path, result, recurDepth):
	global maxRecursiveDepth
	recurDepth += 1
	maxRecursiveDepth = recurDepth if recurDepth > maxRecursiveDepth else maxRecursiveDepth
	# Return the function if the parameters are illegal.
	if i < 0 or i >= len(maze) or j < 0 or j >= len(maze[0]) or isVisited[i][j] == 1 or maze[i][j] == 1:
		return;

	# If the position is the goal, end the function.
	if i == len(maze) - 1 and j == len(maze[0]) - 1:
		path.append([i, j])
		for p in path:
			result.append(p)
		return True
	# Add the postion in to path.
	path.append([i, j])
	isVisited[i][j] = 1

	# Continue recurve the DFS.
	for round in range(4):
		newI = i + dx[round]
		newJ = j + dy[round]
		isReach = recur(maze, isVisited, newI, newJ, path, result, recurDepth)
		if isReach:
			return True

	path.pop(len(path) - 1)

"""The DFS algorithm."""
def dfs_find_path(maze):
	# Create a matrix which label the visited point in mazeFile.
	isVisited = np.zeros((len(maze), len(maze[0])))

	# Create the path and execute the recursize process.
	path = []
	result = []
	recurDepth = 0
	recur(maze, isVisited, 0, 0, path, result, recurDepth)
	expandPoints = 0
	for i in isVisited:
		for j in i:
			if j == 1:
				expandPoints += 1
	return [result, expandPoints, maxRecursiveDepth]

def dfs(maze):
	result = dfs_find_path(maze)
	return [len(result[0]), result[1], result[2]]

"""The BFS algorithm"""
def bfs_find_path(maze):
	path = []
	isVisited = np.zeros((len(maze), len(maze[0])))
	queue = [[0, 0]]
	dict = {}
	maxQueueSize = 0
	while len(queue) > 0:
		size = len(queue)
		maxQueueSize = size if size > maxQueueSize else maxQueueSize
		for i in range(size):
			pos = queue.pop(0)
			for round in range(4):
				newI = pos[0] + dx[round]
				newJ = pos[1] + dy[round]
				if newI == len(maze) - 1 and newJ == len(maze[0]) - 1 and maze[newI][newJ] == 0:
					dict[newI * len(maze[0]) + newJ] = pos[0] * len(maze[0]) + pos[1]
					curPos = len(maze) * len(maze[0]) - 1
					while curPos != 0:
						path.append([curPos // len(maze[0]), curPos % len(maze[0])])
						curPos = dict[curPos];
					path.append([0,0])
					path.reverse()
					expandPoints = 0
					for i in isVisited:
						for j in i:
							if j == 1:
								expandPoints += 1
					return [path, expandPoints, maxQueueSize]
				if(newI >= 0 and newI < len(maze) and newJ >= 0 and newJ < len(maze) and maze[newI][newJ] == 0 and isVisited[newI][newJ] == 0):
					dict[newI * len(maze[0]) + newJ] = pos[0] * len(maze[0]) + pos[1]
					queue.append([newI, newJ])
					isVisited[newI][newJ] = 1
	expandPoints = 0
	for i in isVisited:
		for j in i:
			if j == 1:
				expandPoints += 1
	return [path, expandPoints, maxQueueSize]

def bfs(maze):
	result = bfs_find_path(maze)
	return [len(result[0]), result[1], result[2]]

if __name__ == "__main__":
	# mazeFile = np.load('./mazeFile/4x4_0.5.npy')
	# for i in range(len(mazeFile)):
	# 	print(mazeFile[i])
	matrix = maze.generate_maze(8, 0.2)
	print(dfs(matrix))