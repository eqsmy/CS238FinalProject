import numpy as np
import random

def rollout(s, pi, d, theta):
    ret = 0.0
    for t in range(0, d):
        a = pi(theta, s)
        s, r = step(s, a)
        #ret += P.gamma^(t-1) * r
        ret += r
    return ret

# find s prime from state and action
def step(s, a):
    if a <= 10:
        # draw from deck, discard card a-1
        hand = np.where(s == 1)
        deck = np.where(s == 0)
        draw = deck[np.random.randint(0,len(deck))]
        print(draw)
        s[draw] = 1
        discard = hand[a-1]
        topdiscard = np.where(s == 3)
        s[topdiscard] = 4
        s[discard] = 3
    elif a == 11:
        # draw from deck, discard drawn card
        deck = np.where(s == 0)
        draw = deck[np.random.randint(len(deck))]
        topdiscard = np.where(s == 3)
        s[draw] = 3
        s[topdiscard] = 4
    else:
        # pick up discard card, discard card a - 12
        topdiscard = np.where(s == 3)
        s[topdiscard] = 1
        hand = np.where(s == 1)
        print(hand)
        print(hand[1])
        discard = hand[a-12]
        s[discard] = 3

    # TODO: calculate reward for new s state
    reward = 1
    return s, reward

class MonteCarloPolicyEvaluation:
    def __init__(self, initial_state, depth, num_samples):
        self.initial_s = initial_state
        self.d = depth
        self.m = num_samples

    def evaluate(self, pi, theta):
        # TODO write rollout policy
        def R(pi): rollout(self.initial_s, pi, self.d, theta)
        return np.mean([R(pi) for i in range(0, self.m)])
