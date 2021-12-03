import numpy as np
from enum import Enum

def rand_idx(arrays):
    if len(arrays[0]) == 0: return -1
    rand_int = np.random.randint(len(arrays[0]))
    return (arrays[0][rand_int], arrays[1][rand_int])

def new_start_state():
    s = np.zeros((4, 13), dtype=np.int64)
    val = Cards.PLAYER_1.value
    for i in [0,1]:
        for i in range(0, 10):
            coords = (np.random.randint(0,4), np.random.randint(0,13))
            while s[coords] != 0.0:
                coords = (np.random.randint(0,4), np.random.randint(0,13))
            s[coords] = val
        val = Cards.PLAYER_2.value

    stock = np.where(s == Cards.STOCK.value)
    s[rand_idx(stock)] = Cards.TOP_DISCARD.value
    stock = np.where(s == Cards.STOCK.value)
    s[rand_idx(stock)] = Cards.TOP_STOCK.value

    return s

class Cards(Enum):
    STOCK = 0
    PLAYER_1 = 1
    PLAYER_2 = 2
    TOP_DISCARD = 3
    NON_TOP_DISCARD = 4
    TOP_STOCK = 5

def end_of_deck(s):
    stock = np.where(s == Cards.STOCK.value)
    draw = np.where(s == Cards.TOP_STOCK.value)

    # end of deck is reached
    if len(draw[0]) == 0 or len(stock[0]) == 0:
        return True
    else:
        return False

def player_turn(s, a, player):
    stock = np.where(s == Cards.STOCK.value)
    draw = np.where(s == Cards.TOP_STOCK.value)

    # end of deck is reached
    if end_of_deck(s):
        return s
        
    draw_idx = (draw[0][0], draw[1][0])
    new_topstock_idx = rand_idx(stock)
    hand = np.where(s == player)
    topdiscard = np.where(s == Cards.TOP_DISCARD.value)
    topdiscard_idx = (topdiscard[0][0], topdiscard[1][0])
    if a <= 10:
        # draw from deck, discard card a-1
        discard_idx = (hand[0][a-1], hand[1][a-1]) 
        s[draw_idx] = player # add to hand
        s[topdiscard_idx] = Cards.NON_TOP_DISCARD.value
        s[discard_idx] = Cards.TOP_DISCARD.value # remove from hand
        s[new_topstock_idx] = Cards.TOP_STOCK.value
    elif a == 11:
        # draw from deck, discard drawn card
        s[topdiscard_idx] = Cards.NON_TOP_DISCARD.value
        s[draw_idx] = Cards.TOP_DISCARD.value
        s[new_topstock_idx] = Cards.TOP_STOCK.value
    elif a <= 21:
        # pick up discard card, discard card a - 12
        discard_idx = (hand[0][a-12], hand[1][a-12])
        s[topdiscard_idx] = player # add to hand
        s[discard_idx] = Cards.TOP_DISCARD.value # remove from hand

    return s

def pi_random(theta, s):
    _, deadwood, _ = hand_info(s, 2)
    if deadwood == 0:
        return 23
    elif deadwood < 10:
        return 22
    return np.random.randint(1, 22)

def deadwood(s, player):
    return np.random.randint(1, 20)

def in_set(l, r, locked):
    for i in range(l, r + 1):
        if i in locked:
            return True
    return False

def find_runs(row, locked):
    num_runs = 0
    num_cards_in_runs = 0
    l = 0 
    r = 2
    while r < len(row):
        #3 or 4 run exists
        if sum(row[l:r + 1]) == 3 and not in_set(l, r, locked): 
            #check for 4 
            if r + 1 < len(row) and sum(row[l:r + 2]) == 4:
                num_runs +=1
                row[l:r + 2] = -1
                num_cards_in_runs += 4
                l += 4; r += 4
            else: 
                num_runs +=1
                row[l:r + 1] = -1
                num_cards_in_runs += 3
                l += 3; r += 3
        else:
            l += 1; r += 1 
    return num_runs, num_cards_in_runs

def hand_info(s, player):
    #assume numbers of interst at 1 and other numbers are 0
    num_melds = 0

    #find sets
    binary = np.where(s == player, 1, 0) #zero out all values execpt one
    sums = binary.sum(axis=0)

    locked = []
    num_cards_in_melds = 0

    # set_counts = np.bincount(sums)
    for i in range(len(sums)):
        if sums[i] == 3 or sums[i] == 4: 
            num_cards_in_melds += sums[i]
            binary[:,i] = np.where(binary[:,i] == 1, -1, 0)
            num_melds += 1
            locked.append(i)  
    
    suits, _ = binary.shape
    for i in range(suits):
        melds_in_row, num_cards_in_runs = find_runs(binary[i], locked)
        num_cards_in_melds += num_cards_in_runs
        num_melds += melds_in_row
    deadwood = deadwood_value(binary)
    return num_melds, deadwood, num_cards_in_melds

def deadwood_value(binary):
    locs = np.where(binary == 1)
    value = 0
    for l in locs[1]:
        if l < 10:
            value += l + 1
        else:
            value += 10
    return value

# return 1 for win, 0 for draw, -1 for lose
def play_game(s, pi, theta):
    while True:
        # player 1 turn
        a_1 = pi(theta, s)
        s = player_turn(s, a_1, 1)
        #s, _ = player_step(s, a_1, 1)
        if a_1 == 23:
            return 1
        elif a_1 == 22:
            winner, _ = knock_winner(s, 1)
            if winner == 1:
                return 1
            elif winner == 2:
                return -1
        elif end_of_deck(s):
            return 0

        # player 2 turn (random)
        a_2 = pi_random(theta, s)
        s = player_turn(s, a_2, 2)
        #s, _ = player_step(s, a_2, 2)
        if a_2 == 23:
            return -1
        elif a_2 == 22:
            winner, _ = knock_winner(s, 2)
            if winner == 2:
                return -1
            elif winner == 1:
                return 1
        elif end_of_deck(s):
            return 0

def knock_winner(s, player):
    _, p1_deadwood, _ = hand_info(s, 1)
    _, p2_deadwood, _ = hand_info(s, 2)
    dif = p2_deadwood - p1_deadwood
    if dif > 0:
        # player 1 won and knocked
        if player == 1:
            return 1, dif
        # player 1 won but player 2 knocked
        else:
            return 1, dif + 10
    else:
        # player 2 won and knocked
        if player == 2:
            return 2, dif
        # player 2 won but player 1 knocked
        else:
            return 2, dif - 10

# positive if player 1 won, negative if player 2 won 
def gin_points(s, player):
    _, p1_deadwood, _ = hand_info(s, 1)
    _, p2_deadwood, _ = hand_info(s, 2)

    if player == 1:
        return 20 + p2_deadwood
    else:
        return -1 * (20 + p1_deadwood)

print()
print("Example Starting State:")
print("       A   2   3   4   5   6   7   8   9  10   J   Q   K")
print()
s = new_start_state()
suits = ["C", "D", "H", "S"]
i = 0
for row in s:
    print(suits[i], end="      ")
    for r in row:
        print(r, end="   ")
    print()
    i += 1
print()