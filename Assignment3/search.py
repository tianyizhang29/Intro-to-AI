import map
import numpy as np
import random
import matplotlib.pyplot as plt
import sys

sys.setrecursionlimit(3000)
change = [[-1, 0], [1, 0], [0, -1], [0, 1]]
terrian_type = {1:"flat", 2:"hilly", 3:"forested", 4:"caves"}

class Solution:
    def __init__(self, terrian):
        self.terrian = terrian
        self.width = terrian.width
        self.length = terrian.length
        self.belief = terrian.belief
        self.tgt_pos = terrian.target_location
        self.can_not_found = {"flat":0.1, "hilly":0.3, "forested":0.5, "caves":0.9}

    def update_belief(self, not_found_pos, pos):
        # print(pos)
        # position of cell need to be update
        xi = pos[0]
        yi = pos[1]
        # position of cell not found target
        xj = not_found_pos[0]
        yj = not_found_pos[1]

        poss_cannot_fd_j = 1 - self.can_not_found[self.terrian.get_terrian_type(xj, yj)]

        poss_t_in_pos_before = self.belief[xi][yi]
        poss_not_fd = (1 - self.belief[xj][yj]) + self.belief[xj][yj] * poss_cannot_fd_j

        self.belief[xi][yi] = poss_t_in_pos_before / poss_not_fd
    
    def search_1(self):
        x, y = random.randint(0, self.width - 1), random.randint(0, self.length - 1)
        count = 0

        while(True):
            count += 1
            max_poss = 0
            max_i = 0
            max_j = 0
            if [x, y] == self.tgt_pos:
                terrian_type = self.terrian.get_terrian_type(x, y)
                cannot_found_poss = self.can_not_found[terrian_type]
                dice = random.random()
                # target exists in (x,y), but cannot found.
                if dice < cannot_found_poss:
                    for i in range(self.width):
                        for j in range(self.length):
                            self.update_belief((x, y), (i, j))
                            if self.belief[i][j] > max_poss:
                                max_poss = self.belief[i][j]
                                max_i = i
                                max_j = j
                # target exists in (x,y), and found it
                else:
                    return count
            else:
                self.belief[x][y] = 0
                # target is not in this position, update belief matrix.
                for i in range(self.width):
                    for j in range(self.length):
                        self.update_belief((x, y), (i, j))
                        if self.belief[i][j] > max_poss:
                            max_poss = self.belief[i][j]
                            max_i = i
                            max_j = j
            
            # found the postion with max probability of contains target.
            x = max_i
            y = max_j
    
    def search_2(self):
        x, y = random.randint(0, self.width - 1), random.randint(0, self.length - 1)
        count = 0

        while(True):
            count += 1
            max_poss = 0
            max_i = 0
            max_j = 0
            terrian_type = self.terrian.get_terrian_type(x, y)
            cannot_found_poss = self.can_not_found[terrian_type]
            if [x, y] == self.tgt_pos:
                dice = random.random()
                # target exists in (x,y), but cannot found.
                if dice < cannot_found_poss:
                    for i in range(self.width):
                        for j in range(self.length):
                            self.update_belief((x, y), (i, j))
                            if self.belief[i][j] * (1 - cannot_found_poss) > max_poss:
                                max_poss = self.belief[i][j] * cannot_found_poss
                                max_i = i
                                max_j = j
                # target exists in (x,y), and found it
                else:
                    return count
            else:
                self.belief[x][y] = 0
                # target is not in this position, update belief matrix.
                for i in range(self.width):
                    for j in range(self.length):
                        self.update_belief((x, y), (i, j))
                        if self.belief[i][j] * (1 - cannot_found_poss) > max_poss:
                            max_poss = self.belief[i][j] * cannot_found_poss
                            max_i = i
                            max_j = j
            
            # found the postion with max probability of contains target.
            x = max_i
            y = max_j

    def search_adj(self, rule):
        x, y = random.randint(0, self.width - 1), random.randint(0, self.length - 1)
        count = [0]

        self.dfs(x, y, count, rule)
        return count[0]

    def dfs(self, x, y, count, rule):
        """
        x, y is the current postion.
        count is the array for counting the visited positions.
        type representitives Rule 1(0) or Rule 2(1).
        """
        # print("$$ {}".format(count[0]))
        count[0] += 1
        terrain_type = self.terrian.get_terrian_type(x, y)
        cannot_found_poss = self.can_not_found[terrain_type]
        dice = random.random()
        if [x, y] == self.tgt_pos and dice >= cannot_found_poss:
            return 
        else:
            if [x, y] != self.tgt_pos:
                self.belief[x][y] = 0
            for i in range(self.width):
                for j in range(self.length):
                    self.update_belief((x, y), (i, j))
            max_i = 0
            max_j = 0
            adjacent = []
            for chg in change:
                new_x = chg[0] + x
                new_y = chg[1] + y
                if new_x > 0 and new_x < self.width and new_y > 0 and new_y < self.length and self.belief[new_x][new_y] > 0:
                    adjacent.append(((new_x, new_y), self.belief[new_x][new_y] * (1 - (1 - cannot_found_poss) * float(rule))))
                    adjacent.sort(key=takeSecond, reverse=True)
            # print("adjacent length: {}".format(len(adjacent)))
            for adj in adjacent:
                    max_i = adj[0][0]
                    max_j = adj[0][1]
                    self.dfs(max_i, max_j, count, rule)
        
    def move_target_search(self):
        x, y = random.randint(0, self.width - 1), random.randint(0, self.length - 1)
        count = 0

        while True:
            count += 1
            terrian_type = self.terrian.get_terrian_type(x, y)
            cannot_found_poss = self.can_not_found[terrian_type]
            if [x, y] == self.tgt_pos:
                dice = random.random()
                if dice > cannot_found_poss:
                    pass
                    # TODO
                else:
                    return count
            else:
                hint = self.terrian.move_target()
                hint_type1 = terrian_type[hint[0]]
                hint_type2 = terrian_type[hint[1]]

    def get_same_cell(self, terr_type):
        tpye_idx = terrian_type[terr_type]
        queue = []
        for i in range(self.width):
            for j in range(self.length):
                if self.terrian.grid[i][j] == tpye_idx:
                    queue.append([i, j])
        return queue

    def get_adjacent_same_cell(self, curr_queue, terr_type):
        adjacnet_queue = []
        for c in curr_queue:
            for chg in change:
                new_i = c[0] + chg[0]
                new_j = c[1] + chg[1]
                if new_i >= 0 and new_i < self.width and new_j >= 0 and new_j < self.length:
                    if self.terrian.grid[new_i][new_j] == terr_type and not [new_i, new_j] in adjacnet_queue:
                        adjacnet_queue.append([new_i, new_j])
        return adjacnet_queue
        
def takeSecond(elem):
    return elem[1]

def main():
    sum1 = []
    sum2 = []
    for i in range(20):
        terrian = map.Map(50,50)
        solution = Solution(terrian)
        count1 = solution.search_1()
        sum1.append(count1)
        print("Count under rule 1: {}".format(count1))

        terrian.belief = np.full((50, 50), 1 / 2500)
        solution = Solution(terrian)
        count2 = solution.search_2()
        sum2.append(count2)
        print("Count under rule 2: {}".format(count2))
    
    np.save('./res/q3.npy', (sum1, sum2))

def main1():
    sum1 = []
    sum2 = []
    for i in range(20):
        terrian = map.Map(50,50)
        solution = Solution(terrian)
        count1 = solution.search_adj(0)
        sum1.append(count1)
        print("Count: {}".format(count1))
        terrian.belief = np.full((50, 50), 1 / 2500)
        solution = Solution(terrian)
        count2 = solution.search_adj(1)
        sum2.append(count2)
        print("Count: {}".format(count2))
    np.save('./res/q4.npy', (sum1, sum2))
    
main1()