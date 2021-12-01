import numpy as np
import random
from helpers import rand_idx, new_start_state, Cards, player_step, pi_random, end_of_deck

def rollout(s, pi, d, theta):
    ret = 0.0
    #for t in range(0, d):
    while True:
        a_1 = pi(theta, s)
        s, r = player_step(s, a_1, 1)
        if a_1 == 23 or a_1 == 22 or end_of_deck(s): # TODO: can change this to if r != 0 once scoring is implemented
            return ret
        #ret += P.gamma^(t-1) * r
        ret += r
        a_2 = pi_random(theta, s)
        s, _ = player_step(s, a_2, 2)
    return ret

class MonteCarloPolicyEvaluation:
    def __init__(self, initial_state, depth, num_samples):
        self.initial_s = initial_state
        self.d = depth
        self.m = num_samples

    def evaluate(self, pi, theta):
        #start_state = new_start_state()
        result = [rollout(new_start_state(), pi, self.d, theta) for i in range(0, self.m)]
        return np.mean(result)
