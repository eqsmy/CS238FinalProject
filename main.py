# from page 213 in the textbook

# QUESTIONS
# do we even need to have a P object to represent the MDP? don't think we'll have an enumerated list of all states
# do we need the MDP object and if so how do we restructure the object to fit the problem?

from hookejeeves import HookeJeevesPolicySearch
from policyeval import MonteCarloPolicyEvaluation
from mdp import MDP
import numpy as np
import random
from helpers import new_start_state, hand_info, player_step, Cards
from enum import Enum

# this is where the function goes that turns the parameters into an action
# TODO
def pi(theta, s):
    # search for melds, retrieve deadwood

    # actions
    # group 1: draw from deck, discard from hand
    # group 2: draw from deck, discard from hand
    # group 3: draw from deck, discard from deck

    num_melds, deadwood, num_cards_in_melds = hand_info(s, 1)

    knock = np.random.rand()
    if deadwood < 10:
        if deadwood < 5 and knock < theta[0]:
            print('KNOCK')
            return 22
        elif deadwood < 10 and knock < theta[1]:
            return 22
    elif deadwood == 0:
        print('GIN GIN GIN GIN GIN GIN GING ING')
        return 23

    rand1 = np.random.rand()
    top_discard_idx = np.where(s == Cards.TOP_DISCARD.value)
    hand_idx = np.where(s == Cards.PLAYER_1.value)
    for i in hand_idx[0]:
        if hand_idx[0][i] - top_discard_idx[0][0] > 2 and rand1 < theta[2]:
            return i + 12
        elif hand_idx[1][i] - top_discard_idx[1][0] > 2 and rand1 < theta[3]:
            return i + 12
    
    top_stock_idx = np.where(s == Cards.TOP_STOCK.value)
    for i in hand_idx[0]:
        if hand_idx[0][i] - top_stock_idx[0][0] > 2 and rand1 < theta[4]:
            return i + 1
        elif hand_idx[1][i] - top_stock_idx[1][0] > 2 and rand1 < theta[5]:
            return i + 1

    return 11


    # policy = theta1*state1 + theta2*state2 + theta3*action1 + theta4*action2


    # if no deadwood, return 23 (gin)
    # if deadwood less than 10, return 22
    # if top of discard makes meld, draw it and discard a deadwood
        # discard lower or higher (parameter)
    # if top of stock makes meld, draw it and discard a deadwood --> return between 1 and 10
        # discard lower or higher
    return np.random.randint(1, 22)


s = new_start_state()
d, n_rollouts = 15, 3
U = MonteCarloPolicyEvaluation(s, d, n_rollouts)

theta, alpha, c, epsilon = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5], 0.75, 0.9, 0.01
M = HookeJeevesPolicySearch(theta, alpha, c, epsilon)
theta = M.optimize(pi, U)
print(theta)