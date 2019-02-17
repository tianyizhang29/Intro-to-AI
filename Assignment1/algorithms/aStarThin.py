import math
import numpy as np
import copy
import aStarMD
import random

class Point():
    # f = g + h
    def __init__(self, parent, x, y, h):
        self.parent = parent
        self.x = x
        self.y = y
        if parent is not None:
            self.g = parent.g + 1
            self.h = h
            self.f = self.g + self.h
        else:
            self.g = 0
            self.h = 0
            self.f = 0


    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __cmp__(self, other):
        return self.f - other.f

    def __str__(self):
        return "(%d, %d)" % (self.x, self.y)

class aStarThin():
    def __init__(self, maze, q):
        #read mazeFile file
        self.maze = maze
        self.simple_maze = copy.deepcopy(maze)
        self.q = q
        self.dim = len(maze[0])
        self.open_list = []
        self.close_list = []
        self.endP = Point(None,self.dim - 1, self.dim - 1, 0)
        self.path = []
        self.max_fringe = 0

    def simplify_maze(self, q):
        obstacle = []
        for i in range(len(self.maze)):
            for j in range(len(self.maze[0])):
                if self.maze[i][j] == 1:
                    obstacle.append([i,j])
        num = len(obstacle) * q
        random.shuffle(obstacle)
        for i in range(num):
            locate = obstacle[i]
            self.simple_maze[locate[0]][locate[1]] = 0
        return

    def heuristic_dis(self, x, y):
        heuristic = aStarMD.aStar(self.simple_maze)
        distance = heuristic.find_path_from_point(x, y)
        return distance

    def in_open_list(self, point):
        for temp in self.open_list:
            if temp.__eq__(point):
                return temp
        return None

    def in_close_list(self, point):
        for temp in self.close_list:
            if temp.__eq__(point):
                return temp
        return None

    def searchNear(self, minF, offsetX, offsetY):
        # check out boundary
        if minF.x + offsetX < 0 or minF.x + offsetX >= self.dim or minF.y + offsetY < 0 or minF.y + offsetY >= self.dim :
            return
        # check barrier; if there is a barrier just jump it
        if self.maze[minF.x + offsetX][minF.y + offsetY] == 1:
            return
        current_h = self.heuristic_dis(minF.x + offsetX, minF.y + offsetY)
        currentPoint  = Point(minF, minF.x + offsetX, minF.y + offsetY, current_h)
        # Check if it's visited before
        if self.in_close_list(currentPoint) is not None:
            return
        else:
            # Update couldVisit set and pq
            existPoint = self.in_open_list(currentPoint)
            if existPoint is not None:
                if existPoint.f > currentPoint.f:
                    existPoint.f = currentPoint.f
                    existPoint.parent = minF
            else:
                self.open_list.append(currentPoint)
                if len(self.open_list) > self.max_fringe:
                    self.max_fringe = len(self.open_list)


    def getMinPoint(self):
        current = self.open_list[0]
        for p in self.open_list:
            if p.f < current.f:
                current = p
        return current

    def endPointInClose(self):
        for p in self.close_list:
            if  p.x == self.dim - 1 and p.y == self.dim - 1:
                return p
        return None

    def find_path(self):
        # create startNode and Add to pq and visited dict
        h = self.heuristic_dis(0,0)
        startNode = Point(None, 0, 0, h)
        self.open_list.append(startNode)
        self.max_fringe = 1

        while True:
            minF = self.getMinPoint()
            self.open_list.remove(minF)
            self.close_list.append(minF)

            self.searchNear(minF, 0, 1) #check right
            self.searchNear(minF, 0, -1) #check left
            self.searchNear(minF, 1, 0) #check down
            self.searchNear(minF, -1, 0) #check top

            point = self.endPointInClose()
            if point:
                # self.print_Path(point)
                self.endP = point
                end = copy.copy(self.endP)
                while True:
                    if self.endP.parent:
                        self.path.append(self.endP.parent)
                        self.endP = self.endP.parent
                    else:
                        self.path = list(list.__reversed__(self.path))
                        break
                self.path.append(end)
                return [len(self.path), len(self.open_list) + len(self.close_list), self.max_fringe]
            elif len(self.open_list) == 0:
                return [0, len(self.open_list) + len(self.close_list), self.max_fringe]

    def print_Path(self):
        for i in range(len(self.path) - 1):
            print(self.path[i], end="-> ")
        print(self.path[len(self.path) - 1])


if __name__ == "__main__":
    maze = [[0,1,1,1],
            [0,0,1,0],
            [0,0,0,1],
            [1,1,0,0]]
    test = aStarThin(maze, 0.5)
    print(test.find_path())
    test.print_Path()

