import numpy as np

def rollout(P, s, pi, d):
    ret = 0.0
    for t in range(0, d):
        a = pi(s)
        s, r = randstep(P, s, a)
        ret += P.gamma^(t-1) * r
    return ret

class MonteCarloPolicyEvaluation:
    def __init__(self, problem, initial_dist, depth, num_samples):
        self.P = problem
        self.b = initial_dist
        self.d = depth
        self.m = num_samples

    def evaluate(self, pi, theta):
        # TODO write rollout policy
        def R(pi): rollout(self.P, np.random(self.b), pi, self.d)
        return np.mean([R(pi) for i in range(0, self.m)])
