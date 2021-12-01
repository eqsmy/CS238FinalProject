# from page 213 in the textbook

# QUESTIONS
# do we even need to have a P object to represent the MDP? don't think we'll have an enumerated list of all states
# do we need the MDP object and if so how do we restructure the object to fit the problem?

from hookejeeves import HookeJeevesPolicySearch
from policyeval import MonteCarloPolicyEvaluation
from mdp import MDP
import numpy as np
from scipy.stats import norm
import random
from helpers import rand_idx, new_start_state
from enum import Enum

# this is where the function goes that turns the parameters into an action
# TODO
def pi(theta, s):
    # search for melds, retrieve deadwood
    # find melds: input state matrix, output 
        

    # if no deadwood, return 23 (gin)
    # if deadwood less than 10, return 22
    # if top of discard makes meld, draw it and discard a deadwood
        # discard lower or higher (parameter)
    # if top of stock makes meld, draw it and discard a deadwood --> return between 1 and 10
        # discard lower or higher
    return np.random.randint(1, 24)

class Cards(Enum):
    STOCK = 0
    PLAYER_1 = 1
    PLAYER_2 = 2
    TOP_DISCARD = 3
    NON_TOP_DISCARD = 4
    TOP_STOCK = 5


s = new_start_state()
d, n_rollouts = 10, 3
U = MonteCarloPolicyEvaluation(s, d, n_rollouts)
theta, alpha, c, epsilon = [0.5, 0.5], 0.75, 0.9, 0.01
M = HookeJeevesPolicySearch(theta, alpha, c, epsilon)
theta = M.optimize(pi, U)
print(theta)