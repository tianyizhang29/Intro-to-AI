import numpy as np

dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]

"""The recursive function of DFS"""
def recur(maze, isVisited, i, j, path, result):
	# Return the function if the parameters are illegal.
	if i < 0 or i >= len(maze) or j < 0 or j >= len(maze[0]) or isVisited[i][j] == 1 or maze[i][j] == 1:
		return;

	# If the position is the goal, end the function.
	if i == len(maze) - 1 and j == len(maze[0]) - 1:
		path.append([i, j])
		for p in path:
			result.append(p)
		# print(result)
		return ;
	# Add the postion in to path.
	path.append([i, j])
	isVisited[i][j] = 1

	# Continue recurve the DFS.
	for round in range(4):
		newI = i + dx[round]
		newJ = j + dy[round]
		recur(maze, isVisited, newI, newJ, path, result)

	isVisited[i][j] = 0
	path.pop(len(path) - 1)

"""The DFS algorithm."""
def dfs(maze):
	# Create a matrix which label the visited point in maze.
	isVisited = np.zeros((len(maze), len(maze[0])))

	# Create the path and execute the recursize process.
	path = []
	result = []
	recur(maze, isVisited, 0, 0, path, result)

	return result

"""The BFS algorithm"""
def bfs(maze):
	isVisited = np.zeros((len(maze), len(maze[0])))
	queue = [[0, 0]]
	while len(queue) > 0:
		size = len(queue)
		for i in range(size):
			pos = queue.pop(0)
			for round in range(4):
				newI = pos[0] + dx[round]
				newJ = pos[1] + dy[round]
				if newI == len(maze) - 1 and newJ == len(maze[0]) - 1:
					return True
				if(newI >= 0 and newI < len(maze) and newJ >= 0 and newJ < len(maze) and maze[newI][newJ] == 0 and isVisited[newI][newJ] == 0):
					queue.append([newI, newJ])
					maze[newI][newJ] = 1
	
	return False

if __name__ == "__main__":
	maze = [[0,0,0,0],
			[0,1,1,0],
			[0,0,0,1],
			[0,1,0,0]]
	print(dfs(maze))


