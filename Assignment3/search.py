import map
import numpy as np
import random

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
            if (x, y) == self.tgt_pos:
                terrian_type = self.terrian.get_terrian_type(x, y)
                cannot_found_poss = self.can_not_found[terrian_type]
                dice = random.random()
                # target exists in (x,y), but cannot found.
                if dice < cannot_found_poss:
                    for i in range(self.width):
                        for j in range(self.length):
                            self.update_belief((x, y), (i, j))
                            if self.belief[i][j] > max_poss:
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
            if (x, y) == self.tgt_pos:
                dice = random.random()
                # target exists in (x,y), but cannot found.
                if dice < cannot_found_poss:
                    for i in range(self.width):
                        for j in range(self.length):
                            self.update_belief((x, y), (i, j))
                            if self.belief[i][j] * cannot_found_poss > max_poss:
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
                        if self.belief[i][j] * cannot_found_poss > max_poss:
                            max_i = i
                            max_j = j
            
            # found the postion with max probability of contains target.
            x = max_i
            y = max_j

def main():
    sum1 = 0
    for i in range(10):
        terrian = map.Map(50,50)
        solution = Solution(terrian)
        count1 = solution.search_1()
        sum1 += count1
        print("Count under rule 1: {}".format(count1))
    print("Average for rule 1: {}".format(sum1 / 10))

    sum2 = 0
    for i in range(10):
        terrian = map.Map(50,50)
        solution = Solution(terrian)
        count2 = solution.search_2()
        sum2 += count2
        print("Count under rule 2: {}".format(count2))
    print("Average for rule 2: {}".format(sum2 / 10)) 

main()    