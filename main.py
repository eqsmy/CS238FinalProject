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


# this is where the function goes that turns the parameters into an action
# s will have the form of a matrix of size 4x13
def pi(theta, s):
    return np.random.randint(1, 22)

s = new_start_state()
b, d, n_rollouts = norm(0.3, 0.1), 10, 3
U = MonteCarloPolicyEvaluation(s, d, n_rollouts)
theta, alpha, c, epsilon = [0.5, 0.5], 0.75, 0.75, 0.01
M = HookeJeevesPolicySearch(theta, alpha, c, epsilon)
theta = M.optimize(pi, U)
print(theta)