# TODO: write utility function U
# TODO: implement for our problem
# TODO: test this with dummy data for our problem

# good example of implementation on page 213

import numpy as np

class HookeJeevesPolicySearch:
    def __init__(parameters, step_size, reduction_factor, term_step_size):
        self.theta = parameters
        self.alpha = step_size
        self.c = reduction_factor
        self.epsilon = term_step_size

    def optimize(self, pi, U):
        theta = self.theta
        theta_prime = np.empty_like(theta)
        alpha, c, epsilon = self.alpha, self.c, self.epsilon
        u, n = U(pi, theta), len(theta)
        while alpha > epsilon:
            theta_prime = theta
            best = {"i": 0, "sgn": 0, "u": u}
            for i in range(0, n):
                for sgn in [-1, 1]:
                    theta_prime[i] = theta[i] + sgn*alpha
                    u_prime = U(pi, theta_prime)
                    if u_prime > best["u"]:
                        best = {"i": i, "sgn": sgn, "u": u_prime}
                theta_prime[i] = theta[i]
            if best["i"] != 0:
                theta[best["i"]] += best["sgn"]*alpha
                u = best["u"]
            else:
                alpha *= c
        return 0
    
