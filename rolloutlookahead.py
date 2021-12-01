from helpers import player_step, pi_random

class RolloutLookahead():
    def __init__(rollout_policy, depth):
        self.pi = rollout_policy
        self.d = depth
    
    def runrolloutlookahead(self, s, gamma):
        U(s) = rollout(s, self.pi, self.d, gamma)
        return 

    
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