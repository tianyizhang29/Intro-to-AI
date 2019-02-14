import math
import numpy as np
import copy
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

class aStar():
    # def __init__(self, file):
    #     #read maze file
    #     maze = np.load(file)
    #     self.maze = maze
    #     self.dim = maze.shape[0]
    #     self.open_list = []
    #     self.close_list = []

    def __init__(self, maze):
        #read maze file
        self.maze = maze
        self.dim = len(maze[0])
        self.open_list = []
        self.close_list = []

    def cal_Manhattan(self, x, y):
        distance  = abs(self.dim - x) + abs(self.dim - y)
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
        current_h = self.cal_Manhattan(minF.x + offsetX, minF.y + offsetY)
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
        h = self.cal_Manhattan(0,0)
        startNode = Point(None, 0, 0, h)
        self.open_list.append(startNode)

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
                self.printPath(point)
                break
            elif len(self.open_list) == 0:
                return print('Could Not Find Path!')

    def printPath(self, endPoint):
        path = []
        end = copy.copy(endPoint)
        while True:
            if endPoint.parent:
                path.append(endPoint.parent)
                endPoint = endPoint.parent
            else:
                path = list(list.__reversed__(path))
                break
        for p in path:
            print(p, end="-> ")
        print(end)

if __name__ == "__main__":
    maze = [[0,1,1,1],
            [0,0,1,0],
            [0,0,0,1],
            [1,1,0,0]]
    test = aStar(maze= maze)
    aStar.find_path(test)


