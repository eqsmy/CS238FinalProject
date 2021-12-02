import numpy as np

class HookeJeevesPolicySearch:
    def __init__(self, parameters, step_size, reduction_factor, term_step_size):
        self.theta = parameters
        self.alpha = step_size
        self.c = reduction_factor
        self.epsilon = term_step_size

    def optimize(self, pi, U):
        theta = self.theta
        theta_prime = np.empty_like(theta)
        alpha, c, epsilon = self.alpha, self.c, self.epsilon
        u, n = U.evaluate(pi, theta), len(theta)
        idx = 1
        while alpha > epsilon:
            theta_prime = theta
            best = {"i": -1, "sgn": 0, "u": u}
            for i in range(0, n):
                for sgn in [-1, 1]:
                    theta_prime[i] = theta[i] + sgn*alpha
                    u_prime = U.evaluate(pi, theta_prime)
                    if u_prime > best["u"]:
                        best = {"i": i, "sgn": sgn, "u": u_prime}
                theta_prime[i] = theta[i]
            if best["i"] != -1:
                theta[best["i"]] += best["sgn"]*alpha
                u = best["u"]
            else:
                alpha *= c
            idx += 1
            print(theta)
            print(f"alpha: {alpha}, epsilon: {epsilon}")
        return theta