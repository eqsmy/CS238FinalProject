# from page 213 in the textbook

# QUESTIONS
# do we even need to have a P object to represent the MDP? don't think we'll have an enumerated list of all states
# do we need the MDP object and if so how do we restructure the object to fit the problem?

from hookejeeves import HookeJeevesPolicySearch
from policyeval import MonteCarloPolicyEvaluation
from mdp import MDP
import numpy as np
import scipy as sp

def pi(theta, s):
    return np.random.normal(theta[0]*s, abs(theta[1]) + 0.00001)

b, d, n_rollouts = sp.stats.norm(0.3, 0.1), 10, 3
U = MonteCarloPolicyEvaluation(P, b, d, n_rollouts)
theta, alpha, c, epsilon = [0.0, 1.0], 0.75, 0.75, 0.01
M = HookeJeevesPolicySearch(theta, alpha, c, epsilon)
theta = M.optimize(M, pi, U)