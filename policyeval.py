import numpy as np
import random
from helpers import rand_idx, new_start_state, Cards

def pi_random(theta, s):
    return np.random.randint(1, 22)

def rollout(s, pi, d, theta):
    ret = 0.0
    for t in range(0, d):
        a_1 = pi(theta, s)
        s, r = player_step(s, a_1, 1)
        if r == -1: # TODO: can change this to if r != 0 once scoring is implemented
            return ret
        #ret += P.gamma^(t-1) * r
        ret += r
        a_2 = pi_random(theta, s)
        s, _ = player_step(s, a_2, 2)
    return ret

# TODO: calculate reward for new s state
def score(s, a):
    # positive reward for player 1, negative for player 2?
    # if a is 23 (gin), r is 20 + opponent's deadwood
    # if a is 22 (knock), r is difference between deadwoods for the winner plus 10 points if the non-knocking player won
    # otherwise return 0?
    # reward if end of deck is reached?
    reward = np.random.randint(20)
    return reward

# find s prime from state and action
def player_step(s, a, player):
    stock = np.where(s == Cards.STOCK.value)
    draw = np.where(s == Cards.TOP_STOCK.value)
    if len(draw[0]) == 0 or len(stock[0]) == 0:
        return s, score(s, a)
    draw_idx = (draw[0][0], draw[1][0])
    new_topstock_idx = rand_idx(stock)
    hand = np.where(s == player)
    topdiscard = np.where(s == Cards.TOP_DISCARD.value)
    topdiscard_idx = (topdiscard[0][0], topdiscard[1][0])
    if a <= 10:
        # draw from deck, discard card a-1
        discard_idx = (hand[0][a-1], hand[1][a-1]) 
        s[draw_idx] = player # add to hand
        s[topdiscard_idx] = Cards.NON_TOP_DISCARD.value
        s[discard_idx] = Cards.TOP_DISCARD.value # remove from hand
        s[new_topstock_idx] = Cards.TOP_STOCK.value
    elif a == 11:
        # draw from deck, discard drawn card
        s[topdiscard_idx] = Cards.NON_TOP_DISCARD.value
        s[draw_idx] = Cards.TOP_DISCARD.value
        s[new_topstock_idx] = Cards.TOP_STOCK.value
    else:
        # pick up discard card, discard card a - 12
        discard_idx = (hand[0][a-12], hand[1][a-12])
        s[topdiscard_idx] = player # add to hand
        s[discard_idx] = Cards.TOP_DISCARD.value # remove from hand
    reward = score(s, a)
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
