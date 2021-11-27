import numpy as np
import random
from helpers import rand_idx, new_start_state

def rollout(s, pi, d, theta):
    ret = 0.0
    for t in range(0, d):
        a_1 = pi(theta, s)
        s, r = player_step(s, a_1, 1)
        if r == -1:
            return ret
        #ret += P.gamma^(t-1) * r
        ret += r
        a_2 = pi(theta, s)
        s, _ = player_step(s, a_2, 2)
    return ret

# find s prime from state and action
def player_step(s, a, player):
    deck = np.where(s == 0)
    draw_idx = rand_idx(deck)
    if draw_idx == -1:
        return s, -1
    hand = np.where(s == player)
    topdiscard = np.where(s == 3)
    topdiscard_idx = (topdiscard[0][0], topdiscard[1][0])
    if a <= 10:
        # draw from deck, discard card a-1
        discard_idx = (hand[0][a-1], hand[1][a-1]) 
        s[draw_idx] = player # add to hand
        s[topdiscard_idx] = 4
        s[discard_idx] = 3 # remove from hand
    elif a == 11:
        # draw from deck, discard drawn card
        s[topdiscard_idx] = 4
        s[draw_idx] = 3
    else:
        # pick up discard card, discard card a - 12
        discard_idx = (hand[0][a-12], hand[1][a-12])
        s[topdiscard_idx] = player # add to hand
        s[discard_idx] = 3 # remove from hand
    
    # TODO: calculate reward for new s state
    reward = np.random.randint(10)
    return s, reward

class MonteCarloPolicyEvaluation:
    def __init__(self, initial_state, depth, num_samples):
        self.initial_s = initial_state
        self.d = depth
        self.m = num_samples

    def evaluate(self, pi, theta):
        start_state = new_start_state()
        result = [rollout(start_state, pi, self.d, theta) for i in range(0, self.m)]
        return np.mean(result)
