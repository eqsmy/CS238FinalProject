from hookejeeves import HookeJeevesPolicySearch
from policyeval import MonteCarloPolicyEvaluation
import numpy as np
from helpers import new_start_state, hand_info, Cards, play_game, pi_random, player_turn

# this is where the function goes that turns the parameters into an action
# TODO
def pi(theta, s):
    # search for melds, retrieve deadwood

    # actions
    # group 1: draw from deck, discard from hand
    # group 2: draw from deck, discard from hand
    # group 3: draw from deck, discard from deck

    num_melds, deadwood, num_cards_in_melds = hand_info(s, 1)
    #print(deadwood)

    knock = np.random.rand()
    if deadwood == 0:
        print('GIN GIN GIN GIN GIN GIN GING ING')
        return 23
    elif deadwood < 10:
        if deadwood < 5 and knock < theta[0]:
            print('KNOCK')
            return 22
        elif deadwood < 10 and knock < theta[1]:
            return 22

    stock = len(np.where(s == Cards.STOCK.value)[0])
    rand1 = np.random.rand()
    top_discard_idx = np.where(s == Cards.TOP_DISCARD.value)
    hand_idx = np.where(s == Cards.PLAYER_1.value)
    for i in hand_idx[0]:
        s_prime = player_turn(s, i+12, 1)
        _, d_prime, _ = hand_info(s_prime, 1)
        if stock < 10:
            if d_prime - deadwood < 0 and 1/(d_prime - deadwood) < theta[3]:
                return i + 12
        else:
            if d_prime - deadwood < 0 and 1/(d_prime - deadwood) < theta[4]:
                return i + 12
    
    top_stock_idx = np.where(s == Cards.TOP_STOCK.value)
    for i in hand_idx[0]:
        s_prime = player_turn(s, i+1, 1)
        _, d_prime, _ = hand_info(s_prime, 1)
        if stock < 10:
            if d_prime - deadwood < 0 and 1/(d_prime - deadwood) < theta[6]:
                return i + 1
        else:
            if d_prime - deadwood < 0 and 1/(d_prime - deadwood) < theta[7]:
                return i + 1

    return 11

s = new_start_state()
d, n_rollouts = 5, 5
U = MonteCarloPolicyEvaluation(s, d, n_rollouts)

theta, alpha, c, epsilon = np.full(8, 0.5), 0.75, 0.95, 0.1
M = HookeJeevesPolicySearch(theta, alpha, c, epsilon)
theta = M.optimize(pi, U)
print(theta)



num_games = 200
result = [play_game(new_start_state(), pi, theta) for i in range(0, num_games)]
wins = result.count(1)
losses = result.count(-1)
ties = result.count(0)
win_rate = wins/num_games
loss_rate = losses/num_games
tie_rate = ties/num_games
print(f"Win rate: {win_rate}")
print(f"Loss rate: {loss_rate}")
print(f"Tie rate: {tie_rate}")

random_result = [play_game(new_start_state(), pi_random, theta) for i in range(0, num_games)]
wins = random_result.count(1)
losses = random_result.count(-1)
ties = random_result.count(0)
win_rate = wins/num_games
loss_rate = losses/num_games
tie_rate = ties/num_games
print(f"RANDOM Win rate: {win_rate}")
print(f"RANDOM Loss rate: {loss_rate}")
print(f"RANDOM Tie rate: {tie_rate}")