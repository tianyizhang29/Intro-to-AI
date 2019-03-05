import matplotlib.pyplot as pl
import environment as ev
import numpy as np
import random
import drawGrid

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class minSweeper:
    # reveal[][] num represents visited; "*" mark as mine; "W" is mine with wrong detection;
    def __init__(self, map, total_mine):
        self.grid = map
        self.d = len(self.grid)
        self.visited = np.reshape(np.zeros(self.d * self.d), (self.d, self.d))
        self.reveal = [(["N"] * self.d).copy() for i in range(self.d)]
        self.to_be_revealed = []
        self.num_mine = 0
        self.dx = [-1, 0, 1]
        self.dy = [-1, 0, 1]
        # self.total_mine = int(file.split('_')[1][0: -4])
        self.total_mine = total_mine

# 找一定是雷的点，标记
    def find_mine(self, cell):
        cur_x = cell.x
        cur_y = cell.y
        neighbour_hint = []
        for i in range(3):
            for j in range(3):
                new_x = cur_x + self.dx[i]
                new_y = cur_y + self.dy[j]
                if new_x >=0 and new_x < self.d and new_y >= 0 and new_y < self.d:
                    if self.reveal[new_x][new_y].__eq__("N") or self.reveal[new_x][new_y] .__eq__("*") or self.reveal[new_x][new_y].__eq__("W") :
                        continue
                    else:
                        neighbour_hint.append(Cell(new_x, new_y))

        while len(neighbour_hint) != 0:
            hint_cell = neighbour_hint.pop(0)
            last_pos = 9
            mine = self.grid[hint_cell.x][hint_cell.y]
            for i in range(3):
                for j in range(3):
                    x = hint_cell.x + self.dx[i]
                    y = hint_cell.y + self.dy[j]
                    if x >=0 and x < self.d and y >= 0 and y < self.d:
                        if last_pos != mine:
                            if self.reveal[x][y] == "N":
                                continue
                            elif self.reveal[x][y] == "*" or self.reveal[x][y] == "W":
                                mine = mine - 1
                                last_pos -= 1
                            else:
                                last_pos = last_pos - 1
                        # 一定是雷
                        if last_pos == mine:
                            # print("")
                            # print("Found (%s, %s) is mine..." % (cell.x, cell.y))
                            # print("")
                            return 1
                        # 一定不是雷
                        elif mine == 0 and last_pos != 0:
                            # print("")
                            # print("Found (%s, %s) is safe..." % (cell.x, cell.y))
                            # print("")
                            return 2
                    else:
                        last_pos -= 1
        #print("(%s, %s) unsure!!!!" % (cell.x, cell.y))
        return 0

    # 当没有能够推论出一定是雷的点的时候，找是雷可能性最小的点。
    def find_reachable_position(self):
        min_prob = 8
        res_index = -1
        for i in range(len(self.to_be_revealed)):
            cur_cell = self.to_be_revealed.__getitem__(i)
            prob = self.cal_possibility(cur_cell)
            if prob < min_prob:
                min_prob = prob
                res_index = i
        # self.to_be_revealed.pop(res_index)
        return res_index

    # 计算每个cell是雷的可能性（计算方法待定）。
    def cal_possibility(self, cell):
        res = 0.0
        for i in range(3):
            for j in range(3):
                new_x = cell.x + self.dx[i]
                new_y = cell.y + self.dy[j]
                if new_x >=0 and new_x < self.d and new_y >= 0 and new_y < self.d:
                    # Find number
                    if not self.reveal[new_x][new_y].__eq__("N") and not self.reveal[new_x][new_y].__eq__('*'):
                        last_pos = 9
                        mine = self.grid[new_x][new_y]
                        for m in range(3):
                            for n in range(3):
                                x = new_x + self.dx[m]
                                y = new_y + self.dy[n]
                                if x >= 0 and x < self.d and y >= 0 and y < self.d:
                                    if self.reveal[x][y].__eq__("N") :
                                        continue
                                    elif self.reveal[x][y].__eq__('*') or self.reveal[x][y].__eq__("W"):
                                        mine = mine - 1
                                        last_pos -= 1
                                    else:
                                        last_pos = last_pos - 1
                                else:
                                    last_pos -= 1
                        res += mine / last_pos
        return res

    # 计算这个点是雷的最大可能性
    def maxPossibility(self, cell):
        return float

    # 检查是否找到了所有的雷
    def check_status(self):
        return bool

    # 检查周围的8个点是否可以加入
    def check_neighbour(self, x, y):
        for i in range(3):
            for j in range(3):
                new_x = x + self.dx[i]
                new_y = y + self.dy[j]
                if new_x >= 0 and new_x < self.d and new_y >= 0 and new_y < self.d:
                    if self.reveal[new_x][new_y].__eq__("N") and  self.visited[new_x][new_y] == 0:
                        self.to_be_revealed.append(Cell(new_x, new_y))
                        self.visited[new_x][new_y] = 1

    def check_finished(self):
        for i in self.reveal.__iter__():
            for item in i.__iter__():
                if item == "N":
                    return False
        return True

    def print_reveal(self):
        for i in range(self.d):
            for j in range(self.d):
                print(self.reveal[i][j], end='  ')
            print('')
        # matrix = np.asarray(self.reveal)
        # drawGrid.drawGrid(matrix)
        print('----------------------------------------')

    # start_game
    def game(self):
        while True:
            # find a start point to start;
            x = random.randint(0, self.d - 1)
            y = random.randint(0, self.d - 1)
            # x = 3
            # y = 8
            num = self.grid[x][y]
            if (num == -1):
                continue
            else:
                self.reveal[x][y] = num
                self.visited[x][y] = 2
                self.check_neighbour(x, y)
            print("Starting point at (%s, %s)" % (x, y))
            while True:
                self.print_reveal()
                find_mark = False
                for i in range(len(self.to_be_revealed)):
                    cur_cell = self.to_be_revealed.__getitem__(i)
                    # 这个点一定是雷, Mark, 更新to_be_revealed。Break;
                    check_res = self.find_mine(cur_cell)
                    if check_res == 1:
                        self.num_mine +=1
                        self.reveal[cur_cell.x][cur_cell.y] = "*"
                        self.visited[cur_cell.x][cur_cell.y] = 2
                        self.check_neighbour(cur_cell.x, cur_cell.y)
                        self.to_be_revealed.pop(i)
                        find_mark = True
                        break
                    # 一定不是雷
                    elif check_res == 2:
                        self.reveal[cur_cell.x][cur_cell.y] = self.grid[cur_cell.x][cur_cell.y]
                        self.visited[cur_cell.x][cur_cell.y] = 2
                        self.to_be_revealed.pop(i)
                        self.check_neighbour(cur_cell.x, cur_cell.y)
                        find_mark = True
                        break
                if find_mark:
                    continue
                # 已经标记了所有是雷的情况：
                else:
                    next_index = self.find_reachable_position()
                    if next_index != -1:
                        next_cell = self.to_be_revealed.__getitem__(next_index)
                        # print("")
                        # print("Into Guess Part; Guess(%s, %s) as next cell" % (next_cell.x, next_cell.y))
                        # print("")
                        self.to_be_revealed.pop(next_index)
                        self.visited[next_cell.x][next_cell.y] = 2
                        if self.grid[next_cell.x][next_cell.y] == -1:
                            self.reveal[next_cell.x][next_cell.y] = "W"
                        else:
                            self.reveal[next_cell.x][next_cell.y] = self.grid[next_cell.x][next_cell.y]
                            self.check_neighbour(next_cell.x, next_cell.y)
                if self.check_finished():
                    print('')
                    print('')
                    print("---------------Finished-------------------")
                    print("correct rate: %s" % (self.num_mine / self.total_mine))
                    return self.num_mine / self.total_mine
        matrix = np.asarray(self.reveal)
        drawGrid.drawGrid(matrix)

if __name__ == '__main__':
    # d = 20
    # rate = np.arange(0, 0.38, 0.02)
    # result = []
    # for r in rate:
    #     print(r)
    #     n = d * d * r
    #     map = ev.initial_environment(d,int(n))
    #     test = minSweeper(map, n)
    #     res = test.game()
    #     result.append(res)

    # pl.plot(rate, result)
    # pl.title("Mine density vs Final score")
    # pl.xlabel("Mine density")
    # pl.xlabel("Final score")
    # pl.axis([0, rate[(len(rate) - 1)], 0, 1.2])
    # pl.show()
    d = 20
    rate = 0.15
    n = d * d * rate
    map = ev.initial_environment(d,int(n))
    test = minSweeper(map, n)
    res = test.game()
    matrix = np.asarray(test.reveal)
    drawGrid.drawGrid(matrix)