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

# this is where the function goes that turns the parameters into an action
# s will have the form of a matrix of size 4x13
def pi(theta, s):
    return np.random.randint(1, 22)

# deal player hands
s = np.zeros((4, 13))
val = 1
for i in [0,1]:
    for i in range(0, 10):
        coords = (np.random.randint(0,4), np.random.randint(0,13))
        while s[coords] != 0.0:
            coords = (np.random.randint(0,4), np.random.randint(0,13))
        s[coords] = val
    val = 2

print(s)

b, d, n_rollouts = norm(0.3, 0.1), 10, 3
U = MonteCarloPolicyEvaluation(s, d, n_rollouts)
theta, alpha, c, epsilon = [0.0, 1.0], 0.75, 0.75, 0.01
M = HookeJeevesPolicySearch(theta, alpha, c, epsilon)
theta = M.optimize(pi, U)