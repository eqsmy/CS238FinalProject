# def rollout(s, pi, d, theta):
#     ret = 0.0
#     #for t in range(0, d):
#     gamma = 0.9
#     t = 0
#     for _ in range(0, d):
#     #while True:
#         a_1 = pi(theta, s)
#         s, r = player_step(s, a_1, 1)
#         if a_1 == 23 or a_1 == 22 or end_of_deck(s):
#             r = score(s, a_1, 1)
#             return r
#         ret += pow(gamma,t-1) * r
#         t += 1
#         #ret += r
#         a_2 = pi_random(theta, s)
#         s, _ = player_step(s, a_2, 2)
#         if a_2 == 23 or a_2 == 22 or end_of_deck(s):
#             r = score(s, -1, 1)
#             return r
#     return ret

# # find s prime from state and action
# def player_step(s, a, player):
#     stock = np.where(s == Cards.STOCK.value)
#     draw = np.where(s == Cards.TOP_STOCK.value)

#     # end of deck is reached
#     if end_of_deck(s):
#         return s, score(s, a, player)
        
#     draw_idx = (draw[0][0], draw[1][0])
#     new_topstock_idx = rand_idx(stock)
#     hand = np.where(s == player)
#     topdiscard = np.where(s == Cards.TOP_DISCARD.value)
#     topdiscard_idx = (topdiscard[0][0], topdiscard[1][0])
#     if a <= 10:
#         # draw from deck, discard card a-1
#         discard_idx = (hand[0][a-1], hand[1][a-1]) 
#         s[draw_idx] = player # add to hand
#         s[topdiscard_idx] = Cards.NON_TOP_DISCARD.value
#         s[discard_idx] = Cards.TOP_DISCARD.value # remove from hand
#         s[new_topstock_idx] = Cards.TOP_STOCK.value
#     elif a == 11:
#         # draw from deck, discard drawn card
#         s[topdiscard_idx] = Cards.NON_TOP_DISCARD.value
#         s[draw_idx] = Cards.TOP_DISCARD.value
#         s[new_topstock_idx] = Cards.TOP_STOCK.value
#     elif a <= 21:
#         # pick up discard card, discard card a - 12
#         discard_idx = (hand[0][a-12], hand[1][a-12])
#         s[topdiscard_idx] = player # add to hand
#         s[discard_idx] = Cards.TOP_DISCARD.value # remove from hand

#     if player == Cards.PLAYER_1.value:
#         reward = score(s, a, player)
#         return s, reward
#     return s, 0

# only called for player 1
# def score(s, a, player):
#     p1_nummelds, p1_deadwood, _ = hand_info(s, 1)
#     p2_nummelds, p2_deadwood, _ = hand_info(s, 2)

#     scale = 100
#     # Gin
#     if a == 23:
#         return scale * (20 + p2_deadwood)
#     # Knock
#     elif a == 22:
#         winner, points = knock_winner(s)
#         #dif = p2_deadwood - p1_deadwood
#         # player 1 won
#         if winner == 1:
#             return scale * points
#         # player 2 won
#         elif winner == 2:
#             return scale * points
#     # Otherwise
#     else:
#         r = 4 * p1_nummelds - 5 * p1_deadwood
#         return r

#     reward = np.random.randint(20)
#     return reward