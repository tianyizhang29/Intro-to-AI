import numpy as np
import random

class cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class minSweeper:
    # reveal[][] num represents visited; "*" mark as mine; "W" is mine with wrong detection;
    def __init__(self, file):
        self.grid = np.load(file)
        self.d = len(self.grid)
        self.n = 15
        self.reveal = [["N" * self.d] in range(self.d)]
        self.to_be_revealed = []
        self.num_mine = 0
        self.dx = [-1, 0, 1]
        self.dy = [-1, 0, 1]


    # 找一定是雷的点，标记
    # 不是8个点。
    def find_mine(self, cell):
        cur_x = cell.x
        cur_y = cell.y
        neighbour_hint = []
        for i in range(3):
            for j in range(3):
                new_x = cur_x + self.dx[i]
                new_y = cur_y + self.dy[j]
                if self.reveal[new_x][new_y] == "N" or self.reveal[new_x][new_y] == "*" or self.reveal[new_x][new_y] == "W":
                    continue
                else:
                    neighbour_hint.append(cell(new_x, new_y))



        # bug -> 多个位置可以判定是雷或者空
        while len(neighbour_hint) != 0:
            cur_cell = neighbour_hint.pop(0)
            last_pos = 9
            mine = self.grid[cur_cell.x][cur_cell.y]
            for i in range(3):
                for j in range(3):
                    x = cur_cell.x + self.dx[i]
                    y = cur_cell.y + self.dy[j]
                    if self.reveal[x][y] == "N":
                        continue
                    elif self.reveal[x][y] == "*" or self.reveal[x][y] == "W":
                        mine = mine - 1
                        last_pos -= 1
                    else:
                        last_pos = last_pos - 1
                    # 一定是雷
                    if last_pos == mine:
                        return 1
                    # 一定不是雷
                    elif mine == 0:
                        return 2
            return 0

    # 当没有能够推论出一定是雷的点的时候，找是雷可能性最小的点。
    def find_reachable_position(self):
        min_prob = 8
        res_index = -1
        for i in range(len(self.to_be_revealed)):
            prob = self.cal_possibility(self.to_be_revealed[.__getitem__(i)])
            if prob < min_prob:
                min_prob = prob
                res_index = i
        return res_index

    # 计算每个cell是雷的可能性（计算方法待定）。
    def cal_possibility(self, cell):
        res = 0.0
        for i in range(3):
            for j in range(3):
                new_x = cell.x + self.dx[i]
                new_y = cell.y + self.dy[j]
                if new_x >=0 and new_x < self.d and new_y >= 0 and new_y < self.d: # Validate
                    if self.reveal[new_x][new_y] != "N" and self.reveal[new_x][new_y] != "*" and self.reveal[new_x][new_y] != "W":
                        last_pos = 9
                        mine = self.grid[new_x][new_y]
                        for i in range(3):
                            for j in range(3):
                                x = new_x + self.dx[i]
                                y = new_y + self.dy[j]
                                # 此处需要验证坐标有效性
                                if new_x >=0 and new_x < self.d and new_y >= 0 and new_y < self.d:
                                    if self.reveal[x][y] == "N":
                                        continue
                                    elif self.reveal[x][y] == "*" or self.reveal[new_x][new_y] == "W":
                                        mine -= - 1
                                        last_pos -= 1
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
                    if self.grid[new_x][new_y] == "N":
                        self.to_be_revealed.__add__(cell(new_x, new_y))

    def check_finished(self):
        for i in self.reveal:
            if i == "N":
                return False
        return True

    # start_game
    def game(self):
        # find a start point to start;
        x = random.randint(0, self.d)
        y = random.randint(0, self.d)
        num = self.grid[x][y]
        if (num == -1):
            print("boom!")
            return
        else:
            self.reveal[x][y] = str(num)
            self.check_neighbour(x, y)
        while True:
            find_mark = False
            for i in range(len(self.to_be_revealed)):
                cur_cell = self.to_be_revealed.__getitem__(i)
                # 这个点一定是雷, Mark, 更新to_be_revealed。Break;
                if self.find_mine(cur_cell) == 1:
                    self.num_mine +=1
                    self.reveal[cur_cell.x][cur_cell.y] = "*"
                    self.check_neighbour(cur_cell.x, cur_cell.y)
                    self.to_be_revealed.pop(i)
                    find_mark = True
                    break
                # 一定不是雷
                elif self.find_mine(cur_cell) == 2:
                    self.reveal[cur_cell.x][cur_cell.y] = self.grid[cur_cell.x][cur_cell.y]
                    self.to_be_revealed.pop(i)
                    self.check_neighbour(cur_cell.x, cur_cell.y)
                    break
            if find_mark:
                continue
            # 已经标记了所有是雷的情况：
            else:
                next_position = self.find_reachable_position()
                next_cell = self.to_be_revealed.__getitem__(next_position)
                self.to_be_revealed.pop(next_position)
                if self.grid[next_cell.x][next_cell.y] == "-1":
                    self.reveal[next_cell.x][next_cell.y] = "W"
                else:
                    self.reveal[next_cell.x][next_cell.y] = self.grid[next_cell.x][next_cell.y]
                    self.to_be_revealed.append(cell(next_cell))
            if self.check_finished():
                print("---------------Finished-------------------")
                print("correct rate: %s" % (self.num_mine / 15.0))



if __name__ == '__main__':
    test = minSweeper("10_15.npy")
    test.game()