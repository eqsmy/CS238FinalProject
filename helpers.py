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



# find s prime from state and action
def player_step(s, a, player):
    stock = np.where(s == Cards.STOCK.value)
    draw = np.where(s == Cards.TOP_STOCK.value)

    # end of deck is reached
    if end_of_deck(s):
        return s, score(s, a, player)
        
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

    if player == Cards.PLAYER_1.value:
        reward = score(s, a, player)
        return s, reward
    return s, 0

def pi_random(theta, s):
    return np.random.randint(1, 24)

def deadwood(s, player):
    return np.random.randint(1, 20)

def in_set(l, r, locked):
    for i in range(l, r + 1):
        if i in locked:
            return True
    return False

def find_runs(row, locked):
    # row = [0,1,0,1,1,0,0,0,1,1,1]
    # print(row)
    # locked = [9]
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
    #print(num_runs)
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
            #print(s[:,i])
            binary[:,i] = np.where(binary[:,i] == 1, -1, 0)
            #print(s)
            num_melds += 1
            locked.append(i)  
    
    suits, _ = binary.shape
    for i in range(suits):
        #print('s[i] = ', binary[i])
        melds_in_row, num_cards_in_runs = find_runs(binary[i], locked)
        num_cards_in_melds += num_cards_in_runs
        #print(f"Melds: {melds_in_row}")
        num_melds += melds_in_row
    deadwood = deadwood_value(binary)
    #print(np.where(binary == 1))
    #print(f"Num Cards: {num_cards_in_melds}")
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

# TODO: calculate reward for new s state
# only called for player 1
def score(s, a, player):
    # if new meld is formed, +4?
        # difference between new state and old state would be positive
    # if deadwood score goes down then add points
    
    p1_nummelds, p1_deadwood, _ = hand_info(s, 1)
    p2_nummelds, p2_deadwood, _ = hand_info(s, 2)

    scale = 100
    # Gin
    if a == 23:
        return scale * (20 + p2_deadwood)
    # Knock
    elif a == 22:
        dif = p2_deadwood - p1_deadwood
        # player 1 won
        if dif > 0:
            return scale * (dif + 10)
        # player 2 won
        elif dif <= 0:
            return scale * (dif - 10)
    # Otherwise
    else:
        r = 4 * p1_nummelds - 5 * p1_deadwood
        return r

    # otherwise return 0?
    # reward if end of deck is reached?
    reward = np.random.randint(20)
    return reward


s = new_start_state()

# s = np.zeros((4,13), dtype=np.int8)
# s[0][1] = 1
# s[1][1] = 1
# s[2][1] = 1
# s[3][1] = 1
# s[1][1:5] = 1
# s[2][8] = 1

# print(s)
#print(result)


