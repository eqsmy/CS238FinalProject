import numpy as np
from helpers import new_start_state, pi_random, end_of_deck, knock_winner, gin_points, player_turn
    
# return end of game points
def full_rollout(s, pi, theta):
    while True:
        # player 1 turn
        a_1 = pi(theta, s)
        #s, _ = player_step(s, a_1, 1)
        s = player_turn(s, a_1, 1)
        if a_1 == 23:
            score = gin_points(s, 1)
            return score
        elif a_1 == 22:
            _, points = knock_winner(s, 1)
            return points
        elif end_of_deck(s):
            return -5

        # player 2 turn (random)
        a_2 = pi_random(theta, s)
        s = player_turn(s, a_2, 2)
        #s, _ = player_step(s, a_2, 2)
        if a_2 == 23:
            score = gin_points(s, 2)
            return score
        elif a_2 == 22:
            _, points = knock_winner(s, 2)
            return points
        elif end_of_deck(s):
            return -5

class MonteCarloPolicyEvaluation:
    def __init__(self, initial_state, depth, num_samples):
        self.initial_s = initial_state
        self.d = depth
        self.m = num_samples

    def evaluate(self, pi, theta):
        #start_state = new_start_state()
        result = [full_rollout(new_start_state(), pi, theta) for i in range(0, self.m)]
        return np.mean(result)
