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

def find_runs(row, locked):
    #[0,1,1,1,1,0,0,0,0,0,0]
    num_runs = 0
    l = 0 
    r = 2
    while r < len(row):
        #3 or 4 run exists
        if sum(row[l:r + 1]) == 3: 
            #check for 4 
            if r + 1 < len(row) and sum(row[l:r + 2]) == 4:
                num_runs +=1
                l += 4; r += 4
            else: 
                num_runs +=1
                l += 3; r += 3
        else:
            l += 1; r += 1 
            
    return num_runs




def num_melds(s, player):
    #assume numbers of interst at 1 and other numbers are 0

    num_melds = 0

    #find sets
    binary = np.where(s == player, 1, 0) #zero out all values execpt one
    print(binary)
    sums = binary.sum(axis=0)

    locked = []

    # set_counts = np.bincount(sums)
    for i in range(len(sums)):
        if sums[i] == 3 or sums[i] == 4: 
            num_melds += 1
            locked.append(i)  
    
    suits, _ = binary.shape
    for i in range(suits):
        print('s[i] = ', binary[i])
        melds_in_row = find_runs(binary[i], locked)
        print(melds_in_row)
        num_melds += melds_in_row
    return num_melds    

def find_melds(s, ):
    s = [[0,0,],[],[],[]]

# TODO: calculate reward for new s state
# only called for player 1
def score(s, a, player):
    # if new meld is formed, +4?
        # difference between new state and old state would be positive
    # if deadwood score goes down then add points

    # Gin
    if a == 23:
        return 20 + deadwood(s, 2)
    # Knock
    elif a == 22:
        dif = deadwood(s, 2) - deadwood(s, 1)
        # player 1 won
        if dif > 0:
            return dif + 10
        # player 2 won
        elif dif <= 0:
            return dif - 10
    # Otherwise
    else:
        r = 4 * num_melds(s, player) - 5 * deadwood(s, player)
        return r

    # otherwise return 0?
    # reward if end of deck is reached?
    reward = np.random.randint(20)
    return reward


s = new_start_state()

# print(s)
result = num_melds(s, 1)
print(result)


