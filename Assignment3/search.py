import map
import numpy as np

class Solution:
    def __init__(self, terrian):
        self.terrian = terrian
        self.belief = terrian.belief
        self.can_not_found = {"flat":0.1, "hilly":0.3, "forested":0.5, "caves":0.9}

    def update_belief(self, not_found_pos, pos):
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
    
    